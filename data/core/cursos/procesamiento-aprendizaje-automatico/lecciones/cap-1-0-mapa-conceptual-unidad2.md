# Lección 1.0: Fundamentos del Aprendizaje Automático: Concepto, Técnicas, Búsqueda y Diseño de Modelos

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo Intro:** Bloque Aprendizaje Automático: Fundamentos Teóricos y Mapa Conceptual  
**Carga horaria estimada:** 35 min  
**Prerrequisitos:** Haber completado la Unidad 0 (Diagnóstico de conocimientos previos) y Unidad 1 (Fundamentos de entorno y desarrollo).  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10, Espacio 12: *«Bloque Aprendizaje automático: Concepto de Aprendizaje automático. Técnicas de aprendizaje automático. Objetivos de la tarea de Aprendizaje. El aprendizaje como una tarea de búsqueda. Sub tareas relacionadas con la tarea de aprendizaje. Diseño de modelos. Evaluación del modelo. Aprendizaje Inductivo y Deductivo»*).

---

## 1. Concepto de Aprendizaje Automático

El **Aprendizaje Automático (*Machine Learning*)** es la disciplina de la Ciencia de la Computación y la Inteligencia Artificial orientada a la construcción de sistemas capaces de mejorar automáticamente su desempeño en una tarea a través de la experiencia empírica acumulada en datos, sin requerir reglas programadas explícitamente para cada contingencia.

La definición operativa más rigurosa y extendida fue establecida por Tom Mitchell (1997):
> *«Se dice que un programa de computadora aprende de la experiencia $E$ respecto a alguna clase de tareas $T$ y medida de rendimiento $P$, si su desempeño en las tareas en $T$, medido por $P$, mejora con la experiencia $E$»*.

```text
PARADIGMA TRADICIONAL (Sistemas basados en reglas):
Reglas Manuales (Código) + Datos de Entrada ────────> Resultados

PARADIGMA DE APRENDIZAJE AUTOMÁTICO:
Datos de Entrada + Respuestas / Recompensas ────────> Modelo Aprendido (Reglas / Pesos)
                                                                │
Nuevos Datos de Telemetría ────────────────────────────────────┘ ────> Inferencia / Predicción
```

### Ejemplo en el contexto de `energy-ml`:
* **Tarea $T$:** Identificar qué electrodoméstico industrial encendió a partir de un salto transitorio de potencia activa y reactiva.
* **Experiencia $E$:** Registros históricos de telemetría eléctrica con firmas electromagnéticas previas.
* **Medida de rendimiento $P$:** Coeficiente $F_1$-score y exactitud (*accuracy*) en la clasificación de maquinaria en planta sin incurrir en falsas alarmas.

---

## 2. Técnicas de Aprendizaje Automático

El universo de técnicas de aprendizaje automático se estructura según la presencia de retroalimentación y la naturaleza del conocimiento inducido:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   TAXONOMÍA DE TÉCNICAS DE MACHINE LEARNING            │
├───────────────────────────┬────────────────────────────────────────────┤
│ 1. Aprendizaje            │ Disponibilidad de pares (entrada, etiqueta)│
│    Supervisado            │ - Clasificación (Bayes, k-NN, CART)        │
│                           │ - Regresión (Árboles continuos, métricas)  │
├───────────────────────────┼────────────────────────────────────────────┤
│ 2. Aprendizaje            │ Datos crudos sin etiquetas de salida       │
│    No Supervisado         │ - Agrupamiento particional (k-medias)      │
│                           │ - Agrupamiento jerárquico (Aglomerativo)   │
│                           │ - Detección de patrones y perfiles         │
├───────────────────────────┼────────────────────────────────────────────┤
│ 3. Aprendizaje            │ Decisiones secuenciales y retroalimentación│
│    por Refuerzo           │ - Procesos de Markov, Bellman, Q-Learning  │
│                           │ - Políticas óptimas de control y despacho  │
├───────────────────────────┼────────────────────────────────────────────┤
│ 4. Aprendizaje Simbólico  │ Extracción de hipótesis interpretables     │
│    e Inductivo Formal     │ - Espacio de Versiones (Candidate-Elim.)   │
│                           │ - Algoritmo AQ (Cobertura secuencial)      │
│                           │ - Programación Lógica Inductiva (FOIL)     │
├───────────────────────────┼────────────────────────────────────────────┤
│ 5. Optimización           │ Búsqueda estocástica en espacios complejos │
│    Evolutiva (Genéticos)  │ - Selección, cruzamiento, mutación, fitness│
└───────────────────────────┴────────────────────────────────────────────┘
```

---

## 3. Objetivos de la Tarea de Aprendizaje

El objetivo primordial del aprendizaje automático **no es memorizar** los datos históricos observados, sino alcanzar una **alta capacidad de Generalización**:

1. **Aproximación de la Función Objetivo Desconocida:** Existe un fenómeno físico real $f: X \to Y$ (ej: la física de impedancia de una red trifásica) que genera los datos. El objetivo del aprendizaje es inducir una función hipótesis $h \approx f$ que se comporte con alta fidelidad.
2. **Minimización del Error de Generalización:** Se busca que el error esperado ante observaciones futuras nunca antes vistas (*Out-of-Sample Error*) sea mínimo, evitando el **Sobreajuste (*Overfitting*)** (memorización de ruido) y el **Subajuste (*Underfitting*)** (incapacidad de capturar el patrón).
3. **Equilibrio entre Explicabilidad y Rendimiento:** En aplicaciones críticas de ingeniería y gestión institucional, los modelos deben ofrecer trazabilidad interpretable (ej: reglas lógicas y árboles) para validar normativas y auditorías técnicas.

---

## 4. El Aprendizaje como una Tarea de Búsqueda

Cualquier algoritmo de aprendizaje automático puede formalizarse matemáticamente como un **problema de búsqueda**:

* **Espacio de Hipótesis ($\mathcal{H}$):** Es el conjunto completo de todas las posibles funciones, reglas o combinaciones de parámetros que el modelo puede representar (por ejemplo, el conjunto de todos los árboles de decisión de profundidad $\le 5$, o todos los hiperplanos en $\mathbb{R}^D$).
* **Navegación en el Espacio de Búsqueda:** El algoritmo evalúa muestras de entrenamiento y navega a través de $\mathcal{H}$ guiado por una función de costo o aptitud para localizar la hipótesis $h \in \mathcal{H}$ más consistente con los datos observados.

```text
         ┌─────────────────────────────────────────────────────────┐
         │ ESPACIO DE HIPÓTESIS H                                  │
         │                                                         │
         │    h₁ (subajuste)          h* (hipótesis óptima)        │
         │         \                     ▲                         │
         │          \                    │ Búsqueda guiada por     │
         │           \                   │ sesgo inductivo         │
         │            ▼                  │                         │
         │        h₂ ─────────> h₃ ──────┘                         │
         │                                   h_overfit (ruido)     │
         └─────────────────────────────────────────────────────────┘
```

### El Rol Indispensable del Sesgo Inductivo (*Inductive Bias*)
Un aprendiz sin ningún supuesto a priori (*unbiased learner*) no tiene fundamento matemático para clasificar una muestra no observada previamente; cualquier predicción sería igualmente arbitraria.
El **Sesgo Inductivo** es el conjunto de supuestos y restricciones que el algoritmo adopta para generalizar más allá de los datos de entrenamiento:
* **Naive Bayes:** Asume independencia condicional entre características dado el target.
* **k-NN:** Asume que muestras cercanas en la métrica euclidiana comparten la misma etiqueta.
* **CART:** Asume que el espacio puede particionarse eficazmente mediante hiperplanos ortogonales a los ejes (reglas binarias univariadas).

---

## 5. Metodología de Diseño de Modelos

El Anexo I enfatiza el *«Diseño de modelos»* como una competencia central de la formación técnica. Diseñar un modelo de machine learning involucra cuatro decisiones estratégicas secuenciales:

```text
ETAPAS DEL DISEÑO DE UN MODELO:
┌────────────────────────────────────────────────────────────────────────┐
│ Etapa 1: Elección de la Experiencia de Entrenamiento                   │
│ - ¿Datos supervisados etiquetados, telemetría cruda o recompensas?     │
│ - Representatividad de la muestra y prevención de sesgos.              │
├────────────────────────────────────────────────────────────────────────┤
│ Etapa 2: Elección de la Función Objetivo a Aprender                    │
│ - ¿Clasificación discreta (falla/normal), valor continuo o cluster?   │
│ - Definición de la métrica de éxito (F1-score, MAE, Silueta).          │
├────────────────────────────────────────────────────────────────────────┤
│ Etapa 3: Elección de la Representación de la Función Objetivo          │
│ - Selección del espacio de hipótesis H (probabilidades, reglas lógicas,│
│   árboles CART, centroides de k-medias o cromosomas genéticos).        │
├────────────────────────────────────────────────────────────────────────┤
│ Etapa 4: Elección del Algoritmo de Búsqueda y Ajuste                   │
│ - Procedimiento de optimización: Descenso de gradiente, cobertura      │
│   secuencial, división recursiva de entropía o algoritmos genéticos.   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 6. Mapa de Convergencia: Cómo se Integran las Unidades del Curso

En las lecciones subsiguientes profundizaremos de forma práctica en cada componente de esta estructura:
* **Capítulo 2:** Deducción vs Inducción y Subtareas del ciclo de Machine Learning (partición temporal, preparación de datos e inferencia).
* **Capítulos 3 y 4:** Modelos supervisados en producción con Naive Bayes y k-NN.
* **Capítulo 5:** Métricas rigurosas de evaluación y flujo TDD con FastAPI y `energy-ml`.
* **Capítulo 6:** Modelos no supervisados (k-medias, agrupamiento aglomerativo), aprendizaje por refuerzo (Q-Learning) y optimización con algoritmos genéticos.
* **Unidad 3:** Inteligencia neuro-simbólica (Espacio de Versiones, reglas formales AQ/FOIL, explicabilidad CART) y orquestación con servidores MCP y agentes autónomos.

---

## Autoevaluación Formativa

1. ¿Por qué se afirma que el aprendizaje automático es formalmente una tarea de búsqueda en un espacio de hipótesis?
2. ¿Qué ocurriría si un algoritmo no tuviera ningún sesgo inductivo (*inductive bias*) al momento de predecir sobre datos no vistos?
3. En el marco de `energy-ml`, describe cuáles serían las 4 etapas de diseño de un modelo para diagnosticar pérdidas energéticas en transformadores.
