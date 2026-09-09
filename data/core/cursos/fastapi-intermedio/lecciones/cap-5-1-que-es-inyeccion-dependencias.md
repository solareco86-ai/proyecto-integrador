### 5.1 ¿Qué es la Inyección de Dependencias? (What is Dependency Injection)

La **Inyección de Dependencias** (*Dependency Injection* o **DI**) es un patrón de diseño de software e ingeniería en el cual una función o componente recibe sus recursos o dependencias externas desde el exterior en lugar de instanciarlos internamente de forma rígida (*Inversion of Control* - IoC).

---

### 1. El Problema de las Dependencias Acopladas

Imaginá que cada endpoint de tu API necesitara conectarse manualmente a una base de datos, validar el token del usuario y leer la configuración global. Escribir esa lógica dentro de cada controlador genera tres inconvenientes graves:
1. **Duplicación Masiva de Código (DRY violado)**: Misma lógica repetida en decenas de rutas.
2. **Dificultad para Pruebas Automatizadas**: Imposibilidad de sustituir la base de datos real por un *mock* de pruebas durante la ejecución de los tests.
3. **Alto Acoplamiento**: Cualquier cambio en el sistema de autenticación exige modificar individualmente cada función controladora.

---

### 2. El Sistema de Inyección de Dependencias de FastAPI

FastAPI incluye uno de los sistemas de inyección de dependencias más potentes, elegantes e intuitivos del ecosistema de Python.

#### Ventajas Principales en FastAPI:
- **Reutilización Transparente de Código**: Una sola función de dependencias puede ser consumida por cientos de endpoints.
- **Resolución Automática de Parámetros**: FastAPI inspecciona qué necesita la dependencia (*Path*, *Query*, *Headers*, *Body*) y resuelve los argumentos antes de ejecutar la función.
- **Jerarquía y Sub-dependencias**: Una dependencia puede depender a su vez de otras dependencias de forma enlazada.
- **Integración Nativa con OpenAPI**: Las dependencias que solicitan cabeceras o tokens (como `Authorization`) aparecen automáticamente documentadas en Swagger UI (`/docs`).
- **Sustitución de Dependencias en Tests (`app.dependency_overrides`)**: Permite reemplazar servicios reales por falsos (*mocks*) en las pruebas unitarias sin tocar el código fuente de producción.

---

### Resumen de la Lección
La Inyección de Dependencias desacopla las responsabilidades de la aplicación, permitiendo que FastAPI resuelva la autenticación, la lectura de parámetros y la apertura de conexiones de forma centralizada y testeable.
