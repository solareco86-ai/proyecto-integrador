# Widget conversacional del sitio

Chat flotante estilo WhatsApp con el que el público consulta sobre el instituto por **texto** o por **nota de voz**. Es el frontend del Epic #144 (iniciativa #150). El motor que responde lo desarrollan los estudiantes de *Técnicas de Procesamiento del Habla* en los Epics #129, #134 y #139.

Mientras ese motor no exista, el widget funciona en **modo mock**: no llama al servidor y responde con un aviso de que el asistente está en desarrollo, con enlaces a la oferta académica y a Secretaría.

## Dónde está cada cosa

| Pieza | Archivo | Qué hace |
|---|---|---|
| Textos y configuración | `data/config/chat_widget.yaml` | Todo lo que ve el público, los límites, la conexión con la API y el modo mock. |
| Validación | `src/application/dtos/chat_widget_dto.py` | `ChatWidgetModel` valida el YAML (también lo hace `scripts/validate_content.py`). `configuracion_cliente()` arma lo que necesita el JavaScript. |
| Carga | `src/application/data_service.py` | `get_chat_widget()` lee y cachea el YAML. |
| Contacto humano | `src/adapters/presenters/chat_widget_presenter.py` | Arma el enlace a WhatsApp, o el correo de Secretaría si WhatsApp no está habilitado. |
| Funciones de plantilla | `src/infrastructure/fastapi/dependencies.py` | `chat_widget_textos()` y `chat_widget_contacto()`, disponibles en todas las plantillas. |
| Plantilla | `templates/partials/components/chat_widget.html` | Macro `chat_widget(textos, contacto, abierto)`. Serializa la configuración en `<script type="application/json" data-chat-config>`. |
| Inclusión en el sitio | `templates/base.html` (bloque `fab`) | Todas las páginas que heredan de `base.html` muestran el widget. |
| Estilos | `static/css/ChatWidget.css` | Importado desde `static/css/src/input.css`. Prefijo `c-chat-widget` y variables `--chat-*`. Tema claro y oscuro. |
| Comportamiento | `static/js/modules/ChatWidget.js` | Ventana, envío, «escribiendo», errores con reintento, grabación y accesibilidad. Lo inicia `static/js/app.js`. |
| Cliente de la API | `static/js/modules/ChatApiClient.js` | Contrato `/api/v1/chat`, tiempos máximos, tipos de error y modo mock. |
| Estado | `static/js/modules/ChatConversacion.js` | `session_id`, historial en `sessionStorage` y filtro de enlaces seguros. |
| Grabación | `static/js/modules/VoiceRecorder.js` | `MediaRecorder`, permisos, límite de duración y detección de la `Permissions-Policy`. |
| Conversión de audio | `static/js/modules/ConversorWav.js` | Convierte a WAV mono de 16 kHz lo que el contrato no acepta (Safari graba `audio/mp4`). |
| CSP | `src/infrastructure/fastapi/csp.py` | `media-src 'self' blob:` para escuchar la nota antes de enviarla. |

## Contrato con el motor

| Método y ruta | Entrada | Salida |
|---|---|---|
| `POST /api/v1/chat/text` | JSON `{ "session_id", "message" }` | `{ "reply", "intent", "sources", "confidence" }` |
| `POST /api/v1/chat/audio` | `multipart/form-data`: `audio` (`.webm`, `.ogg` o `.wav`) y `session_id` | Lo mismo, más `transcript` |
| `GET /api/v1/chat/health` | — | Estado del servicio y módulos activos |

- `sources` son rutas del sitio (`/carreras`) o URLs `https:`. Cualquier otra cosa no se muestra como enlace.
- Si la respuesta no respeta el contrato, el widget muestra el error `respuestaInvalida`.

## Configuración (`data/config/chat_widget.yaml`)

| Clave | Para qué |
|---|---|
| `titulo`, `subtitulo`, `avatar`, `saludo`, `aviso`, `placeholder` | Lo que se ve en la ventana. |
| `contacto.whatsapp`, `contacto.correo` | Texto del enlace de contacto humano. |
| `longitudMaxima` | Largo máximo de una consulta escrita. |
| `etiquetas.*` | `aria-label` y `label` de los controles. |
| `interfaz.*` | Textos que muestra el JavaScript («escribiendo», «Más información», «Reintentar», «Grabando», «Nota de voz»). |
| `audio.duracionMaximaSeg`, `audio.duracionMinimaMs` | Al llegar al máximo, la nota se envía sola. Las más cortas que el mínimo se descartan. |
| `api.baseUrl`, `api.timeoutTextoMs`, `api.timeoutAudioMs` | Conexión con el motor. |
| `api.mock` | `true`: respuestas simuladas sin llamar al servidor. **Pasar a `false` cuando el backend esté disponible (#130).** |
| `errores.*` | Mensaje para el público por cada tipo de error (red, timeout, servidor, validación, audio vacío, respuesta inválida, permiso de micrófono denegado, sin micrófono, grabación no disponible). |
| `mock.*` | Respuesta, transcripción, intención, fuentes, confianza y demora del modo mock. **El público ve estos textos**, así que no deben sonar a prueba técnica. Si la respuesta incluye `{mensaje}`, se reemplaza por la consulta. |

**WhatsApp:** el enlace de contacto se controla con las variables de entorno `WHATSAPP_ENABLED`, `WHATSAPP_PHONE` y `WHATSAPP_MESSAGE` (ver `src/infrastructure/settings/config.py`). Mientras el número institucional siga en trámite, `WHATSAPP_ENABLED` queda en `False` y el chat ofrece el correo de Secretaría.

## Ocultar el widget en una página

Sobrescribir el bloque vacío en la plantilla de esa página:

```jinja
{% block fab %}{% endblock %}
```

## Seguridad

- **XSS:** todo lo que llega del servidor se inserta con `textContent`. `tests/test_chat_widget_js.py` verifica que `ChatWidget.js` no use `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `eval` ni `new Function`.
- **Enlaces:** las fuentes pasan por `urlDeFuenteSegura()`, que rechaza `javascript:`, `data:`, `//otro-sitio` y `http:`. Los enlaces externos se abren con `rel="noopener noreferrer"`.
- **Privacidad:** las notas de voz no se guardan en el navegador. El historial (máximo 50 mensajes, en `sessionStorage`) guarda solo su transcripción.

## Accesibilidad

- Ventana con `role="dialog"`, `aria-modal="true"` y título asociado.
- Al abrir, el foco va al campo. Tab y Shift+Tab recorren solo los controles de la ventana. Escape cierra (o descarta la grabación en curso) y devuelve el foco al botón.
- Mensajes en `role="log"` con `aria-live="polite"`. El indicador de «escribiendo» tiene texto para lectores de pantalla.
- Foco visible en todos los controles y animaciones desactivadas con `prefers-reduced-motion`.

## Notas de voz y el micrófono en producción

El botón de micrófono solo aparece si el navegador tiene `MediaRecorder` y `getUserMedia`, y si la cabecera `Permissions-Policy` del sitio permite el micrófono.

En producción, las cabeceras de seguridad las agrega nginx en el VPS (no están en este repositorio). `isftn199.com.ar` envía `permissions-policy: geolocation=(), microphone=(self), camera=(), payment=()`, que permite el micrófono solo al propio sitio.

- Esa cabecera sale de `/etc/nginx/snippets/security-headers-isftn199.conf`: una copia del snippet común `/etc/nginx/conf.d/security-headers-common.conf`, que comparten otros sitios del VPS y bloquea el micrófono. **Si cambia el snippet común, hay que replicar el cambio en el de isftn199.**
- `dev.isftn199.com.ar` no envía `Permissions-Policy`, así que ahí el micrófono funciona por defecto.
- Para cualquier cambio en el VPS, seguir las reglas de operación de [ops.md](ops.md).

## Ver y probar en local

```bash
./run.sh --debug        # o: DEBUG=true python3 run.py
```

- Cualquier página del sitio, por ejemplo `http://127.0.0.1:8001/`.
- `http://127.0.0.1:8001/dev/preview/chat_widget`: el widget abierto, solo con `DEBUG=true`.
- `http://127.0.0.1:8001/dev/preview/chat_widget_cerrado`: solo el botón.

En `127.0.0.1` el navegador permite el micrófono porque lo considera un contexto seguro.

**Pruebas automáticas** (entran en el pipeline del pre-push):

| Archivo | Qué cubre |
|---|---|
| `tests/test_chat_widget.py` | Plantilla: accesibilidad, textos de los datos y configuración serializada. |
| `tests/test_chat_widget_textos.py` | YAML y modelo. |
| `tests/test_chat_widget_js.py` | Auditoría anti-XSS y que `app.js` inicie el widget. |
| `tests/test_chat_widget_integracion.py` | El widget aparece en las páginas y el contacto humano se arma bien. |
| `tests/test_pruebas_js.py` | Corre con `node --test` los archivos de `tests/js/`: cliente de la API, estado de la conversación, grabación y conversión a WAV. |

## Limitaciones conocidas

- Si alguien cambia de página mientras espera una respuesta, esa respuesta se pierde (su consulta queda en el historial).
- El widget responde en modo mock hasta que el backend implemente el contrato (#130). En ese modo, la nota de voz no se transcribe: se muestra el texto de `mock.transcripcion`.
