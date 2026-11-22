# Lección 6.3: Algoritmo k-medias: Centroides, Convergencia y Selección de k (Método del Codo y Silueta)

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo 6:** Bloque Aprendizaje No Supervisado y Agrupamiento (Clustering)  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado la Lección 6.1 (Conceptos de clustering) y Lección 6.2 (Estrategia aglomerativa).  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10, Espacio 12: Bloque Aprendizaje No Supervisado: *«Algoritmo k-medias»*).

---

## 1. Fundamentos del Algoritmo k-medias (*k-means*)

El algoritmo **k-medias (*k-means*)** es el método particional por excelencia en aprendizaje automático. Su propósito es particionar `N` observaciones en `K` clusters mutuamente excluyentes, donde cada observación pertenece al cluster cuyo **centroide** (media matemática de los puntos del grupo) se encuentra más cercano.

### Función Objetivo: Suma de Cuadrados Intra-Cluster (WCSS / Inercia)
k-medias busca minimizar la inercia o suma de distancias euclidianas cuadradas de cada punto `x_i` a su centroide asignado `mu_k`:

```text
Inercia (WCSS) = sum_{k=1}^K sum_{x_i in C_k} || x_i - mu_k ||^2
```

---

## 2. El Algoritmo Estándar de Lloyd: Pasos de Optimización

El algoritmo k-medias opera de manera iterativa alternando dos fases fundamentales hasta alcanzar convergencia:

```text
PASOS DEL ALGORITMO K-MEDIAS:
┌────────────────────────────────────────────────────────────────────────┐
│ Paso 1: Inicialización                                                 │
│ Se eligen K centroides iniciales (mu_1, ..., mu_K).                    │
│ Recomendado: k-means++ (distribuye los centroides iniciales alejados). │
├────────────────────────────────────────────────────────────────────────┤
│ Paso 2: Asignación (Expectation)                                       │
│ Cada muestra x_i se asigna al cluster del centroide más cercano:      │
│ c_i = argmin_k || x_i - mu_k ||^2                                      │
├────────────────────────────────────────────────────────────────────────┤
│ Paso 3: Actualización (Maximization)                                   │
│ Se recalculan las posiciones de los centroides como el promedio        │
│ de todos los puntos asignados a cada grupo:                            │
│ mu_k = (1 / |C_k|) * sum_{x_i in C_k} x_i                              │
├────────────────────────────────────────────────────────────────────────┤
│ Paso 4: Criterio de Parada                                             │
│ Se repiten los pasos 2 y 3 hasta que la asignación no varíe o el cambio│
│ en los centroides sea inferior a un umbral de tolerancia (tol).        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 3. El Desafío Central: Selección del Número Óptimo de Clusters (`k`)

Dado que k-medias es no supervisado y no disponemos de etiquetas reales para calcular accuracy o matrices de confusión, la elección de `k` requiere **métricas de validación interna**:

### A. Método del Codo (*Elbow Method*)
* Se entrena el algoritmo para una secuencia de valores de `k` (por ejemplo, `k in [1, 2, ..., 10]`).
* Se grafica la **inercia (WCSS)** en función de `k`.
* La inercia siempre disminuye a medida que `k` aumenta (para `k = N`, la inercia es 0). Sin embargo, el punto de inflexión donde la reducción marginal de la inercia se desacelera abruptamente (la "curvatura del codo") indica el compromiso óptimo entre compacidad y parsimonia del modelo.

### B. Coeficiente de Silueta (*Silhouette Score*)
El coeficiente de silueta mide cuán similar es un punto a su propio cluster en comparación con los otros clusters. Para cada muestra `i`:
- `a(i)`: distancia media de `i` a todos los demás puntos de su mismo cluster (cohesión).
- `b(i)`: distancia media de `i` a todos los puntos del cluster más cercano distinto al suyo (separación).

```text
s(i) = (b(i) - a(i)) / max(a(i), b(i))
```

* **Interpretación:**
  - `s(i) ≈ +1`: Muestra excelentemente agrupada y lejos de clusters vecinos.
  - `s(i) ≈ 0`: Muestra ubicada en el límite o frontera entre dos clusters.
  - `s(i) < 0`: Muestra probablemente asignada al cluster incorrecto.
* El valor promedio global de silueta en todo el dataset permite comparar cuantitativamente distintas configuraciones de `k`.

---

## 4. Implementación en Python con Scikit-Learn

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

# Dataset sintético de lecturas de potencia (kW) y corriente (A)
np.random.seed(42)
cluster_1 = np.random.normal(loc=[1.2, 5.5], scale=0.15, size=(40, 2))
cluster_2 = np.random.normal(loc=[4.8, 22.0], scale=0.35, size=(40, 2))
cluster_3 = np.random.normal(loc=[9.5, 43.0], scale=0.60, size=(40, 2))
X = np.vstack([cluster_1, cluster_2, cluster_3])

# Búsqueda del k óptimo evaluando inercia y silueta
inercias = []
siluetas = {}

for k in range(2, 6):
    kmeans = KMeans(n_clusters=k, init="k-means++", random_state=42, n_init=10)
    etiquetas = kmeans.fit_predict(X)
    inercias.append(kmeans.inertia_)
    score_sil = silhouette_score(X, etiquetas)
    siluetas[k] = score_sil
    print(f"k={k} | Inercia={kmeans.inertia_:.1f} | Silueta={score_sil:.3f}")

mejor_k = max(siluetas, key=siluetas.get)
print(f"\n=> El k óptimo según el coeficiente de silueta es k = {mejor_k}")
```

---

## 5. Cuadro Comparativo: k-medias vs Estrategia Aglomerativa

```text
┌───────────────────────────┬───────────────────────────┬──────────────────────────┐
│ Característica            │ Algoritmo k-medias        │ Estrategia Aglomerativa  │
├───────────────────────────┼───────────────────────────┼──────────────────────────┤
│ Tipo de algoritmo         │ Particional (iterativo)   │ Jerárquico (ascendente)  │
│ Complejidad temporal      │ O(N * K * iteraciones)    │ O(N^2 log N) o O(N^3)    │
│ Escalabilidad             │ Alta (apta grandes datos) │ Baja / Moderada          │
│ Forma de los clusters     │ Esférica / isotrópica     │ Arbitraria (según enlace)│
│ Sensibilidad a outliers   │ Alta (desplaza centroides)│ Media (con enlace simple)│
└───────────────────────────┴───────────────────────────┴──────────────────────────┘
```
