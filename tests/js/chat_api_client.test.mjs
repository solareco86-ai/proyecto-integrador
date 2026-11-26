// Pruebas del cliente de la API del widget conversacional (FE 4.4, issue #148).
// Se ejecutan con `node --test` desde tests/test_chat_api_client_js.py.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';

// package.json declara "type": "commonjs", así que el módulo ES del navegador se
// importa desde su código fuente como data URL (no tiene imports propios).
const fuente = await readFile(new URL('../../static/js/modules/ChatApiClient.js', import.meta.url), 'utf8');
const { ChatApiClient, ChatApiError, validarRespuesta } = await import(
    `data:text/javascript,${encodeURIComponent(fuente)}`
);

const RESPUESTA_OK = { reply: 'Hola', intent: 'saludo', sources: ['/carreras'], confidence: 0.9 };

function configuracion({ mock = false, timeoutTextoMs = 1000 } = {}) {
    return {
        longitudMaxima: 20,
        api: { baseUrl: '/api/v1/chat/', mock, timeoutTextoMs, timeoutAudioMs: 1000 },
        errores: {},
        mock: {
            respuesta: 'Eco: {mensaje}',
            transcripcion: 'texto dictado',
            intencion: 'mock',
            fuentes: ['/carreras'],
            confianza: 1,
            demoraMs: 0,
        },
    };
}

function respuestaHttp(estado, cuerpo) {
    return new Response(typeof cuerpo === 'string' ? cuerpo : JSON.stringify(cuerpo), { status: estado });
}

async function tipoDeError(promesa) {
    try {
        await promesa;
    } catch (error) {
        assert.ok(error instanceof ChatApiError, `se esperaba ChatApiError y llegó ${error}`);
        return error.tipo;
    }
    assert.fail('se esperaba un error');
}

test('envía la consulta escrita según el contrato', async () => {
    const llamadas = [];
    const cliente = new ChatApiClient(configuracion(), async (url, init) => {
        llamadas.push({ url, init });
        return respuestaHttp(200, { ...RESPUESTA_OK, extra: 'se descarta' });
    });

    const respuesta = await cliente.enviarTexto('sesion-1', '  ¿Qué carreras hay?  ');

    assert.deepEqual(respuesta, RESPUESTA_OK);
    assert.equal(llamadas[0].url, '/api/v1/chat/text');
    assert.equal(llamadas[0].init.method, 'POST');
    assert.deepEqual(JSON.parse(llamadas[0].init.body), { session_id: 'sesion-1', message: '¿Qué carreras hay?' });
});

test('envía la nota de voz como multipart y exige la transcripción', async () => {
    let cuerpo;
    const cliente = new ChatApiClient(configuracion(), async (_url, init) => {
        cuerpo = init.body;
        return respuestaHttp(200, { ...RESPUESTA_OK, transcript: 'qué carreras hay' });
    });

    const respuesta = await cliente.enviarAudio('sesion-1', new Blob(['audio'], { type: 'audio/webm' }));

    assert.equal(respuesta.transcript, 'qué carreras hay');
    assert.equal(cuerpo.get('session_id'), 'sesion-1');
    assert.equal(cuerpo.get('audio').name, 'nota-de-voz.webm');
});

test('rechaza consultas vacías o demasiado largas sin llamar al servidor', async () => {
    const cliente = new ChatApiClient(configuracion(), async () => assert.fail('no debía llamar al servidor'));

    assert.equal(await tipoDeError(cliente.enviarTexto('s', '   ')), 'validacion');
    assert.equal(await tipoDeError(cliente.enviarTexto('s', 'x'.repeat(21))), 'validacion');
    assert.equal(await tipoDeError(cliente.enviarAudio('s', new Blob([]))), 'audioVacio');
});

test('traduce cada falla del servidor a un tipo de error', async () => {
    const casos = [
        [() => Promise.reject(new TypeError('Failed to fetch')), 'red'],
        [() => Promise.resolve(respuestaHttp(422, { detail: 'x' })), 'validacion'],
        [() => Promise.resolve(respuestaHttp(503, 'caído')), 'servidor'],
        [() => Promise.resolve(respuestaHttp(404, 'sin backend')), 'servidor'],
        [() => Promise.resolve(respuestaHttp(200, 'no es json')), 'respuestaInvalida'],
        [() => Promise.resolve(respuestaHttp(200, { reply: 'falta el resto' })), 'respuestaInvalida'],
    ];
    for (const [fetchFn, esperado] of casos) {
        const cliente = new ChatApiClient(configuracion(), fetchFn);
        assert.equal(await tipoDeError(cliente.enviarTexto('s', 'hola')), esperado);
    }
});

test('corta la espera al superar el tiempo máximo', async () => {
    const cliente = new ChatApiClient(configuracion({ timeoutTextoMs: 20 }), (_url, init) => new Promise((_resolver, rechazar) => {
        init.signal.addEventListener('abort', () => rechazar(new DOMException('abortado', 'AbortError')));
    }));

    assert.equal(await tipoDeError(cliente.enviarTexto('s', 'hola')), 'timeout');
});

test('el modo mock responde sin llamar al servidor y con la forma del contrato', async () => {
    const cliente = new ChatApiClient(configuracion({ mock: true }), async () => assert.fail('no debía llamar al servidor'));

    const texto = await cliente.enviarTexto('s', 'hola');
    const audio = await cliente.enviarAudio('s', new Blob(['audio']));

    assert.ok(cliente.enModoMock);
    assert.deepEqual(texto, { reply: 'Eco: hola', intent: 'mock', sources: ['/carreras'], confidence: 1 });
    assert.equal(audio.transcript, 'texto dictado');
    assert.equal(audio.reply, 'Eco: texto dictado');
    assert.deepEqual(validarRespuesta(audio, true), audio);
});
