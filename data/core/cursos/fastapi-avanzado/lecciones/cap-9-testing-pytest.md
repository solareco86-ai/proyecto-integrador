### Tests Asíncronos Automatizados
Desarrollar una estrategia de testing sólida para verificar el comportamiento de la API:

- **Estructuración con pytest**: Configuración de fixtures asíncronos.
- **Cliente HTTPX**: Uso de `AsyncClient` de HTTPX para realizar peticiones de prueba a la aplicación FastAPI sin levantar un servidor físico.
- **Aislamiento y Mocks**: Uso de bases de datos temporales (SQLite en memoria) y stubs de llamadas de red de APIs externas.
