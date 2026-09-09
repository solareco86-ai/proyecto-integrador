### Estrategias de Despliegue en Producción
Llevar nuestra aplicación local a servidores accesibles por internet:

- **Dockerización**: Creación de `Dockerfile` optimizados para FastAPI usando compilaciones multi-etapa (multi-stage builds).
- **Servidores de Producción**: Configuración de Gunicorn como manejador de procesos y Uvicorn como trabajador ASGI.
- **Servidores VPS & Reverse Proxy**: Puesta a punto con Nginx como proxy reverso, Let's Encrypt para HTTPS/SSL gratuito y automatización de despliegue continuo (CI/CD) con GitHub Actions.
