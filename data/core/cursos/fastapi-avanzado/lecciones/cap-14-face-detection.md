### Streaming y Procesamiento de Imagen en Tiempo Real
Construcción de un caso de uso avanzado integrando procesamiento multimedia y WebSockets:

- **Configuración de OpenCV**: Carga de clasificadores en cascada de Haar o modelos de deep learning para detección de rostros.
- **Procesamiento de Cuadros (Frames)**: Decodificación en el servidor de imágenes en formato base64 recibidas a través de una conexión WebSocket.
- **Streaming de Resultados**: Procesamiento de la imagen, dibujo de rectángulos en las caras detectadas y retransmisión del frame modificado al cliente en tiempo real con latencia mínima.
