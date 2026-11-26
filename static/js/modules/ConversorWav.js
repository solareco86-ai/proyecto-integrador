/**
 * @fileoverview Conversión de notas de voz a WAV (FE 4.3, issue #147).
 * El contrato del Epic #144 acepta `.webm`, `.ogg` y `.wav`. Safari graba en
 * `audio/mp4`, así que esas grabaciones se convierten en el navegador a WAV PCM
 * de 16 bits, mono y 16 kHz (el formato que el Eje 2.2 usa de todos modos).
 */

/** Formatos del contrato, sin parámetros de códec. */
const FORMATOS_ACEPTADOS = new Map([
    ['audio/webm', 'webm'],
    ['audio/ogg', 'ogg'],
    ['audio/wav', 'wav'],
    ['audio/x-wav', 'wav'],
    ['audio/wave', 'wav'],
]);

/** Frecuencia de muestreo de las conversiones (la que usa el reconocimiento del habla). */
export const FRECUENCIA_WAV = 16000;

/**
 * @param {string} tipoMime - Por ejemplo `audio/webm;codecs=opus`.
 * @returns {string | null} Extensión del archivo si el contrato acepta el formato, o null.
 */
export function extensionAceptada(tipoMime) {
    const base = tipoMime.split(';')[0].trim().toLowerCase();
    return FORMATOS_ACEPTADOS.get(base) ?? null;
}

/**
 * Codifica muestras mono en WAV PCM de 16 bits.
 * @param {Float32Array} muestras - Valores entre -1 y 1 (los que se pasan se recortan).
 * @param {number} frecuencia - Muestras por segundo.
 * @returns {ArrayBuffer}
 */
export function codificarWav(muestras, frecuencia) {
    const bytesPorMuestra = 2;
    const datos = muestras.length * bytesPorMuestra;
    const buffer = new ArrayBuffer(44 + datos);
    const vista = new DataView(buffer);
    /** @param {number} posicion @param {string} texto */
    const escribirTexto = (posicion, texto) => {
        for (let i = 0; i < texto.length; i += 1) {
            vista.setUint8(posicion + i, texto.charCodeAt(i));
        }
    };
    escribirTexto(0, 'RIFF');
    vista.setUint32(4, 36 + datos, true);
    escribirTexto(8, 'WAVE');
    escribirTexto(12, 'fmt ');
    vista.setUint32(16, 16, true); // tamaño del bloque fmt
    vista.setUint16(20, 1, true); // PCM
    vista.setUint16(22, 1, true); // mono
    vista.setUint32(24, frecuencia, true);
    vista.setUint32(28, frecuencia * bytesPorMuestra, true); // bytes por segundo
    vista.setUint16(32, bytesPorMuestra, true); // alineación de bloque
    vista.setUint16(34, 16, true); // bits por muestra
    escribirTexto(36, 'data');
    vista.setUint32(40, datos, true);
    for (let i = 0; i < muestras.length; i += 1) {
        const valor = Math.max(-1, Math.min(1, muestras[i]));
        vista.setInt16(44 + i * bytesPorMuestra, valor < 0 ? valor * 0x8000 : valor * 0x7fff, true);
    }
    return buffer;
}

/**
 * Decodifica la grabación con Web Audio y la remuestrea a WAV mono de 16 kHz.
 * @param {Blob} grabacion
 * @returns {Promise<Blob>}
 */
export async function convertirAWav(grabacion) {
    const contexto = new AudioContext();
    let audio;
    try {
        audio = await contexto.decodeAudioData(await grabacion.arrayBuffer());
    } finally {
        void contexto.close();
    }
    const largo = Math.max(1, Math.ceil(audio.duration * FRECUENCIA_WAV));
    // Con un solo canal de salida, Web Audio mezcla la grabación a mono.
    const offline = new OfflineAudioContext(1, largo, FRECUENCIA_WAV);
    const fuente = offline.createBufferSource();
    fuente.buffer = audio;
    fuente.connect(offline.destination);
    fuente.start();
    const remuestreado = await offline.startRendering();
    return new Blob([codificarWav(remuestreado.getChannelData(0), FRECUENCIA_WAV)], { type: 'audio/wav' });
}

/**
 * Deja la grabación en un formato del contrato y le pone nombre de archivo.
 * @param {Blob} grabacion
 * @param {(grabacion: Blob) => Promise<Blob>} [convertir] - Inyectable para pruebas.
 * @returns {Promise<{ audio: Blob, nombre: string }>}
 */
export async function prepararParaEnvio(grabacion, convertir = convertirAWav) {
    const extension = extensionAceptada(grabacion.type);
    if (extension) {
        return { audio: grabacion, nombre: `nota-de-voz.${extension}` };
    }
    return { audio: await convertir(grabacion), nombre: 'nota-de-voz.wav' };
}
