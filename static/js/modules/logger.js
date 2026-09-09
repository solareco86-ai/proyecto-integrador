/**
 * @fileoverview Módulo de logging con gating por entorno.
 * Silencia los niveles verbosos (debug/info) en producción y preserva la señal
 * de diagnóstico (warn/error) en todos los entornos, manteniendo la consola del
 * navegador limpia de ruido propio sin perder visibilidad de fallos reales.
 */

/**
 * Determina si el entorno está en modo debug según la configuración inyectada.
 * Degradación segura: ante la ausencia de `window.APP_CONFIG` se asume producción.
 *
 * @returns {boolean} Verdadero solo si `APP_CONFIG.debug` está explícitamente activo.
 */
const isDebugEnabled = () => {
    try {
        return window.APP_CONFIG?.debug === true;
    } catch {
        return false;
    }
};

/**
 * @typedef {(...args: any[]) => void} LogFn
 * @description Función de logging compatible con la firma de los métodos de `console`.
 */

/**
 * Registro de nivel `debug` (solo visible en entornos de desarrollo).
 * @type {LogFn}
 * @returns {void}
 */
export const debug = (...args) => {
    if (isDebugEnabled()) {
        console.debug(...args);
    }
};

/**
 * Registro de nivel `info` (solo visible en entornos de desarrollo).
 * @type {LogFn}
 * @returns {void}
 */
export const info = (...args) => {
    if (isDebugEnabled()) {
        console.info(...args);
    }
};

/**
 * Registro de nivel `warn` (diagnóstico: siempre visible).
 * @type {LogFn}
 * @returns {void}
 */
export const warn = (...args) => {
    console.warn(...args);
};

/**
 * Registro de nivel `error` (diagnóstico crítico: siempre visible).
 * @type {LogFn}
 * @returns {void}
 */
export const error = (...args) => {
    console.error(...args);
};
