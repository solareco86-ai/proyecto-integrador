/**
 * @fileoverview Cliente de la API del widget conversacional (FE 4.4, issue #148).
 * Habla con el contrato `/api/v1/chat` del Epic #144 o, en modo mock, simula las
 * respuestas con los textos de data/config/chat_widget.yaml. No contiene textos
 * para el público: ante un problema lanza un ChatApiError con su `tipo`, y el
 * widget muestra el mensaje que corresponde a ese tipo según los datos.
 */

/**
 * @typedef {'timeout' | 'red' | 'servidor' | 'validacion' | 'audioVacio' | 'respuestaInvalida'} ChatErrorTipo
 */

/**
 * @typedef {Object} ChatApiConfig
 * @property {string} baseUrl - Prefijo de las rutas del contrato (por ejemplo `/api/v1/chat`).
 * @property {boolean} mock - Si es true, no se llama al backend y se simulan las respuestas.
 * @property {number} timeoutTextoMs - Tiempo máximo de espera de una consulta escrita.
 * @property {number} timeoutAudioMs - Tiempo máximo de espera de una nota de voz.
 */

/**
 * @typedef {Object} ChatMockConfig
 * @property {string} respuesta - Respuesta simulada; `{mensaje}` se reemplaza por la consulta.
 * @property {string} transcripcion - Transcripción simulada de una nota de voz.
 * @property {string} intencion
 * @property {string[]} fuentes
 * @property {number} confianza
 * @property {number} demoraMs - Demora simulada antes de responder.
 */

/**
 * @typedef {Object} ChatClienteConfig
 * @property {number} longitudMaxima - Largo máximo de una consulta escrita.
 * @property {ChatApiConfig} api
 * @property {Record<ChatErrorTipo, string>} errores - Mensajes para el público, por tipo de error.
 * @property {ChatMockConfig} mock
 */

/**
 * Respuesta del motor conversacional según el contrato del Epic #144.
 * @typedef {Object} ChatRespuesta
 * @property {string} reply
 * @property {string} intent
 * @property {string[]} sources
 * @property {number} confidence
 * @property {string} [transcript] - Solo en las respuestas a notas de voz.
 */

/** Estados HTTP que indican que el problema está en lo que se envió. */
const ESTADOS_DE_VALIDACION = new Set([400, 413, 415, 422]);

export class ChatApiError extends Error {
    /**
     * @param {ChatErrorTipo} tipo
     * @param {number | null} [estado] - Estado HTTP, si hubo respuesta del servidor.
     */
    constructor(tipo, estado = null) {
        super(tipo);
        this.name = 'ChatApiError';
        /** @type {ChatErrorTipo} */
        this.tipo = tipo;
        /** @type {number | null} */
        this.estado = estado;
    }
}

/**
 * Lee la configuración que la plantilla serializa en `<script type="application/json" data-chat-config>`.
 * @param {ParentNode} raiz - Contenedor del widget.
 * @returns {ChatClienteConfig | null} La configuración, o null si falta o no es JSON válido.
 */
export function leerConfiguracion(raiz) {
    const nodo = raiz.querySelector('[data-chat-config]');
    if (!nodo || !nodo.textContent) {
        return null;
    }
    try {
        return /** @type {ChatClienteConfig} */ (JSON.parse(nodo.textContent));
    } catch (_) {
        return null;
    }
}

/**
 * Verifica que los datos recibidos respeten el contrato y devuelve solo los campos conocidos.
 * @param {unknown} datos
 * @param {boolean} conTranscripcion - Si la respuesta debe incluir `transcript` (notas de voz).
 * @returns {ChatRespuesta}
 */
export function validarRespuesta(datos, conTranscripcion) {
    if (typeof datos !== 'object' || datos === null) {
        throw new ChatApiError('respuestaInvalida');
    }
    const d = /** @type {Record<string, unknown>} */ (datos);
    const fuentesValidas = Array.isArray(d.sources) && d.sources.every((f) => typeof f === 'string');
    const valido = typeof d.reply === 'string'
        && typeof d.intent === 'string'
        && fuentesValidas
        && typeof d.confidence === 'number'
        && Number.isFinite(d.confidence)
        && (!conTranscripcion || typeof d.transcript === 'string');
    if (!valido) {
        throw new ChatApiError('respuestaInvalida');
    }
    /** @type {ChatRespuesta} */
    const respuesta = {
        reply: /** @type {string} */ (d.reply),
        intent: /** @type {string} */ (d.intent),
        sources: /** @type {string[]} */ (d.sources),
        confidence: /** @type {number} */ (d.confidence),
    };
    if (conTranscripcion) {
        respuesta.transcript = /** @type {string} */ (d.transcript);
    }
    return respuesta;
}

export class ChatApiClient {
    /** @type {ChatClienteConfig} */
    #config;

    /** @type {typeof fetch} */
    #fetch;

    /**
     * @param {ChatClienteConfig} config
     * @param {typeof fetch} [fetchFn] - Implementación de fetch (inyectable para pruebas).
     */
    constructor(config, fetchFn = (entrada, init) => globalThis.fetch(entrada, init)) {
        this.#config = config;
        this.#fetch = fetchFn;
    }

    /** @returns {boolean} */
    get enModoMock() {
        return this.#config.api.mock;
    }

    /**
     * Envía una consulta escrita (`POST {baseUrl}/text`).
     * @param {string} sessionId
     * @param {string} mensaje
     * @returns {Promise<ChatRespuesta>}
     */
    async enviarTexto(sessionId, mensaje) {
        const texto = mensaje.trim();
        if (!texto || texto.length > this.#config.longitudMaxima) {
            throw new ChatApiError('validacion');
        }
        if (this.#config.api.mock) {
            return this.#simular(texto, false);
        }
        const datos = await this.#pedir('/text', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
            body: JSON.stringify({ session_id: sessionId, message: texto }),
        }, this.#config.api.timeoutTextoMs);
        return validarRespuesta(datos, false);
    }

    /**
     * Envía una nota de voz (`POST {baseUrl}/audio`, multipart).
     * @param {string} sessionId
     * @param {Blob} audio
     * @param {string} [nombreArchivo] - Nombre con la extensión del formato grabado.
     * @returns {Promise<ChatRespuesta>}
     */
    async enviarAudio(sessionId, audio, nombreArchivo = 'nota-de-voz.webm') {
        if (!audio || audio.size === 0) {
            throw new ChatApiError('audioVacio');
        }
        if (this.#config.api.mock) {
            return this.#simular(this.#config.mock.transcripcion, true);
        }
        const formulario = new FormData();
        formulario.append('session_id', sessionId);
        formulario.append('audio', audio, nombreArchivo);
        const datos = await this.#pedir('/audio', {
            method: 'POST',
            headers: { Accept: 'application/json' },
            body: formulario,
        }, this.#config.api.timeoutAudioMs);
        return validarRespuesta(datos, true);
    }

    /**
     * Hace la petición con límite de tiempo y traduce cada falla a un ChatApiError.
     * @param {string} ruta
     * @param {RequestInit} init
     * @param {number} timeoutMs
     * @returns {Promise<unknown>} El cuerpo JSON de la respuesta.
     */
    async #pedir(ruta, init, timeoutMs) {
        const controlador = new AbortController();
        const temporizador = setTimeout(() => controlador.abort(), timeoutMs);
        try {
            /** @type {Response} */
            let respuesta;
            try {
                respuesta = await this.#fetch(this.#url(ruta), { ...init, signal: controlador.signal });
            } catch (_) {
                throw new ChatApiError(controlador.signal.aborted ? 'timeout' : 'red');
            }
            if (ESTADOS_DE_VALIDACION.has(respuesta.status)) {
                throw new ChatApiError('validacion', respuesta.status);
            }
            if (!respuesta.ok) {
                throw new ChatApiError('servidor', respuesta.status);
            }
            try {
                return await respuesta.json();
            } catch (_) {
                throw new ChatApiError(controlador.signal.aborted ? 'timeout' : 'respuestaInvalida', respuesta.status);
            }
        } finally {
            clearTimeout(temporizador);
        }
    }

    /**
     * @param {string} ruta
     * @returns {string}
     */
    #url(ruta) {
        return this.#config.api.baseUrl.replace(/\/+$/, '') + ruta;
    }

    /**
     * Respuesta simulada del modo mock, con la misma forma que el contrato.
     * @param {string} mensaje - Consulta escrita o transcripción simulada.
     * @param {boolean} conTranscripcion
     * @returns {Promise<ChatRespuesta>}
     */
    async #simular(mensaje, conTranscripcion) {
        const mock = this.#config.mock;
        await new Promise((resolver) => setTimeout(resolver, mock.demoraMs));
        /** @type {ChatRespuesta} */
        const respuesta = {
            reply: mock.respuesta.replace('{mensaje}', mensaje),
            intent: mock.intencion,
            sources: [...mock.fuentes],
            confidence: mock.confianza,
        };
        if (conTranscripcion) {
            respuesta.transcript = mock.transcripcion;
        }
        return respuesta;
    }
}
