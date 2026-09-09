/**
 * @fileoverview Módulo de Gestión de Consentimiento de Cookies (GDPR / LGPD / Fail-Closed).
 * Controla el banner de cookies, persiste la decisión del usuario en localStorage
 * y dispara la carga diferida de scripts de terceros (GA4, Ads, Clarity).
 */

import { error as logError } from './logger.js';

/**
 * @callback ScriptLoaderCallback
 * Función callback para inicializar la carga de scripts de analítica y marketing.
 * @returns {void}
 */

/**
 * Inicializa el banner y los botones de consentimiento de cookies.
 *
 * @param {HTMLElement | null} bannerElement - Elemento contenedor del banner en el DOM.
 * @param {HTMLElement | null} acceptBtn - Botón para aceptar todas las cookies.
 * @param {HTMLElement | null} rejectBtn - Botón para rechazar cookies de terceros.
 * @param {ScriptLoaderCallback} loadScripts - Callback que ejecuta la carga de scripts al obtener consentimiento.
 * @returns {void}
 */
export const initCookieManager = (bannerElement, acceptBtn, rejectBtn, loadScripts) => {
    try {
        if (!bannerElement || !acceptBtn || !rejectBtn) {
            return;
        }

        const consent = localStorage.getItem('userConsent');
        
        if (consent === 'accepted') {
            loadScripts();
        } else if (consent === null) {
            bannerElement.classList.add('is-visible');
            document.body.classList.add('has-consent-banner');
        }

        acceptBtn.addEventListener('click', () => {
            localStorage.setItem('userConsent', 'accepted');
            bannerElement.classList.remove('is-visible');
            document.body.classList.remove('has-consent-banner');
            loadScripts();
        });

        rejectBtn.addEventListener('click', () => {
            localStorage.setItem('userConsent', 'rejected');
            bannerElement.classList.remove('is-visible');
            document.body.classList.remove('has-consent-banner');
        });
    } catch (error) {
        logError("[CookieManager] Error accediendo a localStorage:", error);
        // Fail-closed: sin consentimiento válido, NO se cargan scripts de terceros.
    }
};

/**
 * Revoca el consentimiento otorgado previamente, eliminando la preferencia de localStorage
 * y recargando la página para garantizar el cese de rastreo.
 *
 * @returns {void}
 */
export const revokeConsent = () => {
    try {
        localStorage.removeItem('userConsent');
        window.location.reload();
    } catch (error) {
        logError("[CookieManager] Error al revocar consentimiento:", error);
    }
};
