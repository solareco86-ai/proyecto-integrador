/**
 * @fileoverview Módulo de Protección Anti-Scraping para Enlaces de Correo Electrónico.
 * Reconstituye dinámicamente las direcciones de correo a partir de data-attributes (data-u y data-d)
 * en tiempo de ejecución del navegador, evitando que crawlers y spambots cosechen correos en texto plano.
 */

import { error as logError } from './logger.js';

/**
 * Inicializa la protección y ensamblado dinámico de correos en el DOM.
 * @returns {void}
 */
export function initEmailProtection() {
    try {
        /** @type {NodeListOf<HTMLAnchorElement>} */
        const protectedElements = document.querySelectorAll('.js-email-protect');
        protectedElements.forEach((el) => {
            const u = el.getAttribute('data-u');
            const d = el.getAttribute('data-d');
            if (u && d) {
                const email = `${u}@${d}`;
                el.setAttribute('href', `mailto:${email}`);
                const displaySpan = el.querySelector('.js-email-display');
                if (displaySpan) {
                    displaySpan.textContent = email;
                }
            }
        });
    } catch (e) {
        logError('[EmailProtector] Error al inicializar protección de email:', e);
    }
}
