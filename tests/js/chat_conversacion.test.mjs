// Pruebas del estado de la conversación del widget (FE 4.2, issue #146).
// Se ejecutan con `node --test` desde tests/test_pruebas_js.py.
import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';

// Igual que en chat_api_client.test.mjs: el módulo ES se importa desde su fuente.
const fuente = await readFile(new URL('../../static/js/modules/ChatConversacion.js', import.meta.url), 'utf8');
const {
    CLAVE_HISTORIAL, CLAVE_SESION, ChatConversacion, MAXIMO_MENSAJES, urlDeFuenteSegura,
} = await import(`data:text/javascript,${encodeURIComponent(fuente)}`);

function almacenamientoEnMemoria(inicial = {}) {
    const datos = new Map(Object.entries(inicial));
    return {
        datos,
        getItem: (clave) => (datos.has(clave) ? datos.get(clave) : null),
        setItem: (clave, valor) => datos.set(clave, String(valor)),
    };
}

test('crea un session_id y lo reutiliza en la misma sesión del navegador', () => {
    const almacenamiento = almacenamientoEnMemoria();
    const primera = new ChatConversacion(almacenamiento, () => 'id-1');
    const segunda = new ChatConversacion(almacenamiento, () => 'id-2');

    assert.equal(primera.sessionId, 'id-1');
    assert.equal(segunda.sessionId, 'id-1');
    assert.equal(almacenamiento.datos.get(CLAVE_SESION), 'id-1');
});

test('el historial sigue al navegar a otra página y conserva solo los últimos mensajes', () => {
    const almacenamiento = almacenamientoEnMemoria();
    const conversacion = new ChatConversacion(almacenamiento);
    for (let i = 0; i < MAXIMO_MENSAJES + 5; i += 1) {
        conversacion.agregar({ autor: i % 2 ? 'bot' : 'usuario', texto: `mensaje ${i}` });
    }

    const enOtraPagina = new ChatConversacion(almacenamiento);

    assert.equal(enOtraPagina.mensajes.length, MAXIMO_MENSAJES);
    assert.equal(enOtraPagina.mensajes.at(-1).texto, `mensaje ${MAXIMO_MENSAJES + 4}`);
});

test('descarta un historial guardado que está corrupto o tiene mensajes inválidos', () => {
    const corrupto = new ChatConversacion(almacenamientoEnMemoria({ [CLAVE_HISTORIAL]: '{no es json' }));
    const mezclado = new ChatConversacion(almacenamientoEnMemoria({
        [CLAVE_HISTORIAL]: JSON.stringify([
            { autor: 'usuario', texto: 'válido' },
            { autor: 'admin', texto: 'autor desconocido' },
            { autor: 'bot', texto: 42 },
            { autor: 'bot', texto: 'fuentes inválidas', fuentes: [1] },
            { autor: 'usuario', texto: 'transcripción', voz: true },
            { autor: 'usuario', texto: 'voz inválida', voz: 'sí' },
        ]),
    }));

    assert.deepEqual(corrupto.mensajes, []);
    assert.deepEqual(mezclado.mensajes, [
        { autor: 'usuario', texto: 'válido' },
        { autor: 'usuario', texto: 'transcripción', voz: true },
    ]);
});

test('funciona sin almacenamiento o si el almacenamiento falla', () => {
    const queFalla = {
        getItem: () => { throw new Error('bloqueado'); },
        setItem: () => { throw new Error('bloqueado'); },
    };
    for (const almacenamiento of [null, queFalla]) {
        const conversacion = new ChatConversacion(almacenamiento, () => 'id');
        conversacion.agregar({ autor: 'usuario', texto: 'hola' });
        assert.equal(conversacion.sessionId, 'id');
        assert.equal(conversacion.mensajes.length, 1);
    }
});

test('solo acepta como enlace rutas del sitio y URLs https', () => {
    assert.equal(urlDeFuenteSegura('/carreras'), '/carreras');
    assert.equal(urlDeFuenteSegura(' /cursos/x '), '/cursos/x');
    assert.equal(urlDeFuenteSegura('https://abc.gob.ar/x'), 'https://abc.gob.ar/x');
    for (const peligrosa of ['javascript:alert(1)', 'JaVaScRiPt:alert(1)', 'data:text/html,x', '//otro.com', '/\\otro.com', 'http://inseguro.com', '', 7, null]) {
        assert.equal(urlDeFuenteSegura(peligrosa), null, `debía rechazar ${peligrosa}`);
    }
});
