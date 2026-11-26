# Lección 6.2: Estrategia Aglomerativa: Clustering Jerárquico y Dendrogramas

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo 6:** Bloque Aprendizaje No Supervisado y Agrupamiento (Clustering)  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 6.1 (Conceptos de agrupamiento y matrices de distancia).  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10, Espacio 12: Bloque Aprendizaje No Supervisado: *«Estrategia Aglomerativa»*).

---

## 1. El Enfoque Jerárquico Aglomerativo (*Bottom-Up*)

A diferencia de los métodos particionales (como k-medias) que requieren especificar de antemano el número exacto `k` de grupos, el **agrupamiento jerárquico (*Hierarchical Clustering*)** construye una jerarquía anidada de particiones en forma de árbol.

La **Estrategia Aglomerativa** opera con un enfoque ascendente (*bottom-up*):
1. **Paso Inicial:** Cada una de las `N` observaciones comienza constituyendo su propio cluster individual de tamaño 1 (existen `N` clusters aislados).
2. **Iteración:** En cada paso sucesivo, se calcula la distancia entre todos los pares de clusters existentes y se fusionan (*merge*) los dos clusters más cercanos o similares.
3. **Paso Final:** El proceso se repite `N - 1` veces hasta que todos los puntos quedan reunidos en un único cluster global que abarca la totalidad del dataset.

```text
ESTRATEGIA AGLOMERATIVA (BOTTOM-UP):
Iteración 3:       [ (A, B), (C, (D, E)) ]      <- 2 clusters restantes
Iteración 2:       [ (A, B), C, (D, E) ]        <- Se fusionan D y E
Iteración 1:       [ (A, B), C, D, E ]          <- Se fusionan A y B
Estado Inicial:    [ A ], [ B ], [ C ], [ D ], [ E ]  <- N clusters aislados
```

---

## 2. Criterios de Enlace (*Linkage Criteria*)

Para fusionar dos clusters `A` y `B`, no basta con medir la distancia entre puntos individuales; es necesario definir la **distancia entre conjuntos de puntos `D(A, B)`**. El Anexo I fundamenta el estudio de los criterios de enlace clásicos:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   CRITERIOS DE ENLACE EN CLUSTERING AGLOMERATIVO       │
├───────────────────────────────┬────────────────────────────────────────┤
│ 1. Enlace Simple              │ Distancia mínima entre cualquier punto │
│    (Single Linkage)           │ de A y cualquier punto de B:           │
│                               │ D(A, B) = min { d(x, y) : x in A, y in B }│
│                               │ Tiende al "efecto cadena" alargado.    │
├───────────────────────────────┼────────────────────────────────────────┤
│ 2. Enlace Completo            │ Distancia máxima entre puntos:         │
│    (Complete Linkage)         │ D(A, B) = max { d(x, y) : x in A, y in B }│
│                               │ Genera clusters compactos y esféricos. │
├───────────────────────────────┼────────────────────────────────────────┤
│ 3. Enlace Promedio            │ Promedio de distancias entre todos     │
│    (Average Linkage)          │ los pares de elementos de A y B.       │
├───────────────────────────────┼────────────────────────────────────────┤
│ 4. Método de Ward             │ Minimiza el incremento de la varianza  │
│    (Ward's Linkage)           │ intra-cluster total al fusionar A y B. │
│                               │ Es el método más utilizado en telemetría│
└───────────────────────────────┴────────────────────────────────────────┘
```

---

## 3. Representación Gráfica: El Dendrograma

La secuencia completa de fusiones se visualiza a través de un **dendrograma**: un diagrama de árbol donde:
- El **eje horizontal** representa las muestras u observaciones individuales.
- El **eje vertical** indica la distancia o disimilitud a la cual se produjo cada fusión.

### Cómo elegir el número de clusters cortando el dendrograma:
Para obtener una partición con `K` grupos, se traza una línea de corte horizontal transversal a cierta altura `h`. La cantidad de líneas verticales cortadas por ese umbral define exactamente el número de clusters resultantes.

---

## 4. Implementación en Python con SciPy y Scikit-Learn

```python
import numpy as np
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
from sklearn.cluster import AgglomerativeClustering

# Muestra sintética de telemetría de potencia activa (W) y reactiva (VAR)
X = np.array([
    [120.0, 15.0],   # Iluminación LED
    [130.0, 18.0],   # Iluminación LED
    [1500.0, 400.0], # Compresor de refrigeración
    [1550.0, 420.0], # Compresor de refrigeración
    [2200.0, 950.0], # Motor de inducción / Bomba
    [2180.0, 930.0], # Motor de inducción / Bomba
])

# 1. Estrategia Aglomerativa con método de Ward
Z = linkage(X, method="ward")

# 2. Extracción de clusters cortando en K = 3
etiquetas = fcluster(Z, t=3, criterion="maxclust")
print("Asignación de clusters:", etiquetas)

# 3. Implementación directa con scikit-learn
modelo = AgglomerativeClustering(n_clusters=3, metric="euclidean", linkage="ward")
predicciones = modelo.fit_predict(X)
print("Clusters scikit-learn:", predicciones)
```

---

## 5. Ventajas y Limitaciones de la Estrategia Aglomerativa

* **Ventajas:**
  - No asume formas esféricas a priori (especialmente con enlace simple o promedio).
  - El dendrograma provee una rica interpretación jerárquica de relaciones taxonómicas.
  - Resultados 100% determinísticos (sin dependencia de inicializaciones aleatorias).
* **Limitaciones:**
  - Complejidad computacional temporal de orden `O(N^3)` o `O(N^2 log N)` y espacial `O(N^2)` para almacenar la matriz de distancias, lo que limita su aplicación directa en streaming masivo de telemetría sin muestreo previo.
