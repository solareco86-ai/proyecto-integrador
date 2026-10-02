### Taller Integrador: Pipeline de inferencia y auditoría orquestado por agentes autónomos

En esta práctica integradora final de la cátedra, los estudiantes lideran y supervisan un proyecto completo desarrollado en FastAPI, donde la implementación y verificación se realiza en colaboración con la tríada de agentes (**Aider**, **OpenCode** y **AGY CLI**).

#### Consigna del Proyecto
1. **Modelado y Contrato:** Definir con Pydantic esquemas de entrada para un dataset industrial con variables continuas y categóricas.
2. **Servicio de Inferencia:** Construir una API en FastAPI que sirva tanto un clasificador probabilístico (Naive Bayes) como un árbol de decisión (CART).
3. **Módulo de Explicabilidad:** Implementar endpoints de auditoría (`GET /rules` y `GET /tree/json`) para inspección de trazas lógicas.
4. **Servidor MCP:** Habilitar un servidor MCP que permita a un agente de terminal conectarse a la API, solicitar diagnósticos y generar un informe técnico resumido.
5. **Acreditación de Calidad:** Suite completa de tests en `pytest` pasando al 100% y cero errores de tipado estricto.
