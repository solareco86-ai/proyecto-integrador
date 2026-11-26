/**
 * @fileoverview Comportamiento del widget conversacional (FE 4.2 y 4.3, issues #146 y #147).
 * Abre y cierra la ventana, envía consultas escritas y notas de voz con
 * ChatApiClient y muestra la conversación. Por seguridad (XSS) todo lo que
 * llega del servidor se inserta con `textContent` y los enlaces de las fuentes
 * pasan por `urlDeFuenteSegura`: en este módulo no se usa `innerHTML`.
 */
import { ChatApiClient, ChatApiError, leerConfiguracion } from './ChatApiClient.js';
import { ChatConversacion, obtenerAlmacenamientoDeSesion, urlDeFuenteSegura } from './ChatConversacion.js';
import { prepararParaEnvio } from './ConversorWav.js';
import { GrabacionError, GrabadorDeVoz, grabacionDisponible } from './VoiceRecorder.js';
import * as logger from './logger.js';

/** @typedef {import('./ChatApiClient.js').ChatClienteConfig} ChatClienteConfig */
/** @typedef {import('./ChatConversacion.js').ChatMensaje} ChatMensaje */

const CLASE_BURBUJA = 'c-chat-widget__bubble';
/** Alto máximo del campo de texto al crecer con el contenido (px). */
const ALTO_MAXIMO_CAMPO = 120;

/**
 * Busca un elemento obligatorio del widget.
 * @template {Element} T
 * @param {ParentNode} raiz
 * @param {string} selector
 * @param {new (...args: any[]) => T} tipo
 * @returns {T}
 */
function requerir(raiz, selector, tipo) {
    const elemento = raiz.querySelector(selector);
    if (!(elemento instanceof tipo)) {
        throw new Error(`[ChatWidget] Falta el elemento ${selector}`);
    }
    return elemento;
}

/**
 * @param {number} ms
 * @returns {string} Duración como `m:ss`.
 */
export function formatearDuracion(ms) {
    const segundos = Math.floor(ms / 1000);
    return `${Math.floor(segundos / 60)}:${String(segundos % 60).padStart(2, '0')}`;
}

export class ChatWidget {
    /**
     * @param {HTMLElement} raiz - Elemento `[data-component="chat-widget"]`.
     * @param {ChatClienteConfig} config
     * @param {ChatApiClient} [cliente]
     * @param {ChatConversacion} [conversacion]
     */
    constructor(raiz, config, cliente = new ChatApiClient(config), conversacion = new ChatConversacion(obtenerAlmacenamientoDeSesion())) {
        this.raiz = raiz;
        this.config = config;
        this.cliente = cliente;
        this.conversacion = conversacion;
        this.boton = requerir(raiz, '[data-chat-toggle]', HTMLButtonElement);
        this.panel = requerir(raiz, '[data-chat-panel]', HTMLElement);
        this.cerrarBoton = requerir(raiz, '[data-chat-close]', HTMLButtonElement);
        this.mensajes = requerir(raiz, '[data-chat-messages]', HTMLElement);
        this.formulario = requerir(raiz, '[data-chat-form]', HTMLFormElement);
        this.campo = requerir(raiz, '[data-chat-input]', HTMLTextAreaElement);
        this.enviarBoton = requerir(raiz, '[data-chat-send]', HTMLButtonElement);
        this.microfono = requerir(raiz, '[data-chat-mic]', HTMLButtonElement);
        this.barraDeGrabacion = requerir(raiz, '[data-chat-recorder]', HTMLElement);
        this.contador = requerir(raiz, '[data-chat-rec-time]', HTMLElement);
        this.cancelarGrabacionBoton = requerir(raiz, '[data-chat-rec-cancel]', HTMLButtonElement);
        this.enviarGrabacionBoton = requerir(raiz, '[data-chat-rec-send]', HTMLButtonElement);
        /** @type {boolean} */
        this.esperando = false;
        /** @type {GrabadorDeVoz | null} */
        this.grabador = null;
        /** @type {number} */
        this.duracionGrabada = 0;

        // Sin MediaRecorder, sin micrófono o con la Permissions-Policy bloqueándolo, solo hay chat de texto.
        this.microfono.hidden = !grabacionDisponible();
        this.conversacion.mensajes.forEach((mensaje) => this.mensajes.append(this.#crearBurbuja(mensaje)));
        this.#enlazarEventos();
    }

    /** @returns {boolean} */
    get abierto() {
        return !this.panel.hidden;
    }

    abrir() {
        this.panel.hidden = false;
        this.raiz.classList.add('is-open');
        this.boton.setAttribute('aria-expanded', 'true');
        this.#desplazarAlFinal();
        this.campo.focus();
    }

    cerrar() {
        if (this.grabador) {
            this.#cancelarGrabacion();
        }
        this.panel.hidden = true;
        this.raiz.classList.remove('is-open');
        this.boton.setAttribute('aria-expanded', 'false');
        this.boton.focus();
    }

    /**
     * Muestra la consulta del usuario y pide la respuesta.
     * @param {string} texto
     * @returns {Promise<void>}
     */
    async enviar(texto) {
        const consulta = texto.trim();
        if (!consulta || this.esperando || this.grabador) {
            return;
        }
        this.#agregar({ autor: 'usuario', texto: consulta });
        this.campo.value = '';
        this.#ajustarAltoCampo();
        await this.#esperarRespuesta(async () => {
            const respuesta = await this.cliente.enviarTexto(this.conversacion.sessionId, consulta);
            this.#agregar({ autor: 'bot', texto: respuesta.reply, fuentes: respuesta.sources });
        });
    }

    #enlazarEventos() {
        this.boton.addEventListener('click', () => this.abrir());
        this.cerrarBoton.addEventListener('click', () => this.cerrar());
        this.raiz.addEventListener('keydown', (evento) => {
            if (evento.key !== 'Escape' || !this.abierto) {
                return;
            }
            evento.preventDefault();
            // Con una grabación en curso, Escape la descarta; si no, cierra la ventana.
            if (this.grabador) {
                this.#cancelarGrabacion();
            } else {
                this.cerrar();
            }
        });
        this.formulario.addEventListener('submit', (evento) => {
            evento.preventDefault();
            void this.enviar(this.campo.value);
        });
        // Enter envía y Shift+Enter agrega un salto de línea, como en WhatsApp.
        this.campo.addEventListener('keydown', (evento) => {
            if (evento.key === 'Enter' && !evento.shiftKey && !evento.isComposing) {
                evento.preventDefault();
                this.formulario.requestSubmit();
            }
        });
        this.campo.addEventListener('input', () => this.#ajustarAltoCampo());
        this.microfono.addEventListener('click', () => void this.#iniciarGrabacion());
        this.cancelarGrabacionBoton.addEventListener('click', () => this.#cancelarGrabacion());
        this.enviarGrabacionBoton.addEventListener('click', () => void this.#enviarGrabacion());
    }

    /**
     * Muestra «escribiendo» mientras se espera al motor; ante un error, ofrece reintentar el mismo pedido.
     * @param {() => Promise<void>} pedir - Llama a la API y agrega la respuesta.
     * @returns {Promise<void>}
     */
    async #esperarRespuesta(pedir) {
        this.#ocupado(true);
        const indicador = this.#crearIndicadorEscribiendo();
        this.mensajes.append(indicador);
        this.#desplazarAlFinal();
        try {
            await pedir();
        } catch (error) {
            const tipo = error instanceof ChatApiError ? error.tipo : 'red';
            if (!(error instanceof ChatApiError)) {
                logger.error('[ChatWidget] Error inesperado al consultar:', error);
            }
            this.#mostrarError(this.config.errores[tipo], () => void this.#esperarRespuesta(pedir));
        } finally {
            indicador.remove();
            this.#ocupado(false);
        }
    }

    /** @param {boolean} ocupado */
    #ocupado(ocupado) {
        this.esperando = ocupado;
        this.enviarBoton.disabled = ocupado;
        this.microfono.disabled = ocupado;
    }

    async #iniciarGrabacion() {
        if (this.esperando || this.grabador) {
            return;
        }
        const grabador = new GrabadorDeVoz({
            duracionMaximaMs: this.config.audio.duracionMaximaSeg * 1000,
            alAvanzar: (ms) => {
                this.duracionGrabada = ms;
                this.contador.textContent = formatearDuracion(ms);
            },
            alLlegarAlLimite: () => void this.#enviarGrabacion(),
        });
        try {
            await grabador.iniciar();
        } catch (error) {
            const tipo = error instanceof GrabacionError ? error.tipo : 'noDisponible';
            this.#mostrarError(this.config.errores[tipo]);
            return;
        }
        this.grabador = grabador;
        this.duracionGrabada = 0;
        this.contador.textContent = formatearDuracion(0);
        this.#modoGrabacion(true);
        this.enviarGrabacionBoton.focus();
    }

    #cancelarGrabacion() {
        this.grabador?.cancelar();
        this.grabador = null;
        this.#modoGrabacion(false);
        this.microfono.focus();
    }

    async #enviarGrabacion() {
        const grabador = this.grabador;
        if (!grabador) {
            return;
        }
        this.grabador = null;
        const duracion = this.duracionGrabada;
        const grabacion = await grabador.detener();
        this.#modoGrabacion(false);
        this.campo.focus();
        if (grabacion.size === 0 || duracion < this.config.audio.duracionMinimaMs) {
            this.#mostrarError(this.config.errores.audioVacio);
            return;
        }
        /** @type {{ audio: Blob, nombre: string }} */
        let preparada;
        try {
            preparada = await prepararParaEnvio(grabacion);
        } catch (error) {
            logger.error('[ChatWidget] No se pudo convertir la nota de voz:', error);
            this.#mostrarError(this.config.errores.noDisponible);
            return;
        }
        const burbuja = this.#crearBurbujaDeVoz(URL.createObjectURL(preparada.audio));
        this.mensajes.append(burbuja);
        await this.#esperarRespuesta(async () => {
            const respuesta = await this.cliente.enviarAudio(this.conversacion.sessionId, preparada.audio, preparada.nombre);
            const transcripcion = respuesta.transcript ?? '';
            const texto = document.createElement('p');
            texto.className = 'c-chat-widget__text';
            texto.textContent = transcripcion;
            burbuja.append(texto);
            this.conversacion.agregar({ autor: 'usuario', texto: transcripcion, voz: true });
            this.#agregar({ autor: 'bot', texto: respuesta.reply, fuentes: respuesta.sources });
        });
    }

    /** @param {boolean} activo */
    #modoGrabacion(activo) {
        this.barraDeGrabacion.hidden = !activo;
        this.raiz.classList.toggle('is-recording', activo);
    }

    /** @param {ChatMensaje} mensaje */
    #agregar(mensaje) {
        this.conversacion.agregar(mensaje);
        this.mensajes.append(this.#crearBurbuja(mensaje));
        this.#desplazarAlFinal();
    }

    /**
     * @param {ChatMensaje} mensaje
     * @returns {HTMLElement}
     */
    #crearBurbuja(mensaje) {
        const burbuja = document.createElement('div');
        burbuja.className = `${CLASE_BURBUJA} ${CLASE_BURBUJA}--${mensaje.autor === 'usuario' ? 'user' : 'bot'}`;
        if (mensaje.voz) {
            burbuja.append(this.#crearRotuloDeVoz());
        }
        const texto = document.createElement('p');
        texto.className = 'c-chat-widget__text';
        texto.textContent = mensaje.texto;
        burbuja.append(texto);

        const enlaces = (mensaje.fuentes || [])
            .map((fuente) => urlDeFuenteSegura(fuente))
            .filter((url) => url !== null);
        if (enlaces.length > 0) {
            burbuja.append(this.#crearFuentes(/** @type {string[]} */ (enlaces)));
        }
        return burbuja;
    }

    /**
     * Burbuja del usuario con el reproductor de su nota de voz; la transcripción se agrega al responder.
     * @param {string} url - URL blob: de la grabación.
     * @returns {HTMLElement}
     */
    #crearBurbujaDeVoz(url) {
        const burbuja = document.createElement('div');
        burbuja.className = `${CLASE_BURBUJA} ${CLASE_BURBUJA}--user ${CLASE_BURBUJA}--voice`;
        const reproductor = document.createElement('audio');
        reproductor.controls = true;
        reproductor.preload = 'metadata';
        reproductor.src = url;
        burbuja.append(this.#crearRotuloDeVoz(), reproductor);
        this.#desplazarAlFinal();
        return burbuja;
    }

    /** @returns {HTMLElement} */
    #crearRotuloDeVoz() {
        const rotulo = document.createElement('span');
        rotulo.className = 'c-chat-widget__voice-label';
        rotulo.textContent = this.config.interfaz.notaDeVoz;
        return rotulo;
    }

    /**
     * @param {string[]} urls - Ya validadas con urlDeFuenteSegura.
     * @returns {HTMLElement}
     */
    #crearFuentes(urls) {
        const contenedor = document.createElement('div');
        contenedor.className = 'c-chat-widget__sources';
        const rotulo = document.createElement('span');
        rotulo.textContent = this.config.interfaz.fuentes;
        const lista = document.createElement('ul');
        for (const url of urls) {
            const enlace = document.createElement('a');
            enlace.href = url;
            enlace.textContent = url;
            if (!url.startsWith('/')) {
                enlace.target = '_blank';
                enlace.rel = 'noopener noreferrer';
            }
            const item = document.createElement('li');
            item.append(enlace);
            lista.append(item);
        }
        contenedor.append(rotulo, lista);
        return contenedor;
    }

    /** @returns {HTMLElement} */
    #crearIndicadorEscribiendo() {
        const indicador = document.createElement('div');
        indicador.className = `${CLASE_BURBUJA} ${CLASE_BURBUJA}--bot ${CLASE_BURBUJA}--typing`;
        const texto = document.createElement('span');
        texto.className = 'c-chat-widget__sr-only';
        texto.textContent = this.config.interfaz.escribiendo;
        indicador.append(texto);
        for (let i = 0; i < 3; i += 1) {
            const punto = document.createElement('span');
            punto.className = 'c-chat-widget__dot';
            punto.setAttribute('aria-hidden', 'true');
            indicador.append(punto);
        }
        return indicador;
    }

    /**
     * Burbuja de error, con botón para reintentar si se indica cómo. No se guarda en el historial.
     * @param {string} mensaje
     * @param {() => void} [reintentar]
     */
    #mostrarError(mensaje, reintentar) {
        const burbuja = document.createElement('div');
        burbuja.className = `${CLASE_BURBUJA} ${CLASE_BURBUJA}--bot ${CLASE_BURBUJA}--error`;
        burbuja.setAttribute('role', 'alert');
        const texto = document.createElement('p');
        texto.className = 'c-chat-widget__text';
        texto.textContent = mensaje;
        burbuja.append(texto);
        if (reintentar) {
            const boton = document.createElement('button');
            boton.type = 'button';
            boton.className = 'c-chat-widget__retry';
            boton.textContent = this.config.interfaz.reintentar;
            boton.addEventListener('click', () => {
                burbuja.remove();
                reintentar();
            });
            burbuja.append(boton);
        }
        this.mensajes.append(burbuja);
        this.#desplazarAlFinal();
    }

    /** Hace crecer el campo con el texto hasta ALTO_MAXIMO_CAMPO; recién ahí aparece la barra de desplazamiento. */
    #ajustarAltoCampo() {
        this.campo.style.height = 'auto';
        // scrollHeight no incluye los bordes y el campo usa box-sizing: border-box.
        const bordes = this.campo.offsetHeight - this.campo.clientHeight;
        const alto = this.campo.scrollHeight + bordes;
        this.campo.style.height = `${Math.min(alto, ALTO_MAXIMO_CAMPO)}px`;
        this.campo.style.overflowY = alto > ALTO_MAXIMO_CAMPO ? 'auto' : 'hidden';
    }

    #desplazarAlFinal() {
        this.mensajes.scrollTop = this.mensajes.scrollHeight;
    }
}

/** Inicializa cada widget conversacional presente en la página. */
export function initChatWidgets() {
    /** @type {NodeListOf<HTMLElement>} */
    const raices = document.querySelectorAll('[data-component="chat-widget"]');
    raices.forEach((raiz) => {
        const config = leerConfiguracion(raiz);
        if (!config) {
            logger.error('[ChatWidget] Falta la configuración data-chat-config o no es JSON válido.');
            return;
        }
        try {
            new ChatWidget(raiz, config);
        } catch (error) {
            logger.error('[ChatWidget] No se pudo inicializar el widget:', error);
        }
    });
}
