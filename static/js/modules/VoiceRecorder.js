/**
 * @fileoverview Grabación de notas de voz con MediaRecorder (FE 4.3, issue #147).
 * No depende del DOM del widget: el navegador se inyecta, así que se prueba con
 * `node --test` usando dobles de getUserMedia y MediaRecorder.
 */

/** @typedef {'permisoDenegado' | 'sinMicrofono' | 'noDisponible'} GrabacionErrorTipo */

/** Formatos en orden de preferencia; todos los acepta el contrato del Epic #144. */
export const FORMATOS_PREFERIDOS = ['audio/webm;codecs=opus', 'audio/ogg;codecs=opus', 'audio/webm', 'audio/ogg'];
/** Cada cuánto se avisa la duración transcurrida (ms). */
const INTERVALO_TICK = 250;

export class GrabacionError extends Error {
    /** @param {GrabacionErrorTipo} tipo */
    constructor(tipo) {
        super(tipo);
        this.name = 'GrabacionError';
        /** @type {GrabacionErrorTipo} */
        this.tipo = tipo;
    }
}

/**
 * @typedef {Object} EntornoDeGrabacion
 * @property {Pick<MediaDevices, 'getUserMedia'> | undefined} mediaDevices
 * @property {(typeof MediaRecorder) | undefined} MediaRecorder
 * @property {{ allowsFeature?: (caracteristica: string) => boolean } | undefined} [politicaDePermisos]
 *   `document.permissionsPolicy` (o `featurePolicy`), si el navegador la expone.
 */

/** @returns {EntornoDeGrabacion} */
export function entornoDelNavegador() {
    const documento = /** @type {Record<string, any> | undefined} */ (globalThis.document);
    return {
        mediaDevices: globalThis.navigator?.mediaDevices,
        MediaRecorder: globalThis.MediaRecorder,
        politicaDePermisos: documento?.permissionsPolicy ?? documento?.featurePolicy,
    };
}

/**
 * Indica si se puede grabar: hay MediaRecorder y getUserMedia, y la cabecera
 * Permissions-Policy del sitio no bloquea el micrófono.
 * @param {EntornoDeGrabacion} [entorno]
 * @returns {boolean}
 */
export function grabacionDisponible(entorno = entornoDelNavegador()) {
    if (!entorno.MediaRecorder || typeof entorno.mediaDevices?.getUserMedia !== 'function') {
        return false;
    }
    const politica = entorno.politicaDePermisos;
    return typeof politica?.allowsFeature !== 'function' || politica.allowsFeature('microphone');
}

/**
 * @param {(tipo: string) => boolean} soporta - `MediaRecorder.isTypeSupported`.
 * @returns {string} El primer formato preferido que el navegador soporta, o '' para el suyo por defecto.
 */
export function elegirFormato(soporta) {
    return FORMATOS_PREFERIDOS.find((tipo) => soporta(tipo)) ?? '';
}

/**
 * @param {unknown} error - Lo que rechaza getUserMedia.
 * @returns {GrabacionErrorTipo}
 */
function tipoDeError(error) {
    const nombre = error instanceof Error || (typeof error === 'object' && error !== null)
        ? /** @type {{ name?: string }} */ (error).name
        : undefined;
    if (nombre === 'NotAllowedError' || nombre === 'SecurityError') {
        return 'permisoDenegado';
    }
    if (nombre === 'NotFoundError' || nombre === 'OverconstrainedError') {
        return 'sinMicrofono';
    }
    return 'noDisponible';
}

/**
 * @typedef {Object} OpcionesDeGrabacion
 * @property {number} duracionMaximaMs - Al llegar, la grabación se detiene sola.
 * @property {(transcurridoMs: number) => void} [alAvanzar] - Para mostrar el contador.
 * @property {() => void} [alLlegarAlLimite]
 * @property {EntornoDeGrabacion} [entorno]
 */

export class GrabadorDeVoz {
    /** @type {OpcionesDeGrabacion} */
    #opciones;
    /** @type {MediaRecorder | null} */
    #grabador = null;
    /** @type {MediaStream | null} */
    #flujo = null;
    /** @type {Blob[]} */
    #partes = [];
    /** @type {ReturnType<typeof setInterval> | null} */
    #tick = null;
    /** @type {number} */
    #inicio = 0;

    /** @param {OpcionesDeGrabacion} opciones */
    constructor(opciones) {
        this.#opciones = opciones;
    }

    /** @returns {boolean} */
    get grabando() {
        return this.#grabador !== null && this.#grabador.state === 'recording';
    }

    /**
     * Pide el micrófono y empieza a grabar.
     * @returns {Promise<void>}
     */
    async iniciar() {
        const entorno = this.#opciones.entorno ?? entornoDelNavegador();
        if (!grabacionDisponible(entorno) || !entorno.MediaRecorder || !entorno.mediaDevices) {
            throw new GrabacionError('noDisponible');
        }
        try {
            this.#flujo = await entorno.mediaDevices.getUserMedia({ audio: true });
        } catch (error) {
            throw new GrabacionError(tipoDeError(error));
        }
        const Grabador = entorno.MediaRecorder;
        const formato = elegirFormato((tipo) => Grabador.isTypeSupported(tipo));
        this.#grabador = formato ? new Grabador(this.#flujo, { mimeType: formato }) : new Grabador(this.#flujo);
        this.#partes = [];
        this.#grabador.addEventListener('dataavailable', (evento) => {
            if (evento.data && evento.data.size > 0) {
                this.#partes.push(evento.data);
            }
        });
        this.#grabador.start(INTERVALO_TICK);
        this.#inicio = Date.now();
        this.#tick = setInterval(() => this.#avanzar(), INTERVALO_TICK);
    }

    /**
     * Detiene la grabación y devuelve el audio.
     * @returns {Promise<Blob>} Blob vacío si no se grabó nada.
     */
    async detener() {
        const grabador = this.#grabador;
        if (!grabador) {
            return new Blob([]);
        }
        const tipo = grabador.mimeType;
        if (grabador.state !== 'inactive') {
            await new Promise((resolver) => {
                grabador.addEventListener('stop', resolver, { once: true });
                grabador.stop();
            });
        }
        const audio = new Blob(this.#partes, tipo ? { type: tipo } : {});
        this.#liberar();
        return audio;
    }

    /** Descarta la grabación en curso. */
    cancelar() {
        if (this.#grabador && this.#grabador.state !== 'inactive') {
            this.#grabador.stop();
        }
        this.#liberar();
    }

    #avanzar() {
        const transcurrido = Date.now() - this.#inicio;
        this.#opciones.alAvanzar?.(transcurrido);
        if (transcurrido >= this.#opciones.duracionMaximaMs) {
            this.#detenerTick();
            this.#opciones.alLlegarAlLimite?.();
        }
    }

    #detenerTick() {
        if (this.#tick !== null) {
            clearInterval(this.#tick);
            this.#tick = null;
        }
    }

    /** Apaga el micrófono (el navegador deja de mostrar el indicador de grabación). */
    #liberar() {
        this.#detenerTick();
        this.#flujo?.getTracks().forEach((pista) => pista.stop());
        this.#flujo = null;
        this.#grabador = null;
        this.#partes = [];
    }
}
