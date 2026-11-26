// Pruebas de la grabación de notas de voz y su conversión a WAV (FE 4.3, issue #147).
// Se ejecutan con `node --test` desde tests/test_pruebas_js.py.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';

// Igual que en los demás archivos: los módulos ES se importan desde su fuente.
async function importar(nombre) {
    const fuente = await readFile(new URL(`../../static/js/modules/${nombre}`, import.meta.url), 'utf8');
    return import(`data:text/javascript,${encodeURIComponent(fuente)}`);
}
const { codificarWav, extensionAceptada, prepararParaEnvio, FRECUENCIA_WAV } = await importar('ConversorWav.js');
const { GrabadorDeVoz, GrabacionError, elegirFormato, grabacionDisponible } = await importar('VoiceRecorder.js');

const esperar = (ms) => new Promise((resolver) => setTimeout(resolver, ms));

class MediaRecorderFalso extends EventTarget {
    static soportados = new Set(['audio/ogg;codecs=opus']);
    static isTypeSupported(tipo) {
        return MediaRecorderFalso.soportados.has(tipo);
    }

    constructor(flujo, opciones = {}) {
        super();
        this.flujo = flujo;
        this.mimeType = opciones.mimeType ?? 'audio/mp4';
        this.state = 'inactive';
    }

    start() {
        this.state = 'recording';
        this.dispatchEvent(Object.assign(new Event('dataavailable'), { data: new Blob(['parte-1']) }));
    }

    stop() {
        this.state = 'inactive';
        this.dispatchEvent(Object.assign(new Event('dataavailable'), { data: new Blob(['parte-2']) }));
        this.dispatchEvent(new Event('stop'));
    }
}

function entornoFalso({ rechazo = null, permitido = true } = {}) {
    const pistas = [{ detenida: false, stop() { this.detenida = true; } }];
    return {
        pistas,
        mediaDevices: {
            getUserMedia: async () => {
                if (rechazo) throw Object.assign(new Error(rechazo), { name: rechazo });
                return { getTracks: () => pistas };
            },
        },
        MediaRecorder: MediaRecorderFalso,
        politicaDePermisos: { allowsFeature: (caracteristica) => caracteristica !== 'microphone' || permitido },
    };
}

test('codifica WAV PCM de 16 bits mono con la cabecera correcta', () => {
    const buffer = codificarWav(new Float32Array([0, 1, -1, 2]), FRECUENCIA_WAV);
    const vista = new DataView(buffer);
    const texto = (desde, largo) => String.fromCharCode(...new Uint8Array(buffer, desde, largo));

    assert.equal(buffer.byteLength, 44 + 4 * 2);
    assert.equal(texto(0, 4), 'RIFF');
    assert.equal(texto(8, 4), 'WAVE');
    assert.equal(vista.getUint16(22, true), 1, 'mono');
    assert.equal(vista.getUint32(24, true), 16000);
    assert.equal(vista.getUint16(34, true), 16, 'bits por muestra');
    assert.equal(vista.getUint32(40, true), 8, 'bytes de datos');
    assert.deepEqual([0, 1, 2, 3].map((i) => vista.getInt16(44 + i * 2, true)), [0, 32767, -32768, 32767]);
});

test('reconoce los formatos del contrato y convierte los demás a WAV', async () => {
    assert.equal(extensionAceptada('audio/webm;codecs=opus'), 'webm');
    assert.equal(extensionAceptada('audio/ogg'), 'ogg');
    assert.equal(extensionAceptada('audio/mp4'), null);

    const webm = await prepararParaEnvio(new Blob(['x'], { type: 'audio/webm;codecs=opus' }), () => assert.fail('no debía convertir'));
    assert.equal(webm.nombre, 'nota-de-voz.webm');

    const safari = await prepararParaEnvio(new Blob(['x'], { type: 'audio/mp4' }), async () => new Blob(['wav'], { type: 'audio/wav' }));
    assert.equal(safari.nombre, 'nota-de-voz.wav');
    assert.equal(safari.audio.type, 'audio/wav');
});

test('elige el primer formato preferido que soporta el navegador', () => {
    assert.equal(elegirFormato((tipo) => tipo === 'audio/ogg;codecs=opus'), 'audio/ogg;codecs=opus');
    assert.equal(elegirFormato(() => false), '', 'Safari: usa su formato por defecto');
});

test('detecta si se puede grabar, incluida la Permissions-Policy del sitio', () => {
    assert.equal(grabacionDisponible(entornoFalso()), true);
    assert.equal(grabacionDisponible(entornoFalso({ permitido: false })), false);
    assert.equal(grabacionDisponible({ ...entornoFalso(), MediaRecorder: undefined }), false);
    assert.equal(grabacionDisponible({ ...entornoFalso(), mediaDevices: undefined }), false);
});

test('graba, devuelve el audio y apaga el micrófono', async () => {
    const entorno = entornoFalso();
    const grabador = new GrabadorDeVoz({ duracionMaximaMs: 60000, entorno });

    await grabador.iniciar();
    assert.equal(grabador.grabando, true);
    const audio = await grabador.detener();

    assert.equal(audio.type, 'audio/ogg;codecs=opus');
    assert.equal(await audio.text(), 'parte-1parte-2');
    assert.equal(grabador.grabando, false);
    assert.equal(entorno.pistas[0].detenida, true);
});

test('traduce los rechazos del micrófono a tipos de error', async () => {
    const casos = [['NotAllowedError', 'permisoDenegado'], ['NotFoundError', 'sinMicrofono'], ['AbortError', 'noDisponible']];
    for (const [rechazo, esperado] of casos) {
        const grabador = new GrabadorDeVoz({ duracionMaximaMs: 1000, entorno: entornoFalso({ rechazo }) });
        await assert.rejects(grabador.iniciar(), (error) => error instanceof GrabacionError && error.tipo === esperado);
    }
    const bloqueado = new GrabadorDeVoz({ duracionMaximaMs: 1000, entorno: entornoFalso({ permitido: false }) });
    await assert.rejects(bloqueado.iniciar(), (error) => error.tipo === 'noDisponible');
});

test('avisa al llegar a la duración máxima y cancelar descarta la grabación', async () => {
    const entorno = entornoFalso();
    let limite = 0;
    const avances = [];
    const grabador = new GrabadorDeVoz({
        duracionMaximaMs: 300, entorno, alAvanzar: (ms) => avances.push(ms), alLlegarAlLimite: () => { limite += 1; },
    });

    await grabador.iniciar();
    await esperar(700);
    assert.equal(limite, 1, 'avisa una sola vez');
    assert.ok(avances.length >= 1);

    grabador.cancelar();
    assert.equal(grabador.grabando, false);
    assert.equal(entorno.pistas[0].detenida, true);
    assert.equal((await grabador.detener()).size, 0);
});
