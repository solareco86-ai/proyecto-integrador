### Seguridad y Autenticación con OAuth2 y JWT
Implementación de flujos robustos de autenticación para proteger endpoints:

- **JSON Web Tokens (JWT)**: Generación, firma y verificación de tokens encriptados.
- **OAuth2 con Contraseñas**: Integración del flujo de login estándar de OAuth2 mediante `OAuth2PasswordBearer` y hashing de contraseñas con Passlib e bcrypt.
- **CORS y Middlewares**: Configuración de restricciones de dominios para consumo seguro de la API desde frontends web independientes.
