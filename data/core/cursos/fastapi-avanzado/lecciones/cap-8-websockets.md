### WebSockets en FastAPI

Los **WebSockets** son un protocolo de comunicación full-duplex sobre una única conexión TCP de larga duración. A diferencia de HTTP, donde el cliente solicita y el servidor responde, con WebSockets ambas partes pueden enviar mensajes en cualquier momento. Esto es ideal para notificaciones en tiempo real, telemetría operativa y chat.

### Cuándo usar WebSockets

| Situación | Protocolo recomendado |
| :--- | :--- |
| Notificaciones push desde el servidor | WebSocket |
| Streaming de datos en tiempo real (telemetría, monitoreo) | WebSocket |
| Peticiones de consulta de datos puntuales | HTTP (REST) |
| Comunicación con clientes que no lo soportan | HTTP + SSE |

### Estructura básica de un endpoint WebSocket en FastAPI

FastAPI permite declarar un endpoint WebSocket con el decorador `@app.websocket`:

```python
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Eco: {data}")
    except WebSocketDisconnect:
        print("Cliente desconectado")
```

### El patrón ConnectionManager

En aplicaciones reales se suele mantener una colección de conexiones activas para poder **transmitir a todos** o a un cliente específico:

```python
class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket) -> None:
        await websocket.send_text(message)

    async def broadcast(self, message: str) -> None:
        for connection in self.active_connections:
            await connection.send_text(message)
```

### Integración con el ciclo de vida de la aplicación

Podés exponer el manager como una instancia accesible desde otros componentes:

```python
manager = ConnectionManager()

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_message(f"Cliente {client_id}: {data}", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
```

### Consideraciones de producción

1. **Autenticación**: validá la identidad del cliente al aceptar la conexión, no solo en la handshake.
2. **Reconexión**: el cliente debe implementar reintentos ante cortes de red.
3. **Escalado**: con múltiples workers, el manager en memoria no comparte conexiones entre procesos; considerá un broker (Redis pub/sub) si escalás.
4. **Heartbeats**: enviar mensajes periódicos para detectar conexiones caídas.

### Micro-desafío práctico

> Implementá un endpoint WebSocket que reciba valores de telemetría en JSON (por ejemplo `{"sensor": "vfd-01", "potencia_kw": 45.2}`) y los reenvíe a todos los clientes conectados usando `broadcast`.

### Resumen

- WebSockets habilitan comunicación full-duplex en tiempo real.
- FastAPI los expone con el decorador `@app.websocket`.
- El patrón `ConnectionManager` centraliza las conexiones activas y permite difundir mensajes.
- En producción considerá autenticación, reconexión, escalado y heartbeats.
