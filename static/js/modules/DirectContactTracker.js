import { getAttributionSource } from './AttributionTracker.js';
import { captureAndPersistCampaign } from './WhatsAppDynamicMessage.js';
import { debug as logDebug, warn as logWarn, error as logError } from './logger.js';

/**
 * @fileoverview Módulo de Telemetría para Contacto Directo (Email y Teléfono).
 * Captura clics en enlaces `mailto:` y `tel:`, así como eventos de copia al portapapeles
 * de los datos de contacto corporativo de DataMaq, garantizando atribución y alerta en tiempo real.
 */

/**
 * Timestamp del último evento de copia enviado para evitar ráfagas o duplicados.
 * @type {number}
 */
let lastCopyEventTime = 0;

/**
 * Cooldown mínimo entre eventos de copia idénticos (milisegundos).
 * @type {number}
 */
const COPY_DEBOUNCE_MS = 3000;

/**
 * Emite la baliza first-party y notifica a analítica ante una interacción con datos de contacto.
 *
 * @param {import('../types.js').DirectContactAction} action - Tipo de acción ('email_click', 'email_copy', 'phone_click', 'phone_copy').
 * @param {string} targetValue - Correo o teléfono objetivo.
 * @param {string} elementName - Identificador descriptivo del elemento en el DOM.
 * @returns {void}
 */
export function sendDirectContactTelemetry(action, targetValue, elementName) {
    const attribution = getAttributionSource();
    const consent = localStorage.getItem('userConsent') || 'pending';
    const campaignData = captureAndPersistCampaign();

    /** @type {import('../types.js').DirectContactPayload} */
    const payloadObj = {
        action,
        targetValue,
        pageLocation: window.location.href,
        trafficSource: attribution,
        element: elementName,
        cookieConsent: consent,
        utmSource: campaignData?.utmSource || null,
        utmMedium: campaignData?.utmMedium || null,
        utmCampaign: campaignData?.utmCampaign || null,
        gclid: campaignData?.gclid || null,
    };

    // 1. GA4: Disparo nativo si hay consentimiento otorgado
    if (typeof window.gtag === 'function') {
        try {
            window.gtag('event', 'direct_contact', {
                contact_action: action,
                contact_target: targetValue,
                event_category: 'engagement',
                page_location: window.location.href,
                transport_type: 'beacon'
            });
        } catch (_) {}
    }

    if (window.dataLayer && typeof window.dataLayer.push === 'function') {
        try {
            window.dataLayer.push({
                event: 'direct_contact',
                contact_action: action,
                contact_target: targetValue
            });
        } catch (_) {}
    }

    // 2. Microsoft Clarity: Indexación personalizada para filtrar sesiones de alta intención
    if (typeof window.clarity === 'function') {
        try {
            window.clarity('set', 'lead_intent', action);
            window.clarity('set', 'traffic_source', attribution);
        } catch (_) {}
    }

    // 3. Telemetría First-Party: Envío directo a FastAPI backend -> Telegram & MySQL
    const payload = JSON.stringify(payloadObj);
    try {
        logDebug('[DirectContactTracker] Enviando payload', payloadObj);
        if (navigator.sendBeacon) {
            navigator.sendBeacon('/api/v1/events/direct-contact', new Blob([payload], { type: 'application/json' }));
        } else {
            fetch('/api/v1/events/direct-contact', {
                method: 'POST',
                body: payload,
                headers: { 'Content-Type': 'application/json' },
                keepalive: true,
            }).catch(() => {});
        }
    } catch (e) {
        logWarn('[DirectContactTracker] Error al enviar telemetría', e);
    }
}

/**
 * Inicializa los listeners de eventos para clics en mailto:, tel: y copias al portapapeles.
 * @returns {void}
 */
export function initDirectContactTracking() {
    try {
        // A. Interceptar clics en enlaces mailto:
        const mailtoLinks = /** @type {NodeListOf<HTMLAnchorElement>} */ (document.querySelectorAll('a[href^="mailto:"]'));
        mailtoLinks.forEach((link) => {
            link.addEventListener('click', () => {
                const href = link.getAttribute('href') || '';
                const email = href.replace('mailto:', '').split('?')[0].trim() || 'ifst199alumnos@gmail.com';
                const context = link.closest('footer') ? 'Footer' : (link.closest('.c-contact') ? 'Página de Contacto' : 'Enlace Mail');
                sendDirectContactTelemetry('email_click', email, context);
            });
        });

        // B. Interceptar clics en enlaces tel:
        const telLinks = /** @type {NodeListOf<HTMLAnchorElement>} */ (document.querySelectorAll('a[href^="tel:"]'));
        telLinks.forEach((link) => {
            link.addEventListener('click', () => {
                const href = link.getAttribute('href') || '';
                const phone = href.replace('tel:', '').trim() || '+54 11 5629 7160';
                const context = link.closest('footer') ? 'Footer' : (link.closest('.c-contact') ? 'Página de Contacto' : 'Enlace Teléfono');
                sendDirectContactTelemetry('phone_click', phone, context);
            });
        });

        // C. Interceptar copia de texto al portapapeles (email o teléfono del ISFT 199)
        document.addEventListener('copy', () => {
            try {
                const selection = window.getSelection()?.toString().trim().toLowerCase();
                if (!selection) return;

                const now = Date.now();
                if (now - lastCopyEventTime < COPY_DEBOUNCE_MS) return;

                if (selection.includes('ifst199alumnos') || selection.includes('isft199') || selection.includes('datamaq.com.ar') || selection.includes('info@datamaq')) {
                    lastCopyEventTime = now;
                    sendDirectContactTelemetry('email_copy', 'ifst199alumnos@gmail.com', 'Selección y Copia de Texto');
                } else if (selection.includes('56297160') || selection.includes('5629 7160') || selection.includes('5629-7160')) {
                    lastCopyEventTime = now;
                    sendDirectContactTelemetry('phone_copy', '+54 11 5629 7160', 'Selección y Copia de Texto');
                }
            } catch (_) {}
        });
    } catch (e) {
        logError('[DirectContactTracker] Fallo al inicializar tracking de contacto directo:', e);
    }
}
