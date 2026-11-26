# Lección 6.7: Comparación Crítica y Selección de Modelos: Supervisados (Bayes, k-NN, CART) y No Supervisados (k-medias, Aglomerativo)

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo 6:** Bloque Aprendizaje No Supervisado y Agrupamiento (Clustering)  
**Carga horaria estimada:** 40 min  
**Prerrequisitos:** Haber completado los Capítulos 3 a 6 de la Unidad 2 (Modelos supervisados: Bayes, k-NN, CART; y modelos no supervisados: k-medias y clustering aglomerativo).  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10, Espacio 12: Bloque Aprendizaje No Supervisado: *«Comparación y selección de modelos»*).

---

## 1. El Dilema de la Selección de Modelos en Producción

A lo largo del trayecto formativo hemos estudiado algoritmos pertenecientes a diferentes familias y paradigmas de aprendizaje:
* **Supervisados probabilísticos:** Naive Bayes.
* **Supervisados basados en instancias (*Lazy*):** k-Nearest Neighbors (k-NN).
* **Supervisados basados en partición recursiva y reglas:** Árboles CART.
* **No supervisados particionales:** Algoritmo k-medias.
* **No supervisados jerárquicos (*Bottom-Up*):** Estrategia Aglomerativa.

En un entorno productivo real como **`energy-ml`**, la pregunta determinante del ingeniero de datos es:
> **"Frente a este problema de telemetría y diagnóstico, ¿cuál es el modelo óptimo y bajo qué criterios objetivos debo seleccionarlo?"**

---

## 2. Árbol de Decisión: ¿Supervisado o No Supervisado?

El primer paso metodológico consiste en determinar la naturaleza de los datos y el objetivo de la tarea:

```text
┌────────────────────────────────────────────────────────────────────────┐
│             ÁRBOL DE DECISIÓN METODOLÓGICO: PARADIGMAS                 │
├────────────────────────────────────────────────────────────────────────┤
│ ¿Se dispone de etiquetas históricas confiables (ground truth)?         │
│  ├── SÍ -> APRENDIZAJE SUPERVISADO                                     │
│  │    ├── ¿Se necesitan probabilidades calibradas de certeza?          │
│  │    │     └──> NAIVE BAYES (Inferencia lineal ultrarrápida)          │
│  │    ├── ¿Las clases forman firmas geométricas complejas en espacio?  │
│  │    │     └──> k-NN (Aprendizaje por instancias con StandardScaler)  │
│  │    └── ¿Se requiere interpretabilidad en reglas if/else y auditoría?│
│  │          └──> ÁRBOLES CART (Decisión estructurada y explicabilidad) │
│  │                                                                     │
│  └── NO -> APRENDIZAJE NO SUPERVISADO                                  │
│       ├── ¿Dataset masivo en streaming con necesidad de baja latencia? │
│       │     └──> k-MEDIAS (Partición iterativa, O(N*K*iter))           │
│       └── ¿Se busca taxonomía jerárquica o clusters de forma no esférica?│
│             └──> ESTRATEGIA AGLOMERATIVA (Dendrogramas, Ward/Complete) │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Matriz Comparativa Integral de Algoritmos

```text
┌─────────────────┬──────────────┬──────────────┬──────────────┬──────────────┬──────────────┐
│ Característica  │ Naive Bayes  │ k-NN         │ CART         │ k-medias     │ Aglomerativo │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ Paradigma       │ Supervisado  │ Supervisado  │ Supervisado  │ No supervis. │ No supervis. │
│ Tipo de salida  │ Probabilidad │ Clase/Regres.│ Reglas/Valor │ Cluster ID   │ Dendrograma  │
│ Complejidad Tr. │ O(N * D)     │ O(1)         │ O(N * D logN)│ O(N*K*D*iter)│ O(N^2 log N) │
│ Complejidad Inf.│ O(D)         │ O(N * D)     │ O(profund.)  │ O(K * D)     │ N/A (estático)│
│ Escalabilidad   │ Excelente    │ Mala (>50k)  │ Muy buena    │ Muy buena    │ Limitada     │
│ Datos mixtos    │ Moderado     │ Requiere enc.│ Excelente    │ Requiere enc.│ Soporta Gower│
│ Ruido/Outliers  │ Robusto      │ Muy sensible │ Moderado     │ Sensible     │ Robusto (Avg)│
│ Métrica de      │ Log-Loss, F1,│ Accuracy, F1,│ Gini, MAE,   │ Inercia      │ Cofenético,  │
│ Evaluación      │ ROC-AUC      │ Matriz conf. │ R2, F1-Score │ (WCSS), Codo │ Silueta      │
├─────────────────┼──────────────┼──────────────┼──────────────┼──────────────┼──────────────┤
│ Caso Óptimo en  │ Detección de │ Matching de  │ Reglas de    │ Descubrimiento│ Taxonomía de│
│ energy-ml       │ fallas con   │ firmas trans-│ disparo de   │ de máquinas  │ régimen de   │
│                 │ probabilidades│itorias raras│ alarmas      │ sin etiquetas│ operación    │
└─────────────────┴──────────────┴──────────────┴──────────────┴──────────────┴──────────────┘
```

---

## 4. Comparación Específica en No Supervisado: k-medias vs Aglomerativo

Dentro del Bloque No Supervisado, la elección entre k-medias y Estrategia Aglomerativa se guía por tres factores técnicos:

1. **Volumen de Muestras ($N$):**
   - Si $N > 10.000$, la matriz de distancias de la estrategia aglomerativa ($O(N^2)$ en memoria) desborda la RAM del servidor. **k-medias** es la opción mandatoria.
   - Para estudios de auditoría energética con muestras representativas de transitorios ($N < 2.000$), la **estrategia aglomerativa** provee dendrogramas determinísticos sin riesgo de caer en óptimos locales.
2. **Forma de las Agrupaciones:**
   - k-medias asume clusters esféricos e isotrópicos con varianza similar.
   - La estrategia aglomerativa (con enlace promedio o simple) puede identificar agrupamientos con geometrías irregulares o alargadas.
3. **Criterio de Validación:**
   - En k-medias se evalúa la inercia (método del codo) para descartar sobre-segmentación.
   - En ambos algoritmos, el **coeficiente de silueta** permite comparar directamente cuál estrategia genera clusters mejor delimitados.

---

## 5. Laboratorio Práctico: Comparación Empírica en energy-ml

El siguiente script evalúa y compara tanto modelos supervisados (cuando se cuenta con etiquetas) como modelos no supervisados (cuando se analizan perfiles en crudo):

```python
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score

# Generación de telemetría de prueba (Potencia, Factor de Potencia, THD)
np.random.seed(42)
X_raw, y_real = make_blobs(n_samples=300, n_features=3, centers=3, cluster_std=0.8, random_state=42)
scaler = StandardScaler()
X = scaler.fit_transform(X_raw)

print("=== 1. EVALUACIÓN DE MODELOS SUPERVISADOS (5-Fold CV) ===")
modelos_sup = {
    "Naive Bayes": GaussianNB(),
    "k-NN (k=5)": KNeighborsClassifier(n_neighbors=5),
    "CART (depth=3)": DecisionTreeClassifier(max_depth=3, random_state=42)
}

for nombre, mod in modelos_sup.items():
    scores = cross_val_score(mod, X, y_real, cv=5, scoring="f1_weighted")
    print(f" - {nombre:15s} | F1-Score: {scores.mean():.4f} (+/- {scores.std():.4f})")

print("\n=== 2. EVALUACIÓN DE MODELOS NO SUPERVISADOS (Silueta) ===")
# k-medias
km = KMeans(n_clusters=3, init="k-means++", n_init=10, random_state=42)
labels_km = km.fit_predict(X)
sil_km = silhouette_score(X, labels_km)

# Estrategia Aglomerativa (Ward)
agg = AgglomerativeClustering(n_clusters=3, linkage="ward")
labels_agg = agg.fit_predict(X)
sil_agg = silhouette_score(X, labels_agg)

print(f" - k-medias (k=3)       | Coeficiente de Silueta: {sil_km:.4f} (Inercia: {km.inertia_:.1f})")
print(f" - Aglomerativo (Ward)  | Coeficiente de Silueta: {sil_agg:.4f}")

# Criterio de selección
ganador_nosup = "k-medias" if sil_km >= sil_agg else "Estrategia Aglomerativa"
print(f"\n=> Selección no supervisada recomendada: {ganador_nosup}")
```

---

## 6. Autoevaluación Formativa

1. Si un sensor de planta industrial debe diagnosticar fallas en un microcontrolador embebido con 64 KB de memoria y latencia inferior a 1 ms, ¿qué algoritmo supervisado seleccionarías y por qué?
2. Si un auditor energético recibe un volcado de un mes de telemetría eléctrica sin ninguna etiqueta y necesita descubrir cuántos patrones de consumo existen, ¿cuál es el procedimiento riguroso de selección de modelo y número de clusters?
