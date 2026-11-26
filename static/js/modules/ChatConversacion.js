/**
 * @fileoverview Estado de la conversación del widget (FE 4.2, issue #146).
 * Guarda el identificador de sesión y el historial en sessionStorage para que la
 * conversación siga al navegar entre páginas, y decide qué fuentes se pueden
 * mostrar como enlace. No depende del DOM: se prueba con `node --test`.
 */

/** @typedef {'usuario' | 'bot'} ChatAutor */

/**
 * @typedef {Object} ChatMensaje
 * @property {ChatAutor} autor
 * @property {string} texto
 * @property {string[]} [fuentes] - Rutas o URLs de donde sale una respuesta del bot.
 * @property {boolean} [voz] - El usuario la envió como nota de voz; `texto` es la transcripción.
 */

/** @typedef {Pick<Storage, 'getItem' | 'setItem'>} AlmacenamientoSimple */

export const CLAVE_SESION = 'isft199.chat.sesion';
export const CLAVE_HISTORIAL = 'isft199.chat.historial';
/** Cantidad máxima de mensajes que se conservan entre páginas. */
export const MAXIMO_MENSAJES = 50;

/**
 * sessionStorage puede no existir o lanzar error (modo privado, sitio bloqueado).
 * @returns {AlmacenamientoSimple | null}
 */
export function obtenerAlmacenamientoDeSesion() {
    try {
        return globalThis.sessionStorage ?? null;
    } catch (_) {
        return null;
    }
}

/** @returns {string} Identificador aleatorio para el `session_id` del contrato. */
export function generarIdSesion() {
    const cripto = globalThis.crypto;
    if (cripto && typeof cripto.randomUUID === 'function') {
        return cripto.randomUUID();
    }
    return `s-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 12)}`;
}

/**
 * Devuelve la URL de una fuente si se puede mostrar como enlace: una ruta del
 * propio sitio (`/carreras`) o una URL `https:`. Cualquier otro esquema
 * (`javascript:`, `data:`, `//otro-sitio`) se descarta.
 * @param {unknown} fuente
 * @returns {string | null}
 */
export function urlDeFuenteSegura(fuente) {
    if (typeof fuente !== 'string') {
        return null;
    }
    const valor = fuente.trim();
    if (valor.startsWith('/') && !valor.startsWith('//') && !valor.includes('\\')) {
        return valor;
    }
    try {
        const url = new URL(valor);
        return url.protocol === 'https:' ? url.href : null;
    } catch (_) {
        return null;
    }
}

/**
 * @param {unknown} valor
 * @returns {valor is ChatMensaje}
 */
function esMensajeValido(valor) {
    if (typeof valor !== 'object' || valor === null) {
        return false;
    }
    const m = /** @type {Record<string, unknown>} */ (valor);
    const fuentesValidas = m.fuentes === undefined
        || (Array.isArray(m.fuentes) && m.fuentes.every((f) => typeof f === 'string'));
    const vozValida = m.voz === undefined || typeof m.voz === 'boolean';
    return (m.autor === 'usuario' || m.autor === 'bot') && typeof m.texto === 'string' && fuentesValidas && vozValida;
}

export class ChatConversacion {
    /** @type {AlmacenamientoSimple | null} */
    #almacenamiento;

    /** @type {string} */
    #sessionId;

    /** @type {ChatMensaje[]} */
    #mensajes;

    /**
     * @param {AlmacenamientoSimple | null} almacenamiento - null si no hay sessionStorage.
     * @param {() => string} [generarId]
     */
    constructor(almacenamiento, generarId = generarIdSesion) {
        this.#almacenamiento = almacenamiento;
        this.#sessionId = this.#leer(CLAVE_SESION) || generarId();
        this.#escribir(CLAVE_SESION, this.#sessionId);
        this.#mensajes = this.#leerHistorial();
    }

    /** @returns {string} */
    get sessionId() {
        return this.#sessionId;
    }

    /** @returns {ChatMensaje[]} Copia del historial, del más viejo al más nuevo. */
    get mensajes() {
        return this.#mensajes.map((m) => ({ ...m }));
    }

    /**
     * Agrega un mensaje y guarda el historial (solo los últimos MAXIMO_MENSAJES).
     * @param {ChatMensaje} mensaje
     */
    agregar(mensaje) {
        this.#mensajes = [...this.#mensajes, { ...mensaje }].slice(-MAXIMO_MENSAJES);
        this.#escribir(CLAVE_HISTORIAL, JSON.stringify(this.#mensajes));
    }

    /** @returns {ChatMensaje[]} */
    #leerHistorial() {
        const crudo = this.#leer(CLAVE_HISTORIAL);
        if (!crudo) {
            return [];
        }
        try {
            const datos = JSON.parse(crudo);
            return Array.isArray(datos) ? datos.filter(esMensajeValido).slice(-MAXIMO_MENSAJES) : [];
        } catch (_) {
            return [];
        }
    }

    /**
     * @param {string} clave
     * @returns {string | null}
     */
    #leer(clave) {
        try {
            return this.#almacenamiento ? this.#almacenamiento.getItem(clave) : null;
        } catch (_) {
            return null;
        }
    }

    /**
     * @param {string} clave
     * @param {string} valor
     */
    #escribir(clave, valor) {
        try {
            this.#almacenamiento?.setItem(clave, valor);
        } catch (_) {
            // Sin almacenamiento la conversación funciona igual, pero no sigue entre páginas.
        }
    }
}
