# Guía de Laboratorio — Lección 4.4: Panorama de Arneses de IA Agéntica: OpenAI Codex, Kimi Code y DeepSeek Harness (DPH)

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 4:** Ecosistema Avanzado de IA Agéntica: Claude Code, Aider y Arneses Autónomos  
**Carga horaria estimada:** 20 min  
**Prerrequisitos:** Haber completado las Lecciones 4.1 a 4.3.

---

## 1. ¿Qué es un "Arnés" (Harness) en Ingeniería de IA Agéntica?

Hasta este momento hemos interactuado con **asistentes de pair programming en consola**: herramientas diseñadas para dialogar con un programador humano que revisa cada sugerencia antes de aplicarla.

Sin embargo, en la frontera de la Inteligencia Artificial y la automatización de infraestructura, los ingenieros operan con **Arneses (Harnesses)**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     ESTRUCTURA DE UN ARNÉS AGÉNTICO                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. LLM (Cerebro)       ◄──► Pesos neuronales (razonamiento y código)   │
│ 2. Loop de Control     ◄──► Ciclo ReAct (Pensar -> Actuar -> Observar) │
│ 3. Sandbox / Runtime   ◄──► Contenedor Docker / VM con Bash y Git      │
│ 4. Sensores y Rieles   ◄──► Linters, test runners (Pytest), AST y métricas
└────────────────────────────────────────────────────────────────────────┘
```

Un **arnés de IA** es el entorno de software que encapsula a un modelo para permitirle resolver tareas de ingeniería de forma **completamente autónoma (desatendida)**:
* Recibe un reporte de error (*bug report* o *issue* de GitHub).
* Clona el repositorio en un entorno seguro y aislado (*sandbox*).
* Ejecuta los tests actuales, observa los errores en consola y planea una solución.
* Edita los archivos, vuelve a correr los tests y verifica si todos pasan en verde.
* Genera el Pull Request final sin intervención humana directa.

---

## 2. OpenAI Codex y los Orígenes de la Síntesis de Código

Históricamente, **Codex** (creado por OpenAI a partir de GPT-3) fue el modelo que inauguró la generación moderna de código y sirvió como motor inicial de GitHub Copilot.

* **Evolución Actual:** Hoy en día, la arquitectura de Codex se ha integrado en el **GitHub Copilot CLI** y en los agentes de automatización de GitHub Actions.
* **Enfoque de Integración:** Opera estrechamente integrado con el ecosistema de Microsoft y GitHub, permitiendo revisiones automáticas de PRs, resúmenes de commits y sugerencias inline dentro del editor.

---

## 3. Kimi Code: El Dominio del Contexto Masivo (200k a 2M Tokens)

Desarrollado por **Moonshot AI**, **Kimi** se ha transformado en un estándar internacional de referencia por su habilidad de procesar **ventanas de contexto ultralargas** (desde 200.000 hasta 2 millones de tokens con fidelidad matemática):

* **Kimi Code CLI / Harness:** Diseñado para escenarios donde la base de código o los manuales técnicos son tan masivos que ningún asistente tradicional puede cargarlos sin olvidar detalles críticos.
* **Casos de Uso Típicos:**
  * Migraciones completas de versiones de frameworks (ej: migrar un proyecto entero de Django a FastAPI).
  * Auditoría forense de millones de líneas de registros (*logs*) de redes eléctricas industriales.
  * Análisis de especificaciones técnicas y patentes de hardware sin necesidad de podar fragmentos.

---

## 4. DPH: DeepSeek Harness

Con la irrupción de los modelos de código abierto y alta eficiencia de DeepSeek, la comunidad de investigación y desarrollo de software libre creó **DPH (DeepSeek Harness)**:

* **¿Para qué se utiliza?:** Es un arnés de evaluación y ejecución autónoma diseñado para someter a modelos de razonamiento (como DeepSeek-V3 y R1) a pruebas rigurosas en benchmarks estándar de la industria, como **SWE-bench** (un conjunto de miles de problemas reales extraídos de repositorios de código abierto de GitHub).
* **Flujo Operativo de DPH:**
  1. Descarga el issue reportado en un issue tracker.
  2. Levanta un contenedor Docker con el entorno del repositorio.
  3. Ejecuta el bucle agéntico de auto-reparación hasta que la suite de pruebas del proyecto pasa en verde.
  4. Mide la tasa de éxito y el consumo de tokens empleado.

---

## 5. Matriz Comparativa: Asistentes Interactivos vs. Arneses Autónomos

| Herramienta | Categoría | Interacción | Caso de Uso Recomendado |
| :--- | :--- | :--- | :--- |
| **OpenCode** | Asistente CLI | Humano-en-el-bucle | Desarrollo diario libre sin costo |
| **Antigravity CLI** | Asistente CLI + Web | Humano-en-el-bucle | Asistencia multimodal y documentación web ($5) |
| **Claude Code** | Asistente CLI | Humano-en-el-bucle | Arquitectura y refactor corporativo ($20) |
| **Aider** | Asistente CLI Git | Humano-en-el-bucle | Edición precisa y commits automáticos (DeepSeek) |
| **Copilot CLI / Codex** | Arnés Integrado | Asistido / Inline | Autocompletado y revisiones en GitHub |
| **Kimi Code** | Arnés de Contexto Masivo | Sesión Analítica | Auditoría de repositorios gigantes y manuales |
| **DPH (DeepSeek Harness)**| Arnés Autónomo | Desatendido / Batch | Auto-resolución de issues y benchmarking |

---

## 6. Cierre del Ecosistema de Agentes y Puerta de Entrada a FastAPI

Has adquirido un mapa mental completo y profesional de la IA agéntica:
1. Sabes cómo programar con herramientas libres sin costo (**OpenCode**).
2. Dispones de la mejor opción precio/calidad para tu vida académica (**Antigravity CLI** con navegador).
3. Conoces el estándar corporativo (**Claude Code**) y sus límites de cuota.
4. Entiendes las entrañas de los agentes y cómo aprovechar la API más económica (**Aider con DeepSeek**).
5. Reconoces el papel transformador de los **arneses autónomos** (Codex, Kimi y DPH).

Ahora que dominas la terminal, Git y el pair programming agéntico, estás listo para dar el salto definitivo: en el **Capítulo 5**, utilizaremos todo este conocimiento para transformar los algoritmos y pipelines de `energy-ml` en un **Servicio Web de Inferencia en Tiempo Real con FastAPI**.
