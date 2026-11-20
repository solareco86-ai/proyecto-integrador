# Lección 6.1: Aprendizaje No Supervisado: Elaboración del Modelo, Características, Ejemplos y Aplicaciones

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo 6:** Bloque Aprendizaje No Supervisado y Agrupamiento (Clustering)  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado los Capítulos 1 al 5 de la Unidad 2 (NumPy, métricas de distancia euclidiana y estandarización de variables).  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10, Espacio 12: Bloque Aprendizaje No Supervisado).

---

## 1. El Paradigma del Aprendizaje No Supervisado

En el aprendizaje supervisado (como Naive Bayes, k-NN o árboles CART), cada muestra de entrenamiento cuenta con una etiqueta objetivo `y` (*ground truth*) que guía el ajuste del modelo mediante la minimización de una función de pérdida supervisada.

En contraste, el **Aprendizaje No Supervisado (*Unsupervised Learning*)** aborda problemas donde los datos consisten exclusivamente en vectores de características `X = {x_1, x_2, ..., x_n}` **sin etiquetas de clase ni valores objetivo conocidos**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│            COMPARACIÓN: APRENDIZAJE SUPERVISADO VS NO SUPERVISADO      │
├───────────────────────────────┬────────────────────────────────────────┤
│ Supervisado (Clasificación)   │ Entrada: (X, y)                        │
│                               │ Meta: Aprender función f: X -> y       │
│                               │ Guía: Error respecto a etiquetas reales│
├───────────────────────────────┼────────────────────────────────────────┤
│ No Supervisado (Clustering)   │ Entrada: X (sin etiquetas y)           │
│                               │ Meta: Descubrir estructura latente     │
│                               │ Guía: Densidad, distancia y similitud  │
└───────────────────────────────┴────────────────────────────────────────┘
```

> **Cita del Anexo I (Res. 2730/22, Sección 10):**  
> En el Bloque Aprendizaje No Supervisado, los contenidos curriculares oficiales prescriben:  
> *«Elaboración del modelo. Características. Ejemplos y aplicaciones. Comparación y selección de modelos. Agrupamiento (Clustering). Estrategia Aglomerativa. Algoritmo k-medias. Aprendizaje por refuerzo»*.

---

## 2. Elaboración del Modelo No Supervisado

Elaborar un modelo no supervisado implica definir formalmente tres componentes:
1. **Espacio de Características (*Feature Space*):** Representación geométrica `D`-dimensional donde cada observación es un punto `x in R^D`.
2. **Medida de Proximidad o Disimilitud:** Función de distancia `d(x_i, x_j)` que cuantifica qué tan parecidas son dos observaciones (típicamente distancia euclidiana, Manhattan o similitud coseno).
3. **Criterio de Agrupamiento:** Función objetivo que premia la **alta cohesión intra-cluster** (elementos del mismo grupo muy cercanos entre sí) y la **alta separación inter-cluster** (distintos grupos alejados unos de otros).

---

## 3. Características y Preparación del Espacio de Datos

En el aprendizaje no supervisado, la calidad de las características es crítica: no existe una señal supervisada que descarte ruido automáticamente.

### Reglas esenciales de ingeniería de características:
* **Estandarización obligatoria:** Variables continuas en diferentes unidades (por ejemplo, Potencia Activa en Watts [0 a 5000] y Factor de Potencia [0.0 a 1.0]) deben escalarse con media 0 y varianza unitaria (`StandardScaler`). De lo contrario, la variable de mayor magnitud dominará artificialmente la geometría del espacio.
* **Manejo de dimensionalidad:** En espacios de muy alta dimensión, la distancia entre cualquier par de puntos tiende a homogeneizarse (*Maldición de la Dimensionalidad*). Es prioritario seleccionar atributos físicos representativos.

---

## 4. Ejemplos y Aplicaciones Reales

El agrupamiento y modelado no supervisado es fundamental en múltiples sectores de la industria y los servicios técnicos:

1. **Monitoreo Energético y Desagregación de Cargas (NILM en `energy-ml`):**  
   Agrupar pulsos y transitorios de potencia sin etiquetas para descubrir cuántos y cuáles electrodomésticos o motores operan en una planta industrial.
2. **Segmentación de Usuarios y Perfiles de Consumo:**  
   Identificar patrones horarios de demanda eléctrica (consumidores diurnos, nocturnos o picos estacionales) para optimización tarifaria.
3. **Detección de Anomalías Operativas:**  
   Lecturas de telemetría que no se integran a ningún cluster denso representan fallas de aislamiento, fugas o desbalances de red.
4. **Bioinformática y Análisis Genómico:**  
   Agrupamiento de perfiles de expresión génica para identificar subtipos de patologías.

---

## 5. Concepto Fundamental de Agrupamiento (*Clustering*)

El **agrupamiento (*Clustering*)** consiste en dividir un conjunto de `N` objetos no etiquetados en `K` grupos o clusters `C = {C_1, C_2, ..., C_K}` de forma tal que:
- Cada muestra pertenezca a un grupo: `union(C_k) = X`.
- En particiones duras (*hard clustering*), los grupos sean disjuntos: `C_i intersect C_j = vacio` para todo `i != j`.
- La varianza interna de cada cluster sea mínima y la separación entre centroides sea máxima.

En las siguientes dos lecciones abordaremos las dos familias fundamentales de algoritmos de clustering exigidas por el Anexo I: la **Estrategia Aglomerativa** (clustering jerárquico) y el algoritmo **k-medias** (clustering particional).

---

## Autoevaluación Formativa

1. ¿Por qué el escalado o estandarización es aún más crítico en clustering que en modelos supervisados con regularización?
2. En el contexto del monitoreo no intrusivo de cargas (`energy-ml`), ¿qué representa físicamente un cluster descubierto en el plano de Potencia Activa vs Potencia Reactiva?
