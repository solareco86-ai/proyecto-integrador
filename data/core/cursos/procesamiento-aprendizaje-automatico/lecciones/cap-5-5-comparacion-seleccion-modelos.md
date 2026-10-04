# Lección 5.5: Comparación Crítica y Selección de Modelos — ¿Cuándo Usar Bayes, k-NN o CART?

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 5:** Evaluación Rigurosa y TDD Asistido por Agentes en `energy-ml`  
**Carga horaria estimada:** 40 min  
**Prerrequisitos:** Haber completado Capítulos 3-4 (Bayes, k-NN, CART).

---

## Objetivo

Hasta ahora aprendimos a **construir** tres algoritmos aislados: Naive Bayes, k-NN y CART. Pero en producción surge la pregunta decisiva:

> **"Tengo un problema de diagnóstico de fallas. ¿Qué algoritmo debo usar?"**

Esta lección te enseña a **comparar algoritmos en igualdad de condiciones** y elegir el mejor para tu contexto específico.

---

## 1. Matriz Comparativa: Bayes vs. k-NN vs. CART

```text
┌──────────────────┬──────────────┬──────────────┬──────────────┐
│ Característica   │ Naive Bayes  │ k-NN         │ CART         │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ Complejidad      │ Lineal (O(n))│ Cúbica (O(n·d))│ Cuadrática  │
│ Interpretación   │ Probabilista │ Geométrica   │ Visual/Lógica│
│ Datos Pequeños   │ ✅ Excelente │ ⚠️ Riesgo    │ ⚠️ Sobreajusta│
│                  │              │  overfitting │              │
│ Datos Grandes    │ ✅ Escalable │ ❌ Lento     │ ✅ Rápido     │
│ Variables Mixed  │ ⚠️ No recome│ ✅ Sí        │ ✅ Sí         │
│ (núm + categ.)   │               │              │              │
│ Ruido / Outliers │ ✅ Robusto   │ ❌ Sensible  │ ⚠️ Moderado  │
│ Features Correl. │ ❌ Asume     │ ✅ Maneja    │ ✅ Maneja    │
│                  │  independ.   │              │              │
│ Ajuste de Paráms │ Mínimo       │ Solo `k`     │ Múltiples    │
│ (Hiperparáms)    │              │              │              │
├──────────────────┼──────────────┼──────────────┼──────────────┤
│ **Caso Óptimo**  │ Datos       │ Firmas       │ Reglas       │
│ en energy-ml     │ históricos   │ geométricas  │ lógicas      │
│                  │ con prior    │ en espacio   │ (si/no)      │
│                  │ de falla     │ de features  │              │
└──────────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 2. Caso Práctico: Clasificación de Cargas en energy-ml

Supongamos que tenemos 4 tipos de cargas en la planta:
- **Motor Inducción** (3200 W, FP=0.72)
- **Horno Eléctrico** (4500 W, FP=0.98)
- **Iluminación LED** (250 W, FP=0.92)
- **Sistema Ventilación** (2200 W, FP=0.85)

Y queremos clasificar una nueva observación: (2800 W, FP=0.75)

### 2.1 Enfoque con Naive Bayes

```python
from sklearn.naive_bayes import GaussianNB
import numpy as np

# Datos históricos etiquetados
X_train = np.array([
    [3200, 0.72], [3100, 0.70],  # Motor
    [4500, 0.98], [4600, 0.99],  # Horno
    [250,  0.92], [280,  0.90],  # LED
    [2200, 0.85], [2300, 0.86]   # Ventilador
])

y_train = ["motor", "motor", "horno", "horno", "led", "led", "ventilador", "ventilador"]

modelo_bayes = GaussianNB()
modelo_bayes.fit(X_train, y_train)

muestra = [[2800, 0.75]]
prediccion = modelo_bayes.predict(muestra)[0]
confianza = modelo_bayes.predict_proba(muestra)[0]

print(f"Predicción: {prediccion}")
print(f"Confianzas: {dict(zip(modelo_bayes.classes_, confianza))}")
```

**Salida esperada:**
```
Predicción: motor
Confianzas: {'motor': 0.78, 'horno': 0.02, 'led': 0.01, 'ventilador': 0.19}
```

**Análisis:**
- ✅ Proporción clara (78% vs 19% vs 2% vs 1%)
- ✅ Interpretable: "Es un motor con 78% de certeza"
- ⚠️ Supone independencia entre potencia y FP (falso en realidad)

---

### 2.2 Enfoque con k-NN (k=3)

```python
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

# Pipeline seguro: escala + k-NN
modelo_knn = Pipeline([
    ("scaler", StandardScaler()),
    ("knn", KNeighborsClassifier(n_neighbors=3))
])

modelo_knn.fit(X_train, y_train)
prediccion = modelo_knn.predict(muestra)[0]

print(f"Predicción: {prediccion}")

# Encontrar los 3 vecinos más cercanos
vecinos_indices = modelo_knn.named_steps["knn"].kneighbors(modelo_knn.named_steps["scaler"].transform(muestra))[1][0]
vecinos_etiquetas = [y_train[i] for i in vecinos_indices]
print(f"3 Vecinos más cercanos: {vecinos_etiquetas}")
```

**Salida esperada:**
```
Predicción: motor
3 Vecinos más cercanos: ['motor', 'motor', 'ventilador']
```

**Análisis:**
- ✅ Resultado comprensible: "Es similar a dos motores y un ventilador"
- ⚠️ Sin probabilidad (o con heurística de votación: 2/3 = 66.7%)
- ❌ Compleja de escalar con 10.000+ registros históricos (lento en inferencia)

---

### 2.3 Enfoque con CART (Árbol de Decisión)

```python
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt

modelo_cart = DecisionTreeClassifier(max_depth=3, random_state=42)
modelo_cart.fit(X_train, y_train)

prediccion = modelo_cart.predict(muestra)[0]
confianza = modelo_cart.predict_proba(muestra)[0]

print(f"Predicción: {prediccion}")
print(f"Confianzas: {dict(zip(modelo_cart.classes_, confianza))}")

# Visualizar reglas de decisión
plot_tree(modelo_cart, feature_names=["Potencia (W)", "Factor Potencia"],
          class_names=modelo_cart.classes_, filled=True)
plt.show()
```

**Salida esperada:**
```
Predicción: motor
Confianzas: {'motor': 1.0, 'horno': 0.0, 'led': 0.0, 'ventilador': 0.0}
```

**Reglas descubiertas (ejemplo):**
```
Si Potencia <= 1000:
  └─ Clasificar como "led"
Si Potencia > 1000 y Potencia <= 3500:
  └─ Clasificar como "motor"
Si Potencia > 3500 y FP >= 0.95:
  └─ Clasificar como "horno"
```

**Análisis:**
- ✅ Reglas interpretables (ejecutivos entienden "si/entonces")
- ✅ Rápido en inferencia (solo comparaciones)
- ⚠️ Confianza binaria (1.0 o 0.0, no probabilidad suave)
- ⚠️ Propenso a sobreajuste con pocos datos

---

## 3. Matriz de Decisión: ¿Cuál Elegir?

### 3.1 Si el Cliente Pregunta: "¿Qué Probabilidad de Falla Hay?"

| Algoritmo | Respuesta | Confianza |
|---|---|---|
| **Bayes** | "97.2% de falla" | Probabilística calibrada |
| **k-NN** | "3 de 5 vecinos fallaron" | Heurística de votación |
| **CART** | "Falla (100% o 0%)" | Binaria, no suave |

→ **Recomendación: Naive Bayes** (probabilidades explícitas)

---

### 3.2 Si el Dataset Histórico es Muy Pequeño (< 100 muestras)

| Algoritmo | Comportamiento | Riesgo |
|---|---|---|
| **Bayes** | Aprende bien con pocas muestras | Bajo; robusto |
| **k-NN** | Busca los vecinos más cercanos | Medio; riesgo de overfitting |
| **CART** | Crece sin control | **Alto; sobreajusta seguro** |

→ **Recomendación: Naive Bayes** (mín. hiperparámetros, máx. generalización)

---

### 3.3 Si Necesitas Máxima Velocidad en Inferencia (Tiempo Real)

| Algoritmo | Latencia | Escalabilidad |
|---|---|---|
| **Bayes** | O(d) — Microsegundos | ✅ Excelente |
| **k-NN** | O(N·d) — Milisegundos | ⚠️ Limita a N < 100k |
| **CART** | O(log N) — Microsegundos | ✅ Excelente |

→ **Recomendación: Bayes o CART** (según contexto de interpretabilidad)

---

### 3.4 Si Necesitas Reglas Explicables a No-Técnicos

| Algoritmo | Explicabilidad | Aceptación Stakeholder |
|---|---|---|
| **Bayes** | "P(A\|B) = ..." | ⚠️ Requiere enseñanza |
| **k-NN** | "Es similar a estos casos..." | ✅ Intuitivo |
| **CART** | "Si X > 5000 entonces..." | ✅ **Mejor aceptación** |

→ **Recomendación: CART** (o comité de decisión híbrido)

---

## 4. Estrategia Híbrida: Ensemble de Modelos

En producción de energy-ml, **no es "elige uno"**, sino **"usa varios en conjunto"**:

```python
from sklearn.ensemble import VotingClassifier

# Combinamos los 3 modelos
modelo_hibrido = VotingClassifier(
    estimators=[
        ("bayes", GaussianNB()),
        ("knn", Pipeline([("scaler", StandardScaler()), 
                          ("knn", KNeighborsClassifier(n_neighbors=5))])),
        ("cart", DecisionTreeClassifier(max_depth=5))
    ],
    voting="soft"  # Promedia probabilidades
)

modelo_hibrido.fit(X_train, y_train)
prob_prediccion = modelo_hibrido.predict_proba(muestra)[0]

print(f"Predicción Ensemble: {modelo_hibrido.predict(muestra)[0]}")
print(f"Confianzas promediadas: {dict(zip(modelo_hibrido.classes_, prob_prediccion))}")
```

**Ventajas del Ensemble:**
- ✅ Suaviza errores de un modelo individual
- ✅ Mayor robustez ante datos anómalos
- ✅ Proporciona intervalo de confianza (si 2/3 acuerdan, confianza 66%+)

---

## 5. Autoevaluación Formativa: Selección en Contextos Reales

### Pregunta 1: Escenario "Mantenimiento Preventivo"

Un operador de planta monitorea 50 transformadores. Tiene 2 años de datos históricos (etiquetados: "Falla Próxima" o "Normal"). Quiere predecir si hay falla en **tiempo real (< 10 ms latencia)**.

¿Qué algoritmo recomiendas?
- A) Naive Bayes (O(d) latencia, interpretable, probabilístico)
- B) k-NN (busca los 5 más cercanos, latencia O(50*4) = O(200) ms, **demasiado lento**)
- C) CART (O(log 50) = 6 comparaciones, latencia microsegundos, interpretable)
- D) Ensemble (máxima robustez, pero latencia 3x Bayes)

**Respuesta correcta:** **A o C**
- Si necesitas probabilidades explícitas → **A (Bayes)**
- Si necesitas reglas = "Si Temp > X entonces Falla" → **C (CART)**

---

### Pregunta 2: Escenario "Dataset Pequeño"

Tienes solo 30 registros históricos de una nueva subestación y necesitas predecir fallas. ¿Cuál es el mayor riesgo?

- A) Naive Bayes generaliza bien incluso con 30 muestras (asunción de independencia actúa como regularizador)
- B) k-NN encontrará "vecinos muy cercanos" pero podrían ser ruido
- C) CART seguro va a sobreajustar, memorizando los 30 casos sin aprender patrones

**Respuesta correcta:** **C**  
**Justificación:** Con 30 muestras, CART crece sin control. Bayes es la opción más segura. Si usas CART, **limita profundidad (`max_depth=2`)**

---

### Pregunta 3: Integración en Endpoint FastAPI

Tu endpoint `POST /api/v1/classify` recibe telemetría cada segundo de 100 clientes concurrentes. ¿Qué combinación es más viable?

- A) Un Bayes por cliente (100 modelos ligeros) — **100 × O(d) = Viable**
- B) Un k-NN centralizado con 50k registros — **O(50k × d) = ~50 ms, marginal**
- C) Un CART por segmento industrial — **O(log N) × clientes = Viable**
- D) Ensemble pesado (Bayes + k-NN + CART) × 100 clientes — **Lento y caro**

**Respuesta correcta:** **A o C**  
**Recomendación:** Bayes por cliente (100 × microsegundos) es la opción más escalable.

---

## 6. Conclusión: No Hay Un "Ganador"

| Contexto | Algoritmo | Razón |
|---|---|---|
| Probabilidades calibradas | **Bayes** | P(Falla\|Datos) es lo que quiero |
| Dataset pequeño | **Bayes** | Regularización implícita |
| Máxima velocidad | **CART** | O(log N) inferencia |
| Máxima inteligibilidad | **CART** | Si/entonces humano |
| Máxima robustez | **Ensemble** | Vota los 3 juntos |
| Firmas geométricas | **k-NN** | Similitud espacial |

**La sabiduría del Científico de Datos: Experimenta, compara en tu dataset específico y elige el que generalice mejor en validación cruzada.**

---

## 7. Laboratorio Integrador: Comparación Empírica en energy-ml

```python
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

# Cargar datos reales de energy-ml
X, y = load_energy_ml_dataset()

modelos = {
    "Naive Bayes": GaussianNB(),
    "k-NN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "CART (depth=3)": DecisionTreeClassifier(max_depth=3)
}

for nombre, modelo in modelos.items():
    # Validación cruzada: 5-fold
    scores = cross_val_score(modelo, X, y, cv=5, scoring="f1_weighted")
    print(f"{nombre}: F1 promedio = {scores.mean():.3f} (+/- {scores.std():.3f})")
```

**Ejecuta este laboratorio en tu `energy-ml` local y veras cuál es el mejor para TUS datos.**

---

## Siguiente Lección

En **Cap 5.6 (TDD y Prod)**, operacionalizaremos el modelo ganador dentro de un endpoint FastAPI con métricas, tests y monitoreo en producción.
