import { getAttributionSource } from './AttributionTracker.js';
import { captureAndPersistCampaign } from './WhatsAppDynamicMessage.js';
import { error as logError, info as logInfo } from './logger.js';

/**
 * @fileoverview Gestión del formulario multi-paso de contacto comercial y cotización de DataMaq.
 * Soporta navegación bidireccional (avanzar, retroceder, clics en stepper),
 * sincronización de barra de progreso y envío resiliente de leads con tipado estricto.
 */

export class FormManager {
    /**
     * @param {HTMLFormElement} formElement - Elemento del formulario de contacto.
     * @param {string} apiUrl - URL del endpoint backend para el envío de leads.
     */
    constructor(formElement, apiUrl) {
        /** @type {HTMLFormElement} */
        this.form = formElement;
        /** @type {string} */
        this.apiUrl = apiUrl;
        /** @type {HTMLElement | Document} */
        this.container = /** @type {HTMLElement | null} */ (this.form.closest('.c-contact')) || document;
        
        /** @type {HTMLElement[]} */
        this.steps = Array.from(this.form.querySelectorAll('.c-contact__step-panel'));
        /** @type {HTMLElement[]} */
        this.stepperItems = Array.from(this.container.querySelectorAll('.c-contact__stepper-item'));
        /** @type {HTMLElement[]} */
        this.stepperTriggers = Array.from(this.container.querySelectorAll('.c-contact__stepper-trigger'));
        /** @type {HTMLElement | null} */
        this.progressFill = this.container.querySelector('.c-contact__progress-fill');
        /** @type {HTMLElement | null} */
        this.progressText = this.container.querySelector('.c-contact__progress-text');
        /** @type {HTMLElement | null} */
        this.progressBar = this.container.querySelector('.c-contact__progress');
        
        /** @type {HTMLButtonElement | null} */
        this.nextBtn = this.form.querySelector('.c-contact__btn--next') || this.form.querySelector('.c-contact__actions button:last-child');
        /** @type {HTMLButtonElement | null} */
        this.prevBtn = this.form.querySelector('.c-contact__btn--prev');
        
        /** @type {number} */
        this.currentStep = 0;
        /** @type {number} */
        this.maxReachedStep = 0;
        /** @type {string} */
        this.finalCtaText = 'Solicitar Diagnóstico y Cotización';

        this.init();
    }

    /**
     * Inicializa los listeners de eventos y el estado visual inicial del formulario.
     * @returns {void}
     */
    init() {
        if (this.nextBtn) {
            this.nextBtn.addEventListener('click', () => this.handleNextOrSubmit());
        }

        if (this.prevBtn) {
            this.prevBtn.addEventListener('click', () => this.handlePrev());
        }

        // Habilitar clics en los indicadores del stepper (eliminación de Dead Clicks)
        this.stepperTriggers.forEach((trigger, idx) => {
            trigger.addEventListener('click', () => this.handleStepperClick(idx));
        });

        // Asegurar estado visual inicial consistente
        this.showStep(0);
    }

    /**
     * Maneja el avance al siguiente paso o el envío final del formulario si está en el último paso.
     * @returns {void}
     */
    handleNextOrSubmit() {
        if (this.currentStep < this.steps.length - 1) {
            this.showStep(this.currentStep + 1);
        } else {
            this.submitForm();
        }
    }

    /**
     * Maneja el retroceso al paso anterior.
     * @returns {void}
     */
    handlePrev() {
        if (this.currentStep > 0) {
            this.showStep(this.currentStep - 1);
        }
    }

    /**
     * Permite la navegación directa por clics en los nodos del stepper.
     * @param {number} index - Índice del paso objetivo.
     * @returns {void}
     */
    handleStepperClick(index) {
        // Permitir saltar a pasos previos ya visitados o al siguiente inmediato
        if (index <= this.maxReachedStep + 1) {
            this.showStep(index);
        }
    }

    /**
     * Muestra el paso especificado y sincroniza clases de accesibilidad y barra de progreso.
     * @param {number} index - Índice del paso a visualizar.
     * @returns {void}
     */
    showStep(index) {
        if (index < 0 || index >= this.steps.length) return;

        this.maxReachedStep = Math.max(this.maxReachedStep, index);

        // 1. Alternar visibilidad de paneles
        this.steps.forEach((panel, i) => {
            if (i === index) {
                panel.classList.remove('is-hidden');
                panel.style.display = 'block';
            } else {
                panel.classList.add('is-hidden');
                panel.style.display = 'none';
            }
        });

        // 2. Sincronizar clases y accesibilidad en el stepper
        this.stepperItems.forEach((item, i) => {
            const trigger = this.stepperTriggers[i];
            if (i === index) {
                item.classList.add('is-active');
                item.classList.remove('is-completed');
                trigger?.setAttribute('aria-current', 'step');
            } else if (i < index) {
                item.classList.remove('is-active');
                item.classList.add('is-completed');
                trigger?.removeAttribute('aria-current');
            } else {
                item.classList.remove('is-active');
                item.classList.remove('is-completed');
                trigger?.removeAttribute('aria-current');
            }
        });

        // 3. Sincronizar barra y texto de progreso
        const percent = Math.round(((index + 1) / this.steps.length) * 100);
        if (this.progressFill) {
            this.progressFill.style.width = `${percent}%`;
        }
        if (this.progressBar) {
            this.progressBar.setAttribute('aria-valuenow', (index + 1).toString());
        }
        if (this.progressText) {
            this.progressText.textContent = `Paso ${index + 1} de ${this.steps.length}`;
        }

        // 4. Sincronizar botones de acción
        if (this.prevBtn) {
            if (index === 0) {
                this.prevBtn.classList.add('tw:hidden');
                this.prevBtn.style.display = 'none';
            } else {
                this.prevBtn.classList.remove('tw:hidden');
                this.prevBtn.style.display = 'inline-flex';
            }
        }

        if (this.nextBtn) {
            if (index === this.steps.length - 1) {
                this.nextBtn.textContent = this.finalCtaText;
            } else {
                this.nextBtn.textContent = 'Continuar →';
            }
        }

        this.currentStep = index;
    }

    /**
     * Recolecta y estructura los datos de todos los campos del formulario multi-paso,
     * combinándolos con la información de atribución y campañas publicitarias.
     *
     * @returns {import('../types.js').ContactSubmitPayload} Payload validado listo para enviar a la API.
     */
    collectData() {
        /**
         * @param {string} id
         * @returns {string}
         */
        const getVal = (id) => {
            const input = /** @type {HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement | null} */ (
                this.form.querySelector('#' + id) || this.form.querySelector(`[name="${id}"]`)
            );
            return input ? input.value : '';
        };

        const campaignData = captureAndPersistCampaign() || {
            utmCampaign: null,
            utmSource: null,
            utmMedium: null,
            gclid: null,
            fbclid: null,
            liFatId: null,
            timestamp: Date.now()
        };

        const cargo = getVal('contacto-cargo') || getVal('cargo');
        const servicio = getVal('contacto-servicio') || getVal('servicio');
        const tarifa = getVal('contacto-tarifa') || getVal('tarifa');
        const maquinas = getVal('contacto-maquinas') || getVal('maquinas');
        let comment = getVal('contacto-comentario') || getVal('comentario') || getVal('comment');

        /** @type {string[]} */
        const extraDetails = [];
        if (cargo) extraDetails.push(`Cargo: ${cargo}`);
        if (servicio) extraDetails.push(`Servicio de interés: ${servicio}`);
        if (tarifa) extraDetails.push(`Tarifa: ${tarifa}`);
        if (maquinas) extraDetails.push(`Máquinas / Variables: ${maquinas}`);
        if (extraDetails.length > 0) {
            comment = comment ? `[${extraDetails.join(' | ')}]\n${comment}` : `[${extraDetails.join(' | ')}]`;
        }

        const fullName = `${getVal('contacto-nombre') || getVal('nombre') || getVal('name')} ${getVal('contacto-apellido') || getVal('apellido')}`.trim()
            || getVal('contacto-nombre') || getVal('nombre') || getVal('name') || 'Contacto Web';

        /** @type {import('../types.js').ContactSubmitPayload} */
        const data = {
            name: fullName,
            comment: comment || 'Consulta desde formulario web',
            email: getVal('contacto-email') || getVal('email') || null,
            phone: getVal('contacto-telefono') || getVal('telefono') || getVal('phone') || null,
            company: getVal('contacto-empresa') || getVal('empresa') || getVal('company') || null,
            geographicLocation: this.form.dataset.localidad || this.form.dataset.industria || getVal('contacto-ubicacion') || getVal('ubicacion') || null,
            createdAt: new Date().toISOString(),
            pageLocation: window.location.href,
            trafficSource: getAttributionSource(),
            gclid: campaignData.gclid || null,
            fbclid: campaignData.fbclid || null,
            utmSource: campaignData.utmSource || null,
            utmMedium: campaignData.utmMedium || null,
            utmCampaign: campaignData.utmCampaign || null,
            leadSource: this.form.dataset.leadSource || 'formulario_contacto',
            website_url_hp: getVal('website_url_hp') || null
        };
        return data;
    }

    /**
     * Envía de forma asíncrona los datos del lead al backend mediante fetch POST.
     * Notifica conversiones a GA4 y Google Ads tras una respuesta satisfactoria.
     *
     * @returns {Promise<void>}
     */
    async submitForm() {
        const payload = this.collectData();

        const submitBtn = this.nextBtn;
        const originalBtnText = submitBtn ? submitBtn.textContent : this.finalCtaText;

        try {
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.textContent = 'Enviando...';
            }
            if (this.prevBtn) {
                this.prevBtn.disabled = true;
            }

            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (response.ok) {
                logInfo('[FormManager] Formulario enviado con éxito.');
                this.form.innerHTML = '<div class="tw:p-6 tw:bg-dm-surface tw:border tw:border-green-500/30 tw:rounded-xl tw:text-center"><p class="tw:text-green-400 tw:font-semibold tw:text-lg tw:mb-2">¡Consulta enviada con éxito!</p><p class="tw:text-dm-text-muted tw:text-sm">Agustín Bustos revisará tu consulta y te responderá en menos de 24 hs.</p></div>';

                // GA4: evento de conversión nativo (solo si hay consentimiento de cookies)
                if (typeof window.gtag === 'function') {
                    window.gtag('event', 'generate_lead', {
                        event_category: 'lead',
                        lead_source: 'formulario_contacto',
                        transport_type: 'beacon'
                    });
                }

                if (window.dataLayer && typeof window.dataLayer.push === 'function') {
                    window.dataLayer.push({
                        event: 'generate_lead',
                        lead_source: 'formulario_contacto'
                    });
                }

                // Microsoft Clarity: Indexación personalizada para filtrar sesiones de alta intención
                if (typeof window.clarity === 'function') {
                    try {
                        window.clarity('set', 'lead_intent', 'form_submit');
                        window.clarity('set', 'lead_status', 'submitted');
                    } catch (_) {}
                }

                // Google Ads: evento de conversión (requiere GOOGLE_ADS_CONVERSION_ID en consola)
                if (window.APP_CONFIG?.googleAdsConversionId
                    && window.APP_CONFIG.googleAdsConversionId !== "None"
                    && typeof window.gtag === 'function') {
                    window.gtag('event', 'conversion', {
                        send_to: window.APP_CONFIG.googleAdsConversionId
                    });
                }
            } else {
                throw new Error(`Error del servidor: ${response.status}`);
            }
        } catch (error) {
            logError('[FormManager] Error al enviar formulario:', error);
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = originalBtnText;
            }
            if (this.prevBtn) {
                this.prevBtn.disabled = false;
            }
            let errorMsg = this.form.querySelector('.c-contact__error-msg');
            if (!errorMsg) {
                errorMsg = document.createElement('p');
                errorMsg.className = 'c-contact__error-msg tw:text-red-400 tw:text-sm tw:mt-3 tw:text-center';
                this.form.querySelector('.c-contact__actions')?.appendChild(errorMsg);
            }
            errorMsg.textContent = 'Hubo un inconveniente al enviar la consulta. Podés escribirnos directo por WhatsApp al +54 11 5629 7160.';
        }
    }
}