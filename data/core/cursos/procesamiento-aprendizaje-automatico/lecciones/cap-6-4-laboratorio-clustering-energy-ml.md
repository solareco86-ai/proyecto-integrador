# Lección 6.4: Laboratorio Práctico: Agrupamiento de Firmas de Consumo Eléctrico en energy-ml

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo 6:** Bloque Aprendizaje No Supervisado y Agrupamiento (Clustering)  
**Carga horaria estimada:** 35 min  
**Prerrequisitos:** Haber completado las Lecciones 6.1 a 6.3.  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10.d: *«Prácticas profesionalizantes en entornos formativos: sistemas y aplicaciones informáticas que utilizan técnicas de aprendizaje supervisado y no supervisado»*).  
**Repositorio del caso:** [`https://github.com/datamaq-automation/energy-ml`](https://github.com/datamaq-automation/energy-ml)

---

## 1. El Problema Técnico: Desagregación No Supervisada de Cargas (NILM)

En sistemas de monitoreo energético como **`energy-ml`**, un medidor inteligente instalado en la acometida eléctrica principal registra la potencia activa total `P (W)` y reactiva `Q (VAR)`. 

A menudo, la planta industrial o el edificio **no posee etiquetas históricas** de qué maquinaria se encendió en cada instante. El objetivo de este laboratorio es implementar una secuencia de análisis no supervisada que permita:
1. Detectar transitorios y saltos de potencia `(Delta P, Delta Q)`.
2. Estandarizar las características con `StandardScaler`.
3. Determinar el número óptimo de cargas mediante el **Método del Codo** y el **Coeficiente de Silueta**.
4. Agrupar las firmas de consumo mediante **k-medias** y **Estrategia Aglomerativa**.
5. Comparar la calidad geométrica de ambos agrupamientos.

---

## 2. Preparación del Laboratorio en Python

```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score

# 1. Simulación de firmas eléctricas delta P (Watts) y delta Q (VAR)
# Representa 4 tipos de aparatos:
# - Carga 1: Iluminación LED y electrónica (P ~ 80W, Q ~ 10 VAR)
# - Carga 2: Resistivo puro / Calefactor (P ~ 2000W, Q ~ 5 VAR)
# - Carga 3: Motor pequeño / Ventilador (P ~ 350W, Q ~ 200 VAR)
# - Carga 4: Compresor industrial con bajo factor de potencia (P ~ 1800W, Q ~ 1100 VAR)

np.random.seed(199)
c1 = np.random.normal(loc=[80, 10], scale=[10, 3], size=(35, 2))
c2 = np.random.normal(loc=[2000, 5], scale=[60, 5], size=(30, 2))
c3 = np.random.normal(loc=[350, 200], scale=[25, 20], size=(40, 2))
c4 = np.random.normal(loc=[1800, 1100], scale=[70, 50], size=(35, 2))

X_raw = np.vstack([c1, c2, c3, c4])

# 2. Estandarización obligatoria de características
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_raw)
```

---

## 3. Determinación de `k` con Codo y Silueta

```python
# Evaluación de k entre 2 y 7
inercias = []
siluetas = {}

print("=== BÚSQUEDA DE HIPERPARÁMETRO K ===")
for k in range(2, 8):
    km = KMeans(n_clusters=k, init="k-means++", n_init=10, random_state=42)
    labels = km.fit_predict(X_scaled)
    inercias.append(km.inertia_)
    score = silhouette_score(X_scaled, labels)
    siluetas[k] = score
    print(f"k = {k} | Inercia = {km.inertia_:.2f} | Silueta = {score:.4f}")

k_optimo = max(siluetas, key=siluetas.get)
print(f"\n=> k seleccionado por máxima silueta: {k_optimo}")
```

---

## 4. Agrupamiento y Comparación de Modelos

Aplicamos simultáneamente el algoritmo **k-medias** y la **Estrategia Aglomerativa (Ward)** con el `k` óptimo determinado:

```python
# A. Modelo Particional: k-medias
km_modelo = KMeans(n_clusters=k_optimo, init="k-means++", n_init=10, random_state=42)
labels_km = km_modelo.fit_predict(X_scaled)
score_km = silhouette_score(X_scaled, labels_km)

# B. Modelo Jerárquico: Estrategia Aglomerativa (Ward)
agg_modelo = AgglomerativeClustering(n_clusters=k_optimo, linkage="ward")
labels_agg = agg_modelo.fit_predict(X_scaled)
score_agg = silhouette_score(X_scaled, labels_agg)

print("\n=== COMPARACIÓN DE ESTRATEGIAS DE CLUSTERING ===")
print(f"k-medias (k-means++)       - Silueta: {score_km:.4f}")
print(f"Estrategia Aglomerativa    - Silueta: {score_agg:.4f}")

# C. Recuperación de los centroides en escala física original (Watts y VAR)
centroides_fisicos = scaler.inverse_transform(km_modelo.cluster_centers_)
print("\n=== CENTROIDES ESTIMADOS POR K-MEDIAS (ESCALA REAL) ===")
for idx, cent in enumerate(centroides_fisicos):
    print(f"Cluster {idx}: Potencia Activa = {cent[0]:.1f} W | Potencia Reactiva = {cent[1]:.1f} VAR")
```

---

## 5. Conclusiones y Práctica Profesionalizante

1. **Sin supervisión ni etiquetas previas**, el sistema segmentó con éxito los 4 patrones de carga eléctrica a partir de sus propiedades electromagnéticas.
2. La combinación de **k-medias** y **Estrategia Aglomerativa** proporciona una doble verificación: si ambos algoritmos convergen a particiones altamente congruentes con coeficientes de silueta elevados (`> 0.70`), existe alta certeza técnica de que los clusters representan maquinaria física real y no agrupamientos espurios.
3. Este módulo forma parte del pipeline de pre-procesamiento e identificación automática de activos industriales en la arquitectura de `energy-ml`.
