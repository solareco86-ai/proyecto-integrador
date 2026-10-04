# Lección 3.1: Entropía, Ganancia de Información (ID3/C4.5) e Impureza de Gini (CART) en energy-ml

En las lecciones previas analizamos algoritmos de cobertura secuencial (*Separate-and-Conquer*) que inducen reglas lógicas independientes. En este capítulo nos enfocamos en el paradigma de **partición jerárquica recursiva** (*Divide-and-Conquer*): los **Árboles de Decisión**.

Los árboles de decisión son uno de los pilares del Machine Learning industrial gracias a su capacidad de modelar interacciones no lineales entre variables continuas y categóricas, manteniendo una estructura de grafo totalmente interpretable. En el ecosistema de ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md), los utilizamos para clasificar contingencias en subestaciones eléctricas a partir de la telemetría de monitoreo continuo.

---

## 1. El Concepto de Pureza en Distribuciones de Clases

Imaginemos un conjunto `S` con 100 muestras de telemetría de transformadores, clasificadas en tres estados operativos:
- `NORMAL`
- `ALERTA_TERMICA`
- `FALLA_CRITICA`

Un nodo en el árbol es **completamente puro** si todas las muestras que contiene pertenecen a la misma clase (incertidumbre nula). En cambio, es **máximamente impuro** si las muestras se reparten en partes iguales entre las tres clases posibles (incertidumbre máxima).

Para seleccionar de forma óptima cuál variable de telemetría debe encabezar cada partición del árbol, los algoritmos recurren a métricas cuantitativas de impureza: **Entropía de Shannon** (ID3, C4.5) e **Impureza de Gini** (CART).

---

## 2. Entropía de Shannon y Ganancia de Información

### Fórmula de la Entropía
La entropía mide la cantidad esperada de información (o grado de sorpresa) requerida para identificar la clase de una muestra aleatoria en el conjunto `S`:
```
H(S) = - Sumatoria [ p_i * log2(p_i) ]   para cada clase i de 1 a c
```
Donde `p_i` representa la proporción (probabilidad empírica) de muestras que pertenecen a la clase `i`.

- **Mínimo:** `H(S) = 0.0` cuando todas las muestras son de una misma clase (`p_1 = 1.0`, y `1.0 * log2(1.0) = 0`).
- **Máximo:** Para 2 clases equiprobables (`p_1 = 0.5, p_2 = 0.5`), `H(S) = - (0.5 * (-1) + 0.5 * (-1)) = 1.0` bit.
- Para 4 clases equiprobables (`p_i = 0.25`), `H(S) = - (4 * 0.25 * (-2)) = 2.0` bits.

### Ganancia de Información (Algoritmo ID3)
La **Ganancia de Información** `IG(S, A)` representa la reducción esperada en entropía resultante de particionar el conjunto `S` según los valores del atributo `A`:
```
IG(S, A) = H(S) - Sumatoria [ (|S_v| / |S|) * H(S_v) ]
```
Donde `S_v` es el subconjunto de muestras donde el atributo `A` toma el valor `v`. El algoritmo evalúa todos los atributos disponibles y elige aquel que maximice la ganancia de información.

---

## 3. Impureza de Gini (Algoritmo CART)

El algoritmo **CART** (*Classification and Regression Trees*), que constituye la base de la clase `DecisionTreeClassifier` de Scikit-Learn en Python, utiliza por defecto el **Índice de Impureza de Gini**:

```
Gini(S) = 1 - Sumatoria [ (p_i)^2 ]   para cada clase i de 1 a c
```

Mide la probabilidad de que una muestra seleccionada al azar del conjunto sea clasificada incorrectamente si se le asignara una etiqueta aleatoria de acuerdo con la distribución de clases en el nodo.

- **Mínimo:** `Gini(S) = 0.0` (pureza total, todas las muestras de la misma clase).
- **Máximo (2 clases):** Si `p_1 = 0.5` y `p_2 = 0.5`, `Gini(S) = 1 - (0.25 + 0.25) = 0.5`.

### ¿Por qué Scikit-Learn prefiere Gini sobre Entropía?
Ambas métricas producen árboles notablemente similares en la práctica (discrepan en menos del 2% de las decisiones de partición). Sin embargo, Gini presenta una ventaja computacional crítica:
- **Cero funciones trigonométricas o logarítmicas:** Gini solo requiere operaciones aritméticas básicas (multiplicaciones y restas), mientras que la entropía exige calcular logaritmos en base 2 (`log2`) en coma flotante para cada clase en cada candidato de partición.
- En datasets industriales de alta frecuencia como la telemetría de `energy-ml` (millones de muestras de sensores), la optimización en CPU es sustancial.

---

## 4. Ejemplo Práctico de Partición en energy-ml

Analicemos la raíz del árbol con un dataset de 80 transformadores:
- 40 en estado `NORMAL` (`p = 0.5`)
- 40 en estado `FALLA_CRITICA` (`p = 0.5`)

Impureza inicial:
```
Gini_raiz = 1 - (0.5^2 + 0.5^2) = 1 - 0.5 = 0.50
```

Se evalúa la partición por el umbral `temperatura_aceite <= 80.0 °C`:

### Rama Izquierda (`T <= 80 °C`): 42 muestras
- 38 `NORMAL` (`p = 38/42 = 0.905`)
- 4 `FALLA_CRITICA` (`p = 4/42 = 0.095`)
- `Gini_izq = 1 - (0.905^2 + 0.095^2) = 1 - (0.819 + 0.009) = 0.172`

### Rama Derecha (`T > 80 °C`): 38 muestras
- 2 `NORMAL` (`p = 2/38 = 0.053`)
- 36 `FALLA_CRITICA` (`p = 36/38 = 0.947`)
- `Gini_der = 1 - (0.053^2 + 0.947^2) = 1 - (0.003 + 0.897) = 0.100`

### Impureza Ponderada de la Partición:
```
Gini_ponderado = (42 / 80) * 0.172 + (38 / 80) * 0.100
               = 0.525 * 0.172 + 0.475 * 0.100
               = 0.090 + 0.047
               = 0.137
```

### Ganancia de Gini (Reducción de Impureza):
```
Delta_Gini = 0.50 - 0.137 = 0.363
```
Una reducción masiva de la impureza (de 0.50 a 0.137), demostrando que `temperatura_aceite <= 80.0 °C` es un discriminador fundamental en la red eléctrica.

En la siguiente lección extenderemos este mecanismo hacia **árboles de regresión** para variables continuas y analizaremos técnicas de poda para evitar el sobreajuste.
