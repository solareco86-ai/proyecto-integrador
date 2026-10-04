# Guía de Laboratorio — Lección 3.1: Economía de la IA Agéntica: Suscripciones Fijas vs. Pago por Uso

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** Asistentes de IA para Estudiantes: OpenCode y Antigravity CLI  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado el Capítulo 2 (Flujo de Trabajo Profesional con Git y GitHub CLI sobre `energy-ml`).

---

## 1. El Ecosistema de Asistentes para Estudiantes de Nivel Superior

En la formación profesional de la Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial del ISFT N° 199, el desarrollo de software asistido por IA no es un juguete ni un chat genérico. Es una **herramienta de ingeniería en línea de comandos (CLI)** que se integra directamente con el sistema de archivos, el intérprete de Python y el repositorio Git.

Para garantizar que **todo estudiante** pueda desarrollar sus prácticas sin encontrarse con barreras de pago o requisitos financieros excluyentes, dividimos nuestro estudio en dos bloques estratégicos:
* **Capítulo 3 (Asistentes Estudiantiles Base):** Nos concentramos en profundidad en **OpenCode** (herramienta libre y de cuota gratuita sin tarjeta) y **Antigravity CLI** (la mejor relación precio/calidad del mercado mediante la tarifa estudiantil de 5 USD/mes y navegación web integrada).
* **Capítulo 4 (Ecosistema Avanzado y Corporativo):** Analizamos las opciones para entornos de trabajo profesionales: **Claude Code** (corporativo), **Aider** (arquitectura interna por pago por uso con API DeepSeek) y el panorama de **Arneses Autónomos** (Codex, Kimi y DPH).

---

## 2. Modelos Financieros: Suscripción Fija vs. Pago por Uso (Pay-as-you-go)

Uno de los conceptos centrales que todo futuro profesional debe dominar es la economía del cómputo cognitivo:

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

### Principio de Inclusión y Accesibilidad en el ISFT N° 199
1. **Punto de Partida sin Tarjeta (Costo $0):** Todo estudiante comienza con **OpenCode** utilizando proveedores comunitarios o claves gratuitas de Google AI Studio / modelos locales con Ollama.
2. **Inversión Optimizada para Estudiantes ($5 USD/mes):** Aquellos que deseen modelos de frontera y capacidades de navegador utilizan **Antigravity CLI** gracias al descuento educativo de 15 USD por 12 meses sobre el plan Pro.
3. **Control Total de Saldo:** En los capítulos posteriores aprenderemos a utilizar APIs de pago por uso (DeepSeek) cargando únicamente 2 USD prepago y aprovechando descuentos de horario valle.

---

## 3. Anatomía de una Instrucción Técnica y Poda de Contexto

Tanto en entornos gratuitos como pagos, la regla de oro de la ingeniería de software es **evitar el desperdicio de tokens y las alucinaciones**:

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

* **Instrucción Vaga (Desperdicio y Alucinación):**  
  *"Arregla el código de energy-ml que tira error."*
* **Instrucción Técnica Precisa ($0 Desperdicio):**  
  *"En `src/pipeline.py`, implementa la función `validar_formato(df: pd.DataFrame) -> bool`. Debe verificar que las columnas `timestamp` y `kwh` no contengan valores nulos. Retorna `True` si es válido o lanza `ValueError` con el detalle del campo faltante. No instales dependencias adicionales."*

---

## 4. Cuadro Comparativo de Asistentes Estudiantiles

| Criterio | OpenCode | Antigravity CLI (`agy`) |
| :--- | :--- | :--- |
| **Licencia** | 100% Open Source | Propietario (Google DeepMind) |
| **Costo para Estudiantes** | **Gratuito ($0)** | **5 USD / mes** (Tarifa Estudiantil) |
| **Requisito de Tarjeta** | **No** (usando Zen / Free Tiers) | Sí (suscripción con descuento) |
| **Capacidades Especiales** | Multi-proveedor (Groq, Ollama, Zen) | Multi-agente, navegación web (`/browser`) |
| **Integración Git** | Edición modular y diffs | Diffs quirúrgicos y ejecución de tests |

En la siguiente lección instalaremos y configuraremos **OpenCode** para poner en marcha nuestro primer asistente de consola totalmente libre de costo.
