# Lección 4.3: Taller Integrador: Pipeline de Inferencia y Auditoría Orquestado por Agentes Autónomos

Llegamos a la culminación del trayecto formativo en **Procesamiento y Aprendizaje Automático** del **ISFT N° 199**. A lo largo de tres unidades temáticas, transformamos un script rudimentario de consola en una plataforma integral de ingeniería de datos y Machine Learning: ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md).

Este **Taller Integrador Final** constituye la evaluación práctica de la cátedra. El desafío consiste en orquestar el ciclo de vida completo del microservicio, colaborando en forma activa con el cuarteto de agentes de IA (**OpenCode**, **Antigravity CLI**, **Claude Code** y **Aider**), manteniendo el control total de la arquitectura, la calidad del software y la gobernanza del repositorio.

---

## 1. Visión Holística de la Arquitectura de energy-ml

El sistema desarrollado articula las cuatro capas de la Arquitectura Limpia e integra tanto modelos numéricos como simbólicos:

```
               +-------------------------------------------------+
               |            Clientes y Agentes de IA             |
               |      (AGY CLI / OpenCode / Aider / SCADA)       |
               +-------------------------------------------------+
                                        |
                 HTTP REST / OpenAPI    |    Model Context Protocol (JSON-RPC)
                 (GET / POST)           |    (tools/list, tools/call)
                                        v
+-------------------------------------------------------------------------------+
|                       Capa de Infraestructura (FastAPI)                       |
|  - /api/v1/predict/consumo       - /api/v1/classify/bayes                     |
|  - /api/v1/classify/knn          - /api/v1/rules                              |
|  - /api/v1/explain/tree          - /api/v1/metrics                            |
|  - /mcp (Servidor MCP)           - Lifespan (Gestión de Modelos en Memoria)   |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                   Capa de Aplicación y Servicios (MLOps)                      |
|  - DTOs Pydantic v2 (Validación estricta y contratos inmutables)             |
|  - Serializadores de Árboles (JSON Explicable para Agentes)                   |
|  - Orquestador de Métricas (Recall, F1-Score, Matriz de Confusión)            |
+-------------------------------------------------------------------------------+
                                        |
                                        v
+-------------------------------------------------------------------------------+
|                      Capa de Dominio y Modelos Híbridos                       |
|  - Deducción Simbólica (AQ / FOIL / Espacio de Versiones S-G)                 |
|  - Inducción Estadística (GaussianNB, KNeighborsClassifier, CART Regressor)   |
|  - Prevención de Fuga Temporal (Time-Series Split sin Shuffle)                |
+-------------------------------------------------------------------------------+
```

---

## 2. Consignas Obligatorias del Proyecto Integrador

Para la aprobación del proyecto, los estudiantes deben verificar los siguientes 6 hitos técnicos:

### Hito 1: Contratos e Ingesta de Telemetría (Pydantic v2)
- Todos los esquemas de entrada y salida deben residir en `src/application/dtos/` con `model_config = ConfigDict(extra="forbid", frozen=True)`.
- Tipado estricto en el 100% de los campos sin tipos desconocidos (`Unknown`).

### Hito 2: Ciclo de Vida y Persistencia en Inferencia
- Los artefactos entrenados (`.joblib`) deben cargarse exclusivamente durante el evento `lifespan` de FastAPI, resguardando los punteros en `app.state`.
- Manejo robusto de errores si el archivo serializado no se encuentra disponible.

### Hito 3: Dualidad Estadística y Simbólica
- Exponer al menos un clasificador probabilístico (Naive Bayes) y un clasificador métrico (k-NN).
- Exponer el catálogo de reglas lógicas auditables en `GET /api/v1/rules` y la descomposición del árbol en `GET /api/v1/explain/tree`.

### Hito 4: Servidor MCP para IA Agéntica
- Exponer el endpoint `POST /mcp` con compatibilidad para JSON-RPC 2.0.
- Registrar al menos dos herramientas operativas (`tools/list` y `tools/call`) que permitan a un agente diagnosticar telemetría y consultar reglas sin intervención humana directa.

### Hito 5: Suite de Pruebas y Cobertura (TDD)
- Suite completa en `pytest` cubriendo rutas, validaciones y lógica de dominio.
- Cobertura de código verificada superior al 85%:
  ```bash
  pytest --cov=src --cov-fail-under=85 tests/
  ```

### Hito 6: Gobernanza con Git y GitHub CLI (gh)
- Todo el trabajo debe reflejar un historial de **commits atómicos y descriptivos**.
- Publicación de un Pull Request descriptivo utilizando `gh pr create` auditado por la herramienta agéntica.

---

## 3. Dinámica de Trabajo con el Cuarteto de IA Agéntica

El estudiante no programa en soledad; actúa como **Ingeniero Líder y Arquitecto**, delegando tareas específicas según la fortaleza de cada herramienta:

1. **OpenCode:** Utilizado para la exploración inicial, redacción de funciones puras de utilidad y generación de tests unitarios básicos sin consumo de saldo de API.
2. **Antigravity CLI (AGY):** Utilizado como asistente principal de terminal para refactorizaciones estructurales, poda de contexto AST en CPU ($0 tokens) y verificación en navegador web (`/browser`).
3. **Claude Code (Opcional):** Utilizado para revisiones de código de alto estándar corporativo y auditoría de seguridad.
4. **Aider (Opcional):** Utilizado para ciclos iterativos de TDD (*Red-Green-Refactor*) con DeepSeek API en horario valle, ejecutando commits atómicos automáticos tras cada test superado.

---

## 4. Rúbrica de Evaluación Académica (ISFT N° 199)

| Criterio de Evaluación | Ponderación | Nivel Excelente (Aprobado Destacado) | Nivel Insuficiente |
| :--- | :--- | :--- | :--- |
| **Arquitectura y Tipado Estricto** | 25% | Arquitectura limpia respetada, 0 errores en Pyright/Pylance, dataclasses y Pydantic v2 correctos. | Lógica de negocio mezclada en rutas FastAPI, tipos dinámicos (`Any`) sin justificación. |
| **Modelos Estadísticos y Simbólicos** | 25% | Implementación correcta de inferencia continua y discreta, con serialización y explicabilidad en JSON. | Modelos no funcionales, sobreajuste evidente o falta de partición temporal adecuada. |
| **Protocolo MCP y Agentes** | 20% | Servidor MCP operativo, tools documentadas con JSON Schema y consumibles desde terminal. | Endpoint MCP con errores de esquema o ausente. |
| **Calidad de Tests (TDD)** | 15% | Suite completa con `pytest` y `TestClient`, cobertura >= 85%, pruebas unitarias y de integración. | Cobertura menor al 85% o tests triviales sin aserciones reales. |
| **Gobernanza Git y Entrega** | 15% | Commits atómicos, sin mezclar refactors con features, PR documentado con `gh`. | Commit único masivo (*monolithic commit*) o mensajes no informativos. |

---

## 5. Reflexión Final: El Rol del Ingeniero de IA del Mañana

La automatización agéntica no reemplaza el criterio del profesional de software; lo eleva. Cuando las herramientas de IA pueden generar código en segundos, el valor diferencial del tecnólogo radica en:
- Su capacidad de diseñar arquitecturas limpias y desacopladas.
- Su comprensión profunda de los sesgos y fundamentos matemáticos de los algoritmos.
- Su rigor ético y metodológico para auditar y verificar que ningún sistema crítico opere sin supervisión.

¡Felicitaciones por completar el recorrido de Procesamiento y Aprendizaje Automático en el ISFT N° 199!
---

## Autoevaluación Formativa y Caza de Código Alucinado

### Preguntas de Razonamiento Conceptual
1. ¿Por qué un agente IA debe "pensar en voz alta" (generar reasoning tokens) antes de invocar el endpoint `/version-space/step` para refinamiento interactivo?
2. ¿Qué síntoma de alucinación de IA detectarías si un agente llama a `/rules` sin verificar primero cuál es el conjunto de reglas actual?

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente código generado por un asistente de IA:

```python
# CÓDIGO CON BUG DE ORQUESTACIÓN GENERADO POR IA:
async def pipeline_agente():
    # IA generó esto sin estado compartido
    predicciones = []
    async for respuesta in agente_predict(energía_datos):
        predicciones.append(respuesta)

    # El agente hace predicciones SIN refinar hipótesis
    # No hay llamadas a /version-space/step ni /rules
```

**Diagnóstico del Revisor Humano:**
1. **Sin Refinamiento Interactivo:** El agente no mejora su comprensión a lo largo del tiempo.
2. **Sin Auditoría de Decisiones:** No registra las reglas que aplicó en cada paso.
3. **Corrección Obligatoria en energy-ml:**
   ```python
   async def pipeline_agente_integrador():
       # 1. Predicción inicial
       resultado_bayes = await client.post("/classify/bayes", json=telemetria)

       # 2. Refinamiento de hipótesis (Candidate-Elimination)
       refinamiento = await client.post("/version-space/step", json=resultado_bayes)

       # 3. Auditoría de reglas aplicadas
       reglas_actuales = await client.get("/rules")

       # 4. El agente "reflexiona" antes de la siguiente predicción
       proxima_telemetria = generar_siguiente_ejemplo()
       return await pipeline_agente_integrador()  # Recursión reflexiva
   ```

---
