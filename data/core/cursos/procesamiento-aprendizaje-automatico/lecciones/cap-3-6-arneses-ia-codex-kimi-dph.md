# Guía de Laboratorio — Lección 3.6: Ecosistema de Arneses de IA Agéntica: OpenAI Codex, Kimi Code y DeepSeek Harness (DPH)

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** El Cuarteto de IA Agéntica: OpenCode, Antigravity CLI, Claude Code y Aider  
**Carga horaria estimada:** 20 min  
**Prerrequisitos:** Haber completado las Lecciones 3.1 a 3.5.

---

## 1. ¿Qué es un "Arnés" (Harness) en IA Agéntica?

A lo largo del capítulo hemos interactuado con asistentes interactivos de consola (OpenCode, Antigravity CLI, Claude Code y Aider). Sin embargo, en la literatura avanzada de Inteligencia Artificial y en la ingeniería de sistemas autónomos aparece con frecuencia el término **Harness (Arnés)**.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     ESTRUCTURA DE UN ARNÉS AGÉNTICO                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. LLM (Cerebro)       ◄──► Pesos neuronales (razonamiento, código)   │
│ 2. Loop de Control     ◄──► Ciclo ReAct (Pensar -> Actuar -> Observar) │
│ 3. Sandbox / Runtime   ◄──► Entorno aislado (Docker, Bash, Git)        │
│ 4. Sensores y Rieles   ◄──► Linters, test runners, AST y métricas      │
└────────────────────────────────────────────────────────────────────────┘
```

Un **arnés de IA** es la infraestructura de software que rodea a un modelo de lenguaje para permitirle operar de forma autónoma sobre un entorno de cómputo real:
* Le provee herramientas de lectura y escritura en disco.
* Controla las llamadas a la terminal y previene comandos peligrosos (`rm -rf`, fugas de credenciales).
* Captura las salidas de error (*tracebacks*) y las retroalimenta al modelo para que se auto-repare.
* Mide el éxito de la tarea mediante suites de pruebas automatizadas (como el benchmark SWE-bench).

---

## 2. OpenAI Codex y los Inicios de la Generación de Código

Históricamente, **Codex** (desarrollado por OpenAI a partir de GPT-3) fue el modelo que inauguró la era de la síntesis de código moderna y sirvió como motor original de GitHub Copilot.

* **Evolución Actual:** Hoy, la tecnología de Codex ha evolucionado hacia el **GitHub Copilot CLI** y arneses de ejecución en el ecosistema de Visual Studio Code y GitHub Actions.
* **Enfoque de Integración:** Opera estrechamente ligado al repositorio remoto de GitHub, permitiendo disparar revisiones automáticas de código (*Copilot pull request reviews*) y sugerencias contextuales inline.

---

## 3. Kimi Code: El Poder del Contexto Masivo y Razonamiento Largo

Desarrollado por **Moonshot AI**, **Kimi** se ha convertido en un referente internacional por su capacidad pionera de procesar **ventanas de contexto masivas** (desde 200.000 hasta 2 millones de tokens de forma fluida):

* **Kimi Code CLI / Harness:** Diseñado para proyectos donde el código fuente o la documentación técnica es tan extensa que ningún modelo tradicional podría cargarla en memoria sin olvidar detalles.
* **Caso de Uso Ideal:** Auditoría de migraciones completas de bases de datos, lectura de manuales técnicos de cientos de páginas o análisis forense de miles de líneas de registros (*logs*) de sistemas industriales sin pérdida de atención (*needle in a haystack*).

---

## 4. DPH: DeepSeek Harness

Con el auge de los modelos de razonamiento abierto de DeepSeek (como DeepSeek-V3 y DeepSeek-R1), la comunidad científica y los equipos de infraestructura crearon **DPH (DeepSeek Harness)**:

* **¿Para qué sirve?:** Es un arnés de evaluación y ejecución autónoma que toma un repositorio de código abierto con un *issue* o error reportado, clona el repositorio en un contenedor Docker aislado, ejecuta los tests que fallan, invoca a DeepSeek para que razone sobre el problema, aplica el parche y verifica si todos los tests pasan en verde.
* **Importancia Académica:** Permite medir cuantitativamente qué tan capaz es un modelo de resolver problemas reales de ingeniería de software sin intervención humana.

---

## 5. Matriz Comparativa: Asistentes Interactivos vs. Arneses Autónomos

| Herramienta | Tipo | Interacción Principal | Caso de Uso Típico |
| :--- | :--- | :--- | :--- |
| **OpenCode** | Asistente CLI | Humano-en-el-bucle (Human-in-the-loop) | Pair programming diario gratuito |
| **Antigravity CLI** | Asistente CLI + Browser | Humano-en-el-bucle con navegación | Desarrollo intensivo con plan estudiantil ($5) |
| **Claude Code** | Asistente CLI | Humano-en-el-bucle corporativo | Arquitectura y refactor enterprise |
| **Aider** | Asistente CLI Git | Humano-en-el-bucle con commits atómicos | Tareas quirúrgicas por tokens (DeepSeek API) |
| **Codex / Copilot CLI** | Arnés integrado | Inline / Asistente de IDE | Autocompletado y revisiones en GitHub |
| **Kimi Code** | Arnés de contexto largo | Sesión analítica masiva | Auditoría de código masivo y documentación |
| **DPH (DeepSeek Harness)** | Arnés autónomo batch | Ejecución desatendida / Benchmarking | Auto-reparación de repositorios e issues |

---

## 6. Conclusión del Capítulo 3

Has adquirido una visión integral, realista y desmitificada del ecosistema de IA agéntica:
1. Conoces las opciones gratuitas (**OpenCode**) para empezar sin fricción financiera.
2. Identificas la mejor opción precio/calidad para tu trayectoria estudiantil (**Antigravity CLI** a 5 USD/mes con soporte web).
3. Comprendes el estándar corporativo (**Claude Code**) y sus restricciones de cuota.
4. Sabes cómo utilizar **Aider con la API de DeepSeek** cargando 2 USD controlados y aprovechando el descuento de horario nocturno.
5. Reconoces el rol de los **arneses autónomos** (Codex, Kimi Code y DPH) en el futuro de la ingeniería de software.

En el **Capítulo 4**, utilizaremos este conjunto de herramientas para dar el siguiente salto profesional: transformar nuestros scripts de consola de `energy-ml` en **servicios web robustos mediante FastAPI**.
