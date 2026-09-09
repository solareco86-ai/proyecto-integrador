/**
 * @fileoverview Módulo de Carga Asíncrona y Segura de Scripts de Terceros.
 * Inyecta Google Tag Manager (gtag.js / GA4 / Google Ads) y Microsoft Clarity
 * exclusivamente tras el consentimiento explícito del usuario.
 */

import { debug, warn } from './logger.js';

/**
 * Registro en memoria de vendors ya advertidos durante la página actual.
 * Fallback de dedupe cuando `sessionStorage` no está disponible (modo privado).
 * @type {Record<string, boolean>}
 */
const warnedInMemory = {};

/**
 * Clave de sesión para el dedupe de avisos por vendor.
 * @param {string} vendor - Identificador del vendor ('gtag' | 'clarity').
 * @returns {string} Clave de sessionStorage normalizada.
 */
const sessionKeyFor = (vendor) => `tp:warned:${vendor}`;

/**
 * Indica si el vendor ya fue advertido en la sesión actual.
 * @param {string} vendor - Identificador del vendor ('gtag' | 'clarity').
 * @returns {boolean} Verdadero si ya se emitió un aviso para este vendor.
 */
const hasVendorWarned = (vendor) => {
    if (warnedInMemory[vendor]) {
        return true;
    }
    try {
        if (sessionStorage.getItem(sessionKeyFor(vendor)) === '1') {
            return true;
        }
    } catch {
        return warnedInMemory[vendor] === true;
    }
    return false;
};

/**
 * Marca al vendor como ya advertido en la sesión actual.
 * @param {string} vendor - Identificador del vendor ('gtag' | 'clarity').
 * @returns {void}
 */
const markVendorWarned = (vendor) => {
    warnedInMemory[vendor] = true;
    try {
        sessionStorage.setItem(sessionKeyFor(vendor), '1');
    } catch {
        // Sin sessionStorage: el dedupe queda limitado a la página actual.
    }
};

/**
 * Registra el fallo de carga de un script de terceros.
 * Emite el aviso una única vez por sesión y despacha el evento de telemetría.
 *
 * @param {string} vendor - Identificador del vendor ('gtag' | 'clarity').
 * @param {string} label - Descripción legible del fallo para el aviso de consola.
 * @returns {void}
 */
const reportVendorFailure = (vendor, label) => {
    if (!hasVendorWarned(vendor)) {
        warn(`[ThirdPartyManager] ${label}`);
        markVendorWarned(vendor);
    }
    try {
        window.dispatchEvent(new CustomEvent('tp:blocked', { detail: { vendor } }));
    } catch {
        // Sin soporte de CustomEvent: la telemetría no puede despacharse.
    }
};

/**
 * Notifica el bloqueo de un script de terceros al dataLayer para su medición en GA4/GTM.
 * @returns {void}
 */
const attachBlockedListener = () => {
    window.addEventListener('tp:blocked', (event) => {
        const detail = /** @type {CustomEvent<{vendor?: string}>} */ (event).detail;
        const vendor = detail && detail.vendor ? detail.vendor : 'unknown';
        if (window.dataLayer && typeof window.dataLayer.push === 'function') {
            try {
                window.dataLayer.push({
                    event: 'third_party_blocked',
                    third_party_vendor: vendor,
                });
            } catch {
                // dataLayer no disponible: la métrica no puede registrarse.
            }
        }
    });
};

// Registro único del listener de telemetría de bloqueo (idempotente por módulo).
attachBlockedListener();

/**
 * Carga de forma asíncrona los scripts de seguimiento autorizados.
 * Inicializa los shims globales de `dataLayer` y `gtag` para evitar excepciones de runtime.
 *
 * @returns {void}
 */

export const loadThirdPartyScripts = () => {
    try {
        const gaId = window.APP_CONFIG?.gaId;
        const adsId = window.APP_CONFIG?.googleAdsId;
        const clarityId = window.APP_CONFIG?.clarityId;

        const hasGtag = (gaId && gaId !== "None") || (adsId && adsId !== "None");

        // Shim global: dataLayer + gtag always available after consent
        window.dataLayer = window.dataLayer || [];
        window.gtag = window.gtag || function () { window.dataLayer.push(arguments); };

        // 1. Google Analytics + Google Ads (single gtag.js script)
        if (hasGtag) {
            try {
                const primaryId = (gaId && gaId !== "None") ? gaId : adsId;
                const script = document.createElement("script");
                script.async = true;
                script.src = "https://www.googletagmanager.com/gtag/js?id=" + primaryId;
                script.crossOrigin = "anonymous";
                script.onerror = () => reportVendorFailure('gtag', 'Error de red al cargar GTAG.');
                document.head.appendChild(script);
                debug("[ThirdPartyManager] GTAG script added", { src: script.src });
            } catch (e) {
                warn("[ThirdPartyManager] Exception while loading GTAG", e);
            }
            // Initialize gtag after script insertion
            window.gtag("js", new Date());
            const gtagOptions = {
                cookie_domain: "auto",
                cookie_flags: "SameSite=Lax;Secure",
            };
            if (gaId && gaId !== "None") window.gtag("config", gaId, gtagOptions);
            if (adsId && adsId !== "None") window.gtag("config", adsId, gtagOptions);
        }

        // 2. Load Microsoft Clarity
        if (clarityId && clarityId !== "None") {
            try {
                (function (c, l, a, r, i, t, y) {
                    c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
                    t = l.createElement(r);
                    t.async = 1;
                    t.src = "https://www.clarity.ms/tag/" + i;
                    t.crossOrigin = "anonymous";
                    t.onerror = () => reportVendorFailure('clarity', 'Error de red al cargar Clarity.');
                    y = l.getElementsByTagName(r)[0];
                    y.parentNode.insertBefore(t, y);
                })(window, document, "clarity", "script", clarityId);
            } catch (e) {
                warn("[ThirdPartyManager] Fallo crítico al inicializar Clarity:", e);
            }
        }
    } catch (e) {
        warn("[ThirdPartyManager] Error inesperado en el flujo de carga:", e);
    }
};
