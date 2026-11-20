# Lección 6.5: Introducción al Aprendizaje por Refuerzo: Agentes, Entornos, Recompensas y Políticas

**Asignatura:** Unidad 2 — Machine Learning e Inferencia Estadística  
**Capítulo 6:** Bloque Aprendizaje No Supervisado y Agrupamiento (Clustering)  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado las Lecciones 6.1 a 6.4 (Fundamentos del aprendizaje a partir de datos sin etiquetas supervisadas).  
**Fuente normativa:** Resolución DGCyE N° 2730/22 (Anexo I, Sección 10, Espacio 12: Bloque Aprendizaje No Supervisado: *«Aprendizaje por refuerzo»*).

---

## 1. Ubicación Normativa y Conceptual

En la taxonomía del diseño curricular oficial (Res. 2730/22, Anexo I, Espacio 12), el **Aprendizaje por Refuerzo (*Reinforcement Learning - RL*)** se introduce como contenido del *Bloque Aprendizaje No Supervisado*. 

Aunque en la literatura técnica contemporánea el RL suele conceptualizarse como un tercer paradigma propio del aprendizaje automático, comparte con el aprendizaje no supervisado una característica medular: **no existe un supervisor externo que proporcione la etiqueta correcta (*ground truth*) o la respuesta óptima para cada estado**. El sistema debe descubrir de forma autónoma cuáles acciones generan el mejor rendimiento interactuando con su entorno.

```text
┌────────────────────────────────────────────────────────────────────────┐
│               TAXONOMÍA DE LOS PARADIGMAS DE APRENDIZAJE               │
├───────────────────────────┬────────────────────────────────────────────┤
│ 1. Aprendizaje            │ Entrada: (X, y).                           │
│    Supervisado            │ Se aprende a mapear entradas a etiquetas   │
│                           │ conocidas provistas por un supervisor.     │
├───────────────────────────┼────────────────────────────────────────────┤
│ 2. Aprendizaje            │ Entrada: X (sin etiquetas).                │
│    No Supervisado         │ Se descubre estructura latente, densidad   │
│                           │ o agrupamientos intrínsecos de los datos.  │
├───────────────────────────┼────────────────────────────────────────────┤
│ 3. Aprendizaje            │ Entrada: Señales de recompensa r(t).       │
│    por Refuerzo           │ Un agente aprende mediante prueba y error  │
│                           │ qué acciones maximizan el retorno a futuro.│
└───────────────────────────┴────────────────────────────────────────────┘
```

---

## 2. Los Componentes del Bucle Agente-Entorno

El marco formal del Aprendizaje por Refuerzo se estructura a través del bucle de interacción entre dos entidades:

```text
                  Acción a(t)
         ┌───────────────────────────┐
         │                           ▼
   ┌───────────┐               ┌───────────┐
   │           │               │           │
   │  AGENTE   │               │  ENTORNO  │
   │           │               │           │
   └───────────┘               └───────────┘
         ▲                           │
         │  Estado s(t+1)            │
         │  Recompensa r(t+1)        │
         └───────────────────────────┘
```

1. **Agente (*Agent*):** Entidad que toma decisiones y ejecuta acciones para alcanzar un objetivo (por ejemplo, el controlador inteligente de despacho de carga en una microrred de `energy-ml`).
2. **Entorno (*Environment*):** El mundo o sistema físico/simulado con el cual interactúa el agente.
3. **Estado `s in S`:** Representación cuantitativa de la situación actual del entorno (ej: nivel de carga de batería, demanda de potencia actual y tarifa eléctrica del bloque horario).
4. **Acción `a in A`:** Operación que el agente puede ejecutar en un estado dado (ej: cargar batería, descargar batería o mantenerse en espera).
5. **Recompensa `r in R`:** Valor escalar numérico que el entorno devuelve al agente tras ejecutar una acción. Premia conductas deseables (ahorro de costos, estabilidad) o penaliza errores (picos de demanda, desgaste innecesario).

---

## 3. Políticas y Funciones de Valor

El objetivo del agente es aprender una **Política `pi(a|s)`**, que define la probabilidad de elegir la acción `a` encontrándose en el estado `s`, de manera tal de maximizar la **Recompensa Acumulada Descontada (*Return*)**:

```text
G(t) = r(t+1) + gamma * r(t+2) + (gamma^2) * r(t+3) + ...
```
Donde `gamma in [0, 1)` es el **factor de descuento**: un `gamma` cercano a 0 prioriza recompensas inmediatas, mientras que un `gamma` cercano a 1 pondera los beneficios estratégicos a largo plazo.

### Función Acción-Valor `Q(s, a)` y la Ecuación de Bellman
La función `Q(s, a)` estima el retorno esperado que obtendrá el agente si ejecuta la acción `a` en el estado `s` y luego continúa siguiendo la política óptima. La relación fundamental de optimización se rige por la **Ecuación de Optimalidad de Bellman**:

```text
Q*(s, a) = r + gamma * max_{a'} Q*(s', a')
```

---

## 4. El Dilema Exploración vs Explotación

Para encontrar la política óptima, el agente enfrenta un compromiso permanente:
* **Explotación (*Exploitation*):** Ejecutar la acción que actualmente tiene el mayor valor `Q` conocido para asegurar recompensas altas.
* **Exploración (*Exploration*):** Intentar acciones alternativas menos probadas para descubrir si conducen a resultados todavía mejores a futuro.

La estrategia clásica para resolver este dilema es la política **epsilon-greedy**:
- Con probabilidad `1 - epsilon`: el agente **explota** eligiendo `argmax_a Q(s, a)`.
- Con probabilidad `epsilon`: el agente **explora** eligiendo una acción al azar.

---

## 5. Implementación Práctica: Algoritmo Q-Learning Tabular en Python

A continuación se presenta una implementación mínima y pedagógica de **Q-Learning** en Python estándar para optimizar la conmutación de almacenamiento de energía según bloques tarifarios:

```python
import numpy as np

# Espacio de Estados: 3 niveles de batería (0: Baja, 1: Media, 2: Alta)
# Espacio de Acciones: 3 acciones (0: Cargar de la red, 1: Espera, 2: Inyectar/Descargar)
NUM_ESTADOS = 3
NUM_ACCIONES = 3

# Tabla Q inicializada en ceros: Q[estado, accion]
tabla_q = np.zeros((NUM_ESTADOS, NUM_ACCIONES))

# Hiperparámetros de aprendizaje
alfa = 0.1       # Tasa de aprendizaje (Learning rate)
gamma = 0.9      # Factor de descuento
epsilon = 0.2    # Probabilidad de exploración
episodios = 500

# Simulación simplificada del entorno de red eléctrica
def paso_entorno(estado: int, accion: int) -> tuple[int, float]:
    """Retorna (nuevo_estado, recompensa) según la acción de despacho."""
    if accion == 0:  # Cargar batería (costo si la red está en hora pico)
        nuevo_estado = min(estado + 1, NUM_ESTADOS - 1)
        recompensa = -2.0  # Costo de compra de energía
    elif accion == 2:  # Descargar batería (beneficio al evitar consumir de red)
        if estado > 0:
            nuevo_estado = estado - 1
            recompensa = +5.0  # Ahorro significativo
        else:
            nuevo_estado = estado
            recompensa = -10.0  # Penalización: batería vacía
    else:  # Espera
        nuevo_estado = estado
        recompensa = 0.0

    return nuevo_estado, recompensa

# Bucle de entrenamiento por Q-Learning
np.random.seed(42)
for ep in range(episodios):
    estado = np.random.randint(0, NUM_ESTADOS)
    for _ in range(10):
        # Política epsilon-greedy
        if np.random.rand() < epsilon:
            accion = np.random.randint(0, NUM_ACCIONES)
        else:
            accion = int(np.argmax(tabla_q[estado]))

        nuevo_estado, recompensa = paso_entorno(estado, accion)

        # Actualización de la regla de Bellman para Q-Learning:
        # Q(s, a) <- Q(s, a) + alfa * [r + gamma * max_a' Q(s', a') - Q(s, a)]
        mejor_q_futuro = np.max(tabla_q[nuevo_estado])
        td_target = recompensa + gamma * mejor_q_futuro
        td_error = td_target - tabla_q[estado, accion]
        tabla_q[estado, accion] += alfa * td_error

        estado = nuevo_estado

print("=== TABLA Q CONVERGIDA TRAS ENTRENAMIENTO ===")
print("Filas = Estados (Batería 0, 1, 2) | Columnas = Acciones (0:Cargar, 1:Espera, 2:Descargar)")
print(np.round(tabla_q, 2))
```

---

## 6. Conexión con la Arquitectura de Agentes Inteligentes

En las unidades avanzadas del campus (Unidad 3: Model Context Protocol y Agentes Autónomos), el concepto de bucle de interacción, toma de decisiones secuenciales y evaluación de consecuencias conecta directamente con el diseño de **agentes de razonamiento autónomo**. Comprender las funciones de recompensa y las políticas de decisión proporciona la base matemática para evaluar sistemas agenticos que operan en producción.
