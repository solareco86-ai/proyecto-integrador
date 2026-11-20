# Lección 6.6: Optimización y Algoritmos Genéticos: Selección, Cruzamiento, Mutación y Búsqueda Estocástica

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo 6:** Bloque Aprendizaje No Supervisado y Agrupamiento (Clustering)  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado las Lecciones 6.1 a 6.5.  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10.b: *«Capacidad 3: Resolver problemas de predicción y optimización usando algoritmos de clasificación, clustering y genéticos»*).

---

## 1. El Rol de la Optimización en Aprendizaje Automático

El aprendizaje automático puede entenderse en su raíz matemática como un problema de **búsqueda y optimización**: encontrar la configuración de parámetros o la estructura de modelo que maximice el rendimiento o minimice una función de costo.

Cuando la función objetivo es diferenciable y convexa, se emplean técnicas analíticas o basadas en gradiente (como el Descenso de Gradiente). Sin embargo, en la ingeniería de sistemas reales surgen problemas con:
* Espacios de búsqueda **discretos y combinatorios** (por ejemplo, selección de subconjuntos de características o asignación de turnos y cargas).
* Funciones de costo **no diferenciables, discontinuas o con múltiples óptimos locales**.
* Problemas NP-complejos con restricciones duras.

Para estos escenarios, los **Algoritmos Genéticos (AG / GA - *Genetic Algorithms*)** proporcionan una estrategia de optimización estocástica inspirada en los principios de la evolución biológica y la selección natural.

---

## 2. Anatomía de un Algoritmo Genético

Un algoritmo genético opera sobre una **población** de posibles soluciones candidatas llamadas **individuos** o **cromosomas**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   CICLO EVOLUTIVO DE UN ALGORITMO GENÉTICO             │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Población Inicial: Generación aleatoria de N cromosomas.            │
│ 2. Evaluación: Cálculo del Fitness f(x) de cada individuo.             │
│ 3. Criterio de Término: ¿Se alcanzó el fitness meta o max generaciones?│
│    -> Si: Finalizar y retornar mejor solución.                         │
│ 4. Selección: Los individuos más aptos tienen mayor probabilidad       │
│    de reproducirse (Torneo o Ruleta).                                  │
│ 5. Cruzamiento (Crossover): Intercambio de material genético entre     │
│    pares de padres para originar hijos.                                │
│ 6. Mutación: Modificación estocástica de genes con probabilidad p_m.   │
│ 7. Elitismo: Preservación de la mejor solución a la nueva generación.  │
│ 8. Retornar al Paso 2 con la nueva población.                          │
└────────────────────────────────────────────────────────────────────────┘
```

### Componentes Fundamentales:
1. **Genotipo y Fenotipo:** El genotipo es la codificación interna de la solución (comúnmente un vector binario `[1, 0, 1, 1, 0]` o un vector real). El fenotipo es su manifestación física en el problema real (ej: qué máquinas encender o qué sensores seleccionar).
2. **Función de Aptitud (*Fitness Function*):** Cuantifica la calidad de cada solución candidata respecto a los objetivos del problema.
3. **Operador de Cruzamiento (*Crossover*):** Combina segmentos de dos cromosomas progenitores para generar descendientes que hereden atributos favorables de ambos.
4. **Operador de Mutación (*Mutation*):** Introduce variabilidad aleatoria alterando genes aislados con baja probabilidad `p_m`, evitando que la población converja prematuramente a un óptimo local subóptimo.
5. **Elitismo (*Elitism*):** Garantiza que el mejor individuo de la generación actual sobreviva intacto a la siguiente generación, impidiendo la pérdida de soluciones óptimas ya descubiertas.

---

## 3. Laboratorio Pequeño: Optimización de Despacho Energético en energy-ml

En este laboratorio implementamos un algoritmo genético en Python puro para resolver un problema típico de **`energy-ml`**:  
Disponemos de un conjunto de cargas eléctricas industriales disponibles para encendido, cada una con su **beneficio operativo** y su **consumo de potencia (Watts)**. La acometida eléctrica tiene un **límite máximo de potencia contratada (15 kW)**. El objetivo es encontrar la combinación óptima de maquinaria que maximice el beneficio sin sobrepasar la potencia máxima permitida (*Problema de la Mochila / Knapsack Problem*).

```python
import numpy as np

# Datos del problema en energy-ml:
# (Nombre, Potencia en Watts, Beneficio productivo 1-100)
cargas = [
    ("Compresor 1", 4500, 75),
    ("Compresor 2", 3800, 60),
    ("Bomba Hidráulica A", 3200, 55),
    ("Bomba Hidráulica B", 2800, 48),
    ("Horno de Curado", 5000, 85),
    ("Extractor Principal", 1800, 30),
    ("Línea de Envasado", 2200, 45),
    ("Iluminación Planta", 1200, 25),
]
NUM_GENES = len(cargas)
POTENCIA_MAXIMA = 15000  # Límite contratado en Watts

# Función de Aptitud (Fitness)
def calcular_fitness(cromosoma: np.ndarray) -> float:
    potencia_total = sum(cargas[i][1] for i in range(NUM_GENES) if cromosoma[i] == 1)
    beneficio_total = sum(cargas[i][2] for i in range(NUM_GENES) if cromosoma[i] == 1)

    # Penalización severa si supera la potencia contratada
    if potencia_total > POTENCIA_MAXIMA:
        return 0.0  # Inviable
    return float(beneficio_total)

# Hiperparámetros del Algoritmo Genético
TAM_POBLACION = 30
GENERACIONES = 40
TASA_MUTACION = 0.05
np.random.seed(42)

# Inicialización de población binaria aleatoria
poblacion = np.random.randint(0, 2, size=(TAM_POBLACION, NUM_GENES))

mejor_fitness_historico = 0.0
mejor_solucion = poblacion[0]

for gen in range(GENERACIONES):
    fitness = np.array([calcular_fitness(ind) for ind in poblacion])
    
    # Identificar el mejor individuo (Elitismo)
    idx_mejor = int(np.argmax(fitness))
    if fitness[idx_mejor] > mejor_fitness_historico:
        mejor_fitness_historico = fitness[idx_mejor]
        mejor_solucion = poblacion[idx_mejor].copy()

    # Selección por Torneo (tamaño = 3)
    nueva_poblacion = [mejor_solucion.copy()]  # Conservar el mejor (Elitismo)
    while len(nueva_poblacion) < TAM_POBLACION:
        candidatos_a = np.random.choice(TAM_POBLACION, 3, replace=False)
        padre_a = poblacion[candidatos_a[np.argmax(fitness[candidatos_a])]]
        candidatos_b = np.random.choice(TAM_POBLACION, 3, replace=False)
        padre_b = poblacion[candidatos_b[np.argmax(fitness[candidatos_b])]]

        # Cruzamiento de un punto (Single-Point Crossover)
        punto = np.random.randint(1, NUM_GENES)
        hijo = np.concatenate([padre_a[:punto], padre_b[punto:]])

        # Mutación bit a bit
        for g in range(NUM_GENES):
            if np.random.rand() < TASA_MUTACION:
                hijo[g] = 1 - hijo[g]

        nueva_poblacion.append(hijo)

    poblacion = np.array(nueva_poblacion)

print("=== OPTIMIZACIÓN GENÉTICA FINALIZADA ===")
print(f"Mejor Beneficio Alcanzado: {mejor_fitness_historico} pts")
potencia_final = sum(cargas[i][1] for i in range(NUM_GENES) if mejor_solucion[i] == 1)
print(f"Potencia Total Demandada: {potencia_final} W (Límite: {POTENCIA_MAXIMA} W)")
print("\nCargas Seleccionadas para Operación:")
for i in range(NUM_GENES):
    if mejor_solucion[i] == 1:
        print(f" - [X] {cargas[i][0]}: {cargas[i][1]} W ({cargas[i][2]} pts)")
```

---

## 4. Articulación de la Capacidad Profesional 3 del Anexo I

La **Capacidad Profesional 3** exige:  
*«Resolver problemas de predicción y optimización usando algoritmos de clasificación, clustering y genéticos»*.

En este curso articulamos las tres componentes:
1. **Predicción (Clasificación):** Naive Bayes, k-NN y Árboles CART para clasificar estados operativos y transitorios en la red.
2. **Clustering:** k-medias y Estrategia Aglomerativa para descubrir perfiles de carga no etiquetados (NILM).
3. **Optimización (Algoritmos Genéticos):** Metaheurística evolutiva para sintonizar hiperparámetros y optimizar decisiones de conmutación de potencia en escenarios con restricciones físicas complejas.
