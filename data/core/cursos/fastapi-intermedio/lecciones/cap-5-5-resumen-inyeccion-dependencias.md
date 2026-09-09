### 5.5 Resumen Integrador del Capítulo 5 (Chapter Summary)

En este capítulo exploramos el sistema de **Inyección de Dependencias** de FastAPI, una de las características de arquitectura más avanzadas del framework para promover el principio DRY, facilitar las pruebas automatizadas y desacoplar la seguridad y la gestión de recursos.

---

### 📋 Checklist de Conceptos y Habilidades Dominadas

| Lección | Conceptos Clave | Métodos y Herramientas |
| :--- | :--- | :--- |
| **5.1 ¿Qué es la Inyección de Dependencias?** | Inversión de Control (IoC), reutilización de lógica, integración con OpenAPI y desacoplamiento para pruebas con `app.dependency_overrides`. | `Depends()`, IoC, Mocks |
| **5.2 Dependencias basadas en Funciones** | Creación de funciones de dependencia con `Depends()`, encadenamiento de sub-dependencias y limpieza de recursos con `yield`. | `Depends()`, `yield`, Generators |
| **5.3 Dependencias basadas en Clases** | Encapsulamiento de parámetros de consulta con la sintaxis abreviada `Depends()`, y validadores parametrizables con `__call__`. | `Depends()`, `__call__` |
| **5.4 Scopes: Ruta, Router y Global** | Aplicación de dependencias transversales sin inyectar parámetros a nivel de Ruta individual, `APIRouter` y `FastAPI` global. | `dependencies=[Depends(...)]` |

---

### 🚀 Próximos Pasos

Has completado con éxito el **Capítulo 5**. En el **Capítulo 6 (Autenticación y Seguridad en FastAPI)** aplicarás la inyección de dependencias para implementar esquemas de autenticación con OAuth2, tokens JWT y hashing seguro de contraseñas.
