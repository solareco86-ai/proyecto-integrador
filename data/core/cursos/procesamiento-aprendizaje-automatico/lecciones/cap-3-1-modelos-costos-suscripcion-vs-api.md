# Guía de Laboratorio — Lección 3.1: Economía de la IA Agéntica: Suscripciones Fijas vs. Pago por Uso

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** El Cuarteto de IA Agéntica: OpenCode, Antigravity CLI, Claude Code y Aider  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado el Capítulo 2 (Flujo de Trabajo Profesional con Git y GitHub CLI sobre `energy-ml`).

---

## 1. De la Tríada al Cuarteto de IA Agéntica

En la práctica profesional de desarrollo de software asistido por Inteligencia Artificial, los entornos ya no se limitan a un único modelo o a una ventana de chat en un navegador. Hoy en día, los ingenieros y científicos de datos operan con **agentes autónomos y semi-autónomos en línea de comandos (CLI)**, capaces de leer el árbol de archivos, ejecutar diagnósticos, correr pruebas unitarias y formular commits directamente en el repositorio local.

Para el estudiante de la Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial del ISFT N° 199, este ecosistema se articula en un **cuarteto estratégico de herramientas**, ordenadas según accesibilidad, costo, aplicabilidad académica y estándares de la industria:

1. **OpenCode (1er Lugar — Base Libre):** Asistente *open source*, multi-modelo y con opciones de cuota gratuita sin tarjeta de crédito. Ideal para comenzar a programar de inmediato sin barreras de entrada.
2. **Antigravity CLI (2do Lugar — Recomendado para Estudiantes):** La mejor relación precio/calidad del mercado mediante la tarifa estudiantil de **5 USD/mes** (descuento de 15 USD por 12 meses sobre el plan Pro). Incorpora control de navegador web integrado (`/browser`), inspección multi-agente y capacidades multimodales.
3. **Claude Code (3er Lugar — Estándar Corporativo, Opcional):** El agente de referencia desarrollado por Anthropic, ampliamente demandado en empresas de tecnología. Opera bajo suscripción de **20 USD/mes** con una cuota de consultas estricta que exige gran disciplina técnica. Recomendado para quienes ya trabajan en el sector.
4. **Aider (4to Lugar — Arquitectura Agéntica Interna, Opcional):** El agente pionero de pair programming en consola, ideal para comprender el funcionamiento interno de la IA agéntica (mapa de repositorio con AST, edición quirúrgica de diffs y benchmarking). Se utiliza con **pago por uso** cargando **2 USD** en la API de **DeepSeek**, la opción más económica y competitiva de la actualidad.
5. **Ecosistema de Arneses Complementarios:** Más allá de las herramientas interactivas de uso diario, exploraremos los arneses de ejecución autónoma como **Codex / GitHub Copilot CLI**, **Kimi Code** y **DeepSeek Harness (DPH)**.

---

## 2. Modelos Financieros: Suscripción Fija vs. Pago por Uso (Pay-as-you-go)

Uno de los errores más comunes al iniciarse en la IA agéntica es no comprender cómo se cobra el acceso al cómputo cognitivo. Existen dos modelos financieros fundamentales:

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│                    MODELOS DE ACCESO A MODELOS DE IA                        │
├───────────────────────────────┬─────────────────────────────────────────────┤
│ 1. Suscripción Mensual Fija   │ Se abona un valor fijo por mes ($5 a $20).  │
│    (Flat Subscription)        │ Cuota de mensajes o créditos renovables.    │
│                               │ Ejemplos: Antigravity ($5 est.), Claude ($20)│
├───────────────────────────────┼─────────────────────────────────────────────┤
│ 2. Pago por Uso (API Tokens)  │ Se paga exclusivamente por token consumido. │
│    (Pay-as-you-go)            │ Sin costo fijo mensual, pero requiere       │
│                               │ cautela y límites de saldo prepago.         │
│                               │ Ejemplo: DeepSeek API, OpenAI API.          │
└───────────────────────────────┴─────────────────────────────────────────────┘
```

### Ventajas y Desafíos de Cada Modelo

* **Suscripción Fija:**
  * *Ventaja:* Predictibilidad total. Sabes con exactitud cuánto gastas al mes ($5 en Antigravity con descuento estudiantil) sin sorpresas en el resumen bancario.
  * *Riesgo:* Límites de velocidad (*rate limits*). Si disparas demasiadas consultas en un lapso corto, la plataforma puede pausar tu acceso por unas horas.
* **Pago por Uso (API):**
  * *Ventaja:* Pagas únicamente por lo que tu agente lee y escribe. Si un fin de semana no programas, no gastas nada. Para tareas puntuales de bajo volumen, puede costar fracciones de centavo de dólar.
  * *Riesgo:* Desborde de gasto involuntario (*runaway loops*). Si dejas un agente en un bucle autónomo sin supervisión ni poda de contexto, puede consumir saldo rápidamente.

---

## 3. DeepSeek API: La Opción Más Competitiva y el Descuento Horario

En el terreno del pago por uso, **DeepSeek** ha revolucionado la industria al ofrecer capacidades comparables a modelos de frontera a una fracción minúscula de su costo:

* **Tarifa Base de DeepSeek:**
  * Entrada (Input Tokens): Aproximadamente **0,14 USD** por millón de tokens (con caché de contexto hasta 0,014 USD).
  * Salida (Output Tokens): Aproximadamente **0,28 USD** por millón de tokens.
  * *Comparación:* Modelos equivalentes de OpenAI o Anthropic suelen costar entre 3 y 15 USD por millón de tokens de entrada (10 a 50 veces más caros).

### El Descuento de Horario Reducido (*Off-Peak Discount*)

DeepSeek aplica un incentivo tarifario significativo durante sus horas valle (*off-peak*):
* **Ventana Horaria Valle:** De **16:30 a 00:30 UTC** de cada día.
* **Horario Local en Argentina (UTC-3):** De **13:30 a 21:30 hs**.
* **Beneficio:** Durante esta franja horaria, el costo por token de entrada y salida se reduce automáticamente en un **50%**.

Esto significa que una sesión de desarrollo técnico con Aider durante la tarde o noche argentina rinde el doble por el mismo saldo.

---

## 4. Regla de Oro para Estudiantes: Cautela y Saldo Prepago Controlado

> ⚠️ **Principio de Seguridad Financiera:**  
> Jamás vincules una tarjeta de crédito a una API sin establecer **límites estrictos de gasto mensual (*hard spending limits*)**. En este curso trabajaremos bajo el principio de **saldo prepago controlado**.

### ¿Cómo configuraremos la prueba con DeepSeek?
1. Se crea la cuenta en la plataforma para desarrolladores de DeepSeek.
2. Se realiza una recarga mínima de **2 USD** (saldo suficiente para semanas enteras de desarrollo si se siguen las buenas prácticas de poda de contexto).
3. No se activa la recarga automática (*auto-reload* desactivado). Si el saldo de 2 USD llega a cero, el agente simplemente se detiene sin generar deudas imprevistas.

---

## 5. Anatomía de una Instrucción Técnica y Conservación de Tokens

Tanto en entornos de cuota fija como en pago por uso, la regla número uno de la ingeniería de software moderna es **evitar el desperdicio de tokens**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ANATOMÍA DE UNA INSTRUCCIÓN TÉCNICA                  │
├─────────────────┬──────────────────────────────────────────────────────┤
│ 1. Contexto     │ Archivo específico y función sobre la que actuar     │
│ 2. Objetivo     │ Tarea concreta (crear, refactorizar, auditar, test)   │
│ 3. Restricciones│ Restricciones técnicas (tipado estricto, sin libs ext)│
│ 4. Verificación │ Cómo se comprobará el resultado (test, salida CLI)   │
└─────────────────┴──────────────────────────────────────────────────────┘
```

* **Instrucción Vaga (Desperdicio Masivo):**  
  *"Arregla el código de energy-ml que tira error."*  
  *(Fuerza al agente a leer decenas de archivos, alucinar librerías y consumir miles de tokens innecesarios).*
* **Instrucción Técnica Precisa ($0 Desperdicio):**  
  *"En `energy-ml/src/pipeline.py`, implementa la función `validar_formato(df: pd.DataFrame) -> bool`. Debe verificar que las columnas `timestamp` y `kwh` no contengan valores nulos. Retorna `True` si es válido o lanza `ValueError` con el detalle del campo faltante. No instales dependencias adicionales."*

---

## 6. Cuadro Resumen del Ecosistema de Agentes

| Herramienta | Tipo | Modelo de Costo | Foco Principal | Audiencia Sugerida |
| :--- | :--- | :--- | :--- | :--- |
| **OpenCode** | CLI / Open Source | Gratuito / Multi-proveedor | Desarrollo libre sin barreras | Todos los estudiantes (Inicio) |
| **Antigravity CLI** | CLI + Browser | Suscripción $5/mes (Estudiantes) | Asistencia multimodal y navegador | Todos los estudiantes (Estándar) |
| **Claude Code** | CLI Corporativo | Suscripción $20/mes (Pro/Team) | Razonamiento enterprise riguroso | Estudiantes trabajando en empresas |
| **Aider** | CLI Git-native | Pago por uso (DeepSeek API $2) | Arquitectura interna y repomap | Aprendizaje técnico profundo |
| **Codex / Kimi / DPH** | Arneses autónomos | Variable / API / Local | Benchmarking y tareas batch | Especialización avanzada |

En la siguiente lección instalaremos y configuraremos **OpenCode**, nuestro punto de partida libre de costo para comenzar a programar con agentes en la terminal.
