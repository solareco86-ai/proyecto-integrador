# Cap 1.0: Mapa Conceptual de la Unidad 2 — Cómo Convergen Probabilidad → Bayes → k-NN → CART

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 1:** Arquitectura de Inferencia y Esquemas Pydantic  
**Duración:** 20 min (lectura + reflexión)  
**Propósito:** Antes de saltar a lecciones aisladas, entender cómo se conectan todos los conceptos.

---

## ¿Por Qué un Mapa Conceptual?

Hasta ahora viste en Unidad 0 y Unidad 1 lo fundamental: NumPy, Git, FastAPI. Ahora en **Unidad 2** te sumergirás en 4 algoritmos diferentes.

El riesgo es que cada lección se sienta como una "isla separada":
- Cap 1 → NumPy (vectores)
- Cap 2 → Probabilidad
- Cap 3 → Naive Bayes
- Cap 4 → k-NN
- Cap 5 → CART

**Sin conexión explícita**, tu cerebro memoriza recetas, no entiende la lógica profunda.

Este mapa conecta las piezas **antes** de estudiarlas en detalle.

---

## 1. La Pregunta Central: ¿Cómo Aprender de Datos?

```
                       DATOS HISTÓRICOS
                       (Telemetría de energy-ml)
                              │
                              ▼
                   ¿Qué algoritmo usar?
                              │
                ┌─────────────┼─────────────┐
                │             │             │
                ▼             ▼             ▼
            Probabilístico  Geométrico    Lógico
                │             │             │
                ▼             ▼             ▼
         Naive Bayes        k-NN         CART
         (Cap 3)          (Cap 4)        (Cap 5)
                │             │             │
                └─────────────┼─────────────┘
                              ▼
                    PREDICCIÓN EN ENERGÍA
                    (Falla? / Carga?)
```

Los tres algoritmos responden la misma pregunta (**"¿qué es?"**) pero desde ángulos diferentes:

1. **Bayes** pregunta: *"¿Cuál es la probabilidad P(Clase | Datos)?"* (razonamiento probabilístico)
2. **k-NN** pregunta: *"¿A quién se parece en el espacio?"* (similitud geométrica)
3. **CART** pregunta: *"¿Qué regla if/then me clasifica?"* (decisiones binarias)

---

## 2. Jerarquía Conceptual: De Matemática a Máquina

### Piso 0: Estadística Subyacente

```
Probabilidad Condicional: P(A|B)
        │
        ├─ Medias y Varianzas (μ, σ)
        │
        └─ Distribuciones: Gaussiana, Bernoulli
                │
                ▼
        ¿Cuál es más probable?
```

**Clave:** Sin entender P(A|B), Bayes es magia. Con P(A|B), es lógica inevitable.

---

### Piso 1: Datos Vectoriales (NumPy)

```
Telemetría en Voltaje [V₁, V₂, V₃, V₄] → Vector 1D
                                  ↓
¿Cómo la comparo con otros vectores?
                                  ↓
                    Distancia Euclidiana
                    ║ V - V' ║ = √[(v1-v1')² + ...]
                                  ↓
                    Broadcasting en NumPy
                    "Compara un vector con 1000 sin bucles"
```

**Clave:** Sin vectorización, k-NN es 300x más lento. Con vectorización, es viable en tiempo real.

---

### Piso 2: Los Tres Algoritmos Convergen

```
                    BAYES
                      │
         "Probabilidad a Posteriori"
         P(Falla | Voltaje, Temp, FP)
                      │
                      ├─ Asume independencia (condiciones)
                      ├─ Calcula P(x | Clase) para cada variable
                      └─ Multiplica probabilidades
                              ↓
                    "Normalizar y Reportar"
                    Resultado: [0.78, 0.15, 0.07] (soft)
---
                      k-NN
                      │
             "Similitud Geométrica"
             Busca los k=5 vecinos más cercanos
                      │
                      ├─ Estandariza variables
                      ├─ Calcula distancias a todos los históricos
                      └─ Vota: "¿Cuántos de los 5 son Falla?"
                              ↓
                    "Votación y Reportar"
                    Resultado: [3 Falla, 2 Normal] (hard majority)
---
                      CART
                      │
                "Reglas if/then"
             Si Voltaje > 220 y Temp > 80:
               └─ Falla
             Si Voltaje ≤ 220:
               └─ Normal
                      │
                      ├─ Particiona el espacio recursivamente
                      ├─ Usa entropía/Gini para elegir splits óptimos
                      └─ Genera árbol de decisión binario
                              ↓
                    "Seguir Rama y Reportar"
                    Resultado: ["Falla"] (hard, 1.0 o 0.0)
```

---

## 3. Tabla Comparativa Rápida (Referencia Gráfica)

```
┌─────────────────┬──────────────┬──────────────┬──────────────┐
│ Pregunta        │ BAYES        │ k-NN         │ CART         │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ ¿Qué es?        │ P(C|D)       │ Similitud    │ Regla        │
│ (Fundamento)    │ Probabilista │ Geométrica   │ Lógica       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Respuesta       │ Suave (0.78)│ Dura (3/5)   │ Binaria (1.0)│
│ (Certeza)       │ Probabilidad │ Votación     │ Sí/No        │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Complejidad     │ O(d)         │ O(N·d)       │ O(log N)     │
│ (Velocidad)     │ Rápido       │ Lento        │ Rápido       │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Interpretable   │ "78% seguro" │ "Como estos" │ "Si X ent."  │
│ (Explicable)    │ (difícil)    │ (mediano)    │ (fácil)      │
├─────────────────┼──────────────┼──────────────┼──────────────┤
│ Ideal para...   │ Datos pequ.  │ Firmas geo.  │ Reglas viz.  │
│                 │ Priors claros│ Millones     │ Execs.       │
└─────────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 4. Casos de Uso Reales en energy-ml

### Caso A: Diagnóstico de Falla Dieléctrica

**Datos:** Temperatura del aceite, corriente RMS, distorsión armónica  
**Pregunta:** "¿Falla inminente o normal?"

| Algoritmo | ¿Usar? | Razón |
|---|---|---|
| **Bayes** | ✅ **SÍ** | Probabilidades calibradas para decisiones de riesgo |
| **k-NN** | ⚠️ Opcional | Si hay 10k+ muestras históricas de fallas similares |
| **CART** | ⚠️ Opcional | Si necesitas reglas legibles para el operador |

**Decisión:** Bayes como base + Ensemble de los 3 para robustez.

---

### Caso B: Identificación de Carga (NILM)

**Datos:** Potencia activa, factor de potencia, corriente, distorsión  
**Pregunta:** "¿Qué equipo está encendido (motor, horno, ventilador, LED)?"

| Algoritmo | ¿Usar? | Razón |
|---|---|---|
| **Bayes** | ✅ **SÍ** | Multiclase (4 clases), probabilidades balanceadas |
| **k-NN** | ✅ **SÍ** | Firmas geométricas muy diferenciadas entre cargas |
| **CART** | ⚠️ Opcional | Si necesitas auditoría: "¿Por qué dijo motor?" |

**Decisión:** k-NN por velocidad + Bayes por confianza = Ensemble.

---

## 5. Flujo de Aprendizaje Recomendado en Unidad 2

```
SEMANA 1
  │
  ├─ Cap 0: NumPy (vectorización)
  │   └─ Objetivo: Rapidez en operaciones masivas
  │
  ├─ Cap 1: Pydantic + FastAPI lifespan
  │   └─ Objetivo: Cargar modelos eficientemente en memoria
  │
  ├─ Cap 2: Teoría Bayesiana
  │   └─ Objetivo: Entender P(A|B), priors, posteriors
  │
  └─ Cap 3: Naive Bayes en código
      └─ Objetivo: Implementar en energy-ml
SEMANA 2
  │
  ├─ Cap 4: Distancias y normalización (k-NN intro)
  │   └─ Objetivo: Razonamiento geométrico
  │
  ├─ Cap 5: k-NN en código + evaluación de métricas
  │   └─ Objetivo: Implementar + medir precisión/recall
  │
  ├─ **Cap 5.5: COMPARACIÓN de Bayes vs. k-NN** ← ESTÁS AQUÍ
  │   └─ Objetivo: ¿Cuál es mejor para TU problema?
  │
  └─ [Cap 6: Árboles de decisión si tiempo, else opcionali]
      └─ Objetivo: Tercer paradigma = más perspectivas
```

---

## 6. Verdades Profundas (Que Descubrirás)

### Verdad 1: "Independencia" de Bayes es Falsa
En energía real, **temperatura y corriente están correlacionadas** (ambas suben con carga). Naive Bayes asume que son independientes. ¿Por qué funciona? Porque la **"ingenuidad" actúa como regularizador**, evitando sobreajuste.

### Verdad 2: k-NN Necesita Datos de Calidad
k-NN solo ve "vecinos cercanos". Si tus datos históricos tienen mucho ruido o faltan casos raros, k-NN los memoriza sin aprender patrones. **Garbage in, garbage out.**

### Verdad 3: CART Crece Sin Control
Un árbol sin límite de profundidad memorizará perfectamente los 100 datos de entrenamiento... y fallará en el dato 101 del mundo real. **Max_depth es tu amigo.**

### Verdad 4: No Hay Ganador Absoluto
El "mejor" algoritmo depende **de tu problema específico, datos y restricciones**. No es matemática pura; es ingeniería.

---

## 7. Autoevaluación Conceptual: ¿Entiendes la Conexión?

### Pregunta 1
"Bayes calcula P(Falla|Datos). k-NN compara distancias. ¿Cuál es la conexión entre probabilidad y geometría?"

**Respuesta esperada:** 
- Bayes responde "¿cuál es la densidad de probabilidad aquí?" 
- k-NN responde "¿esto está cerca de un Falla conocida?"
- Ambos responden "¿falla o no?", solo que desde ópticas diferentes.

---

### Pregunta 2
"Si tienes 500 casos históricos de fallos y 50.000 operaciones normales, ¿qué sesgo tiene CART?"

**Respuesta esperada:** 
CART aprenderá "Normal" perfectamente (mayoría clara) pero memorizará los 500 fallos sin entender el patrón (minoría rara). Solución: usar **class_weight="balanced"** en Scikit-Learn.

---

## 8. Ejercicio Integrador: Dibuja Tu Propia Red

Antes de seguir, toma 10 minutos y **dibuja** (lápiz y papel, o Miro):

1. Centro: "Diagnóstico de Energía"
2. Tres ramas: Bayes, k-NN, CART
3. Para cada rama, agrega:
   - Pregunta fundamental
   - Fortalezas
   - Debilidades
   - Un caso de uso en energy-ml

**Esto es tu mapa mental. Personalizalo.**

---

## 9. Próximas Lecciones

- **Cap 1.1** (Pydantic): Tipado estricto para datos
- **Cap 2.1-2.2**: Fundamentos probabilísticos  
- **Cap 3**: Bayes en código
- **Cap 4**: k-NN en código
- **Cap 5**: Evaluación y métricas
- **Cap 5.5**: Comparación (esta lección te prepara)

**Objetivo a fin de semana:** Dominar vectorización + probabilidad + al menos 2 algoritmos.

---

## Resumen Visual (Una Imagen Vale 1000 Palabras)

```
                       UNIDAD 2: MACHINE LEARNING
                       
Fundamento:            NumPy           Probabilidad      Geometría
                        │                  │                 │
                        ▼                  ▼                 ▼
Algoritmo:             ───              Bayes              k-NN
                                          │
                                          ▼
                                    ¿P(Clase|Datos)?      
                                     (Probabilístico)      
                                    
                                    ────────────────       Lógica
                                                           │
                                                           ▼
                                                          CART
                                                    (Reglas if/then)

Aplicación:            Vectorización   Diagnóstico       Identificación
                       + Pydantic       Predictivo         de Cargas
                       + FastAPI       de Fallas          + Auditoría

Resultado:             Datos            Probabilidades    Reglas
                       Limpios &        Calibradas        Explicables
                       Tipados          + Confianza        + Binarias
```

---

**¡Vamos! Tu próxima lectura te enseñará a implementar esto en código. Mantén este mapa a la vista.**
