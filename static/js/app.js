import { initCookieManager, revokeConsent } from './modules/CookieManager.js';
import { loadThirdPartyScripts } from './modules/ThirdPartyScriptsManager.js';
import { FormManager } from './modules/FormManager.js';
import { CalculatorPowerFactor } from './modules/CalculatorPowerFactor.js';
import { getAttributionSource } from './modules/AttributionTracker.js';
import { captureAndPersistCampaign, updateWhatsAppLinks } from './modules/WhatsAppDynamicMessage.js';
import { initDirectContactTracking } from './modules/DirectContactTracker.js';
import { initEmailProtection } from './modules/EmailProtector.js';
import * as logger from './modules/logger.js';

/**
 * @fileoverview Punto de entrada principal y orquestador del frontend de DataMaq.
 * Coordina la inicialización de cookies, tracking analítico, formulario de contacto,
 * calculadora de factor de potencia, telemetría de contacto directo, atribución SEM y enlaces de WhatsApp.
 */

/**
 * Configuración global de la aplicación cliente.
 * @type {import('./types.js').AppConfig}
 */
export const APP_CONFIG = {
    apiUrl: window.APP_CONFIG?.contactApiUrl || '',
};

document.addEventListener("DOMContentLoaded", () => {
    // 0. Actualización dinámica de enlaces de WhatsApp según campañas SEM (UTMs)
    try {
        updateWhatsAppLinks();
    } catch (e) {
        logger.error("[App] Fallo al actualizar enlaces dinámicos de WhatsApp:", e);
    }

    // 1. Cookies y consentimiento (Fail-closed)
    try {
        initCookieManager(
            document.getElementById('cookie-banner'),
            document.getElementById('accept-cookies'),
            document.getElementById('reject-cookies'),
            loadThirdPartyScripts
        );
    } catch (e) {
        logger.error("[App] Fallo crítico al inicializar CookieManager:", e);
    }

    // 1b. Revocación de consentimiento desde el footer
    try {
        const manageConsentBtn = document.getElementById('manage-consent');
        if (manageConsentBtn) {
            manageConsentBtn.addEventListener('click', revokeConsent);
        }
    } catch (e) {
        logger.error("[App] Fallo al enlazar la revocación de consentimiento:", e);
    }

    // 2. Contact Form Manager (Multi-paso y Single-step)
    try {
        /** @type {NodeListOf<HTMLFormElement>} */
        const contactForms = document.querySelectorAll('.c-contact form, form[data-component="contact-form"]');
        contactForms.forEach((form) => {
            if (APP_CONFIG.apiUrl) {
                new FormManager(form, APP_CONFIG.apiUrl);
            }
        });
    } catch (e) {
        logger.error("[App] Fallo crítico al inicializar FormManager:", e);
    }

    // 2b. Calculadora de Compensación Reactiva (Landings)
    try {
        /** @type {NodeListOf<HTMLElement>} */
        const calcContainers = document.querySelectorAll('.c-calculator, [data-component="power-factor-calculator"]');
        calcContainers.forEach((container) => {
            new CalculatorPowerFactor(container);
        });
    } catch (e) {
        logger.error("[App] Fallo al inicializar CalculatorPowerFactor:", e);
    }

    // 2c. Enriquecimiento de sesión en Microsoft Clarity para landings técnicas
    if (typeof window.clarity === 'function') {
        try {
            if (window.location.pathname.includes('/landing/calidad-energia')) {
                window.clarity('set', 'landing_viewed', 'calidad_energia');
                window.clarity('set', 'service_viewed', 'calidad_energia');
            } else if (window.location.pathname.includes('/landing/telemetria-industrial')) {
                window.clarity('set', 'landing_viewed', 'telemetria_industrial');
                window.clarity('set', 'service_viewed', 'telemetria_industrial');
            }
        } catch (_) {}
    }

    // 3a. Protección anti-scraping de correos electrónicos
    try {
        initEmailProtection();
    } catch (e) {
        logger.error("[App] Fallo al inicializar EmailProtector:", e);
    }

    // 3b. Telemetría de Contacto Directo (clics en mailto:, tel: y copias de email/teléfono)
    try {
        initDirectContactTracking();
    } catch (e) {
        logger.error("[App] Fallo crítico al inicializar DirectContactTracker:", e);
    }

    // 4. Tracking & Notificaciones WhatsApp (GA4, Google Ads y Notificación Backend a Telegram)
    try {
        /** @type {NodeListOf<HTMLAnchorElement>} */
        const whatsappElements = document.querySelectorAll('a[href*="wa.me"], .c-whatsapp-fab');
        whatsappElements.forEach((el) => {
            el.addEventListener('click', () => {
                // Determinar el botón / elemento específico presionado
                let elementName = 'Botón WhatsApp';
                if (el.classList.contains('c-whatsapp-fab') || el.closest('.c-whatsapp-fab')) {
                    elementName = 'Botón Flotante (FAB)';
                } else if (el.closest('.c-hero') || el.closest('.hero') || el.closest('[data-section="hero"]')) {
                    elementName = 'Hero CTA (Portada / Encabezado)';
                } else if (el.closest('.c-contact') || window.location.pathname.includes('/contact')) {
                    elementName = 'Página de Contacto';
                } else if (el.closest('footer')) {
                    elementName = 'Footer';
                } else if (el.getAttribute('aria-label')) {
                    elementName = el.getAttribute('aria-label') || 'Botón WhatsApp';
                }

                // GA4: Disparo nativo de evento de interacción
                if (typeof window.gtag === 'function') {
                    window.gtag('event', 'whatsapp_click', {
                        event_category: 'engagement',
                        event_label: elementName,
                        page_location: window.location.href,
                        transport_type: 'beacon'
                    });
                }

                if (window.dataLayer && typeof window.dataLayer.push === 'function') {
                    window.dataLayer.push({
                        event: 'whatsapp_click'
                    });
                }

                // Microsoft Clarity: Indexación personalizada para filtrar sesiones de alta intención
                if (typeof window.clarity === 'function') {
                    try {
                        window.clarity('set', 'lead_intent', 'whatsapp_click');
                    } catch (_) {}
                }

                // Google Ads: conversión de WhatsApp
                if (window.APP_CONFIG?.googleAdsWhatsappConversionId
                    && window.APP_CONFIG.googleAdsWhatsappConversionId !== "None"
                    && typeof window.gtag === 'function') {
                    window.gtag('event', 'conversion', {
                        send_to: window.APP_CONFIG.googleAdsWhatsappConversionId
                    });
                }

                // Notificación instantánea a Backend / Telegram con Atribución y Consentimiento
                const attribution = getAttributionSource();
                const consent = localStorage.getItem('userConsent') || 'pending';
                const campaignData = captureAndPersistCampaign();

                /** @type {import('./types.js').WhatsAppClickPayload} */
                const payloadObj = {
                    pageLocation: window.location.href,
                    trafficSource: attribution,
                    element: elementName,
                    cookieConsent: consent,
                    utmSource: campaignData?.utmSource || null,
                    utmMedium: campaignData?.utmMedium || null,
                    utmCampaign: campaignData?.utmCampaign || null,
                    gclid: campaignData?.gclid || null
                };
                const payload = JSON.stringify(payloadObj);

                if (navigator.sendBeacon) {
                    navigator.sendBeacon('/api/v1/events/whatsapp-click', new Blob([payload], { type: 'application/json' }));
                } else {
                    fetch('/api/v1/events/whatsapp-click', {
                        method: 'POST',
                        body: payload,
                        headers: { 'Content-Type': 'application/json' },
                        keepalive: true
                    }).catch(() => {});
                }
            });
        });
    } catch (e) {
        logger.error("[App] Fallo crítico al inicializar tracking WhatsApp:", e);
    }
});
