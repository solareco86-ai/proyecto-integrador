# Lección 0.1: Álgebra Matricial Intuitiva, Tensores y Vectorización en CPU con NumPy

En la Unidad 1 aprendimos a configurar nuestro entorno de desarrollo en GNU/Linux y WSL, dominar Git y crear nuestros primeros endpoints en FastAPI. Al ingresar a la **Unidad 2**, nos encontramos con un salto fundamental: la transición desde la programación estructurada tradicional (basada en diccionarios, listas y bucles `for`) hacia el **cálculo numérico vectorial y matricial**.

Muchos estudiantes experimentan una sobrecarga cognitiva en este pasaje porque los modelos de Machine Learning (como Naive Bayes, k-NN o regresiones) no procesan objetos heterogéneos de Python, sino bloques homogéneos de memoria contigua denominados **tensores**.

En esta lección puente de nivelación activa sobre ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md), desmitificamos el álgebra lineal aplicada a la telemetría eléctrica y aprendemos a operar con NumPy en la CPU local con máxima eficiencia.

---

## 1. El Problema del Rendimiento: Listas de Python vs. NumPy Arrays

Una lista estándar de Python (`list`) es un arreglo dinámico de punteros a objetos dispersos en memoria RAM. Cada elemento cuenta con una cabecera de metadatos de CPython (`PyObject`), lo que introduce una sobrecarga considerable:

```
Lista de Python:  [ Ptr0 ] -> [ PyFloat: 220.4 ]
                  [ Ptr1 ] -> [ PyFloat: 221.1 ]
                  [ Ptr2 ] -> [ PyFloat: 219.8 ]
                  (Memoria fragmentada, saltos de puntero en cache L1/L2)

NumPy ndarray:    [ 220.4 | 221.1 | 219.8 | 220.9 | 222.0 ]
                  (Bloque binario contiguo en memoria, vectorización SIMD directa)
```

En un alimentador de media tensión que transmite 50 lecturas de corriente por segundo (3.000 lecturas por minuto):
- Un bucle `for` tradicional en Python para calcular el valor eficaz (RMS) tarda **~45 milisegundos**.
- La misma operación vectorizada con `np.sqrt(np.mean(corriente ** 2))` tarda **~0.15 milisegundos** (un incremento de velocidad superior a **300x** en la CPU local).

---

## 2. Jerarquía de Tensores en Telemetría Eléctrica

Un **tensor** no es un concepto abstracto inalcanzable; es simplemente la generalización de un arreglo numérico a `n` dimensiones:

| Rango / Dimensión | Nombre Común | Forma en NumPy (`shape`) | Significado Físico en energy-ml |
| :--- | :--- | :--- | :--- |
| **0D** | Escalar | `()` | Una medición puntual (ej: `temperatura = 78.4` °C). |
| **1D** | Vector | `(features,)` | Una observación multivariable: `[tension, corriente, temp, thd]`. |
| **2D** | Matriz | `(muestras, features)` | Lote histórico de telemetría: `N` muestras y `M` atributos. Es la convención `X` en Scikit-Learn. |
| **3D** | Tensor 3D | `(subestaciones, tiempo, canales)` | Monitoreo simultáneo de 5 subestaciones durante 24 horas en 4 sensores. |

---

## 3. Vectorización y Broadcasting en la Práctica

El **broadcasting** (difusión) permite a NumPy realizar operaciones aritméticas entre arreglos de diferentes formas sin duplicar datos en memoria.

Supongamos que tenemos una matriz de mediciones crudas `X` con 4 muestras y 3 variables (`[tension_kV, corriente_A, temp_C]`):

```python
import numpy as np

# Matriz 2D de telemetría (4 subestaciones, 3 sensores)
X = np.array(
    [
        [13.2, 420.0, 75.0],
        [13.1, 410.0, 72.0],
        [13.8, 580.0, 91.0],  # Evento anómalo de sobrecarga
        [13.2, 430.0, 76.0],
    ],
    dtype=np.float64,
)

# Vector 1D con las medias nominales de cada sensor (shape: (3,))
medias_nominales = np.array([13.2, 420.0, 75.0], dtype=np.float64)

# Broadcasting automático: resta el vector de 3 elementos a cada una de las 4 filas
desviacion = X - medias_nominales

print("Matriz de desviación respecto al valor nominal:")
print(desviacion)
```

Salida directa en consola:
```text
[[  0.    0.    0. ]
 [ -0.1 -10.   -3. ]
 [  0.6 160.   16. ]
 [  0.   10.    1. ]]
```
Sin escribir un solo bucle `for`, identificamos instantáneamente que la fila 2 supera en +160 A y +16 °C los valores nominales.

---

## 4. Tipado Estricto de Arreglos en energy-ml

Para evitar diagnósticos de tipo desconocido (`reportUnknownVariableType`) y garantizar la robustez arquitectónica en Python 3.12+, utilizamos las anotaciones de tipo provistas por NumPy:

```python
from typing import TypeAlias
import numpy as np
import numpy.typing as npt

# Alias de tipo explícito para matrices de características en Scikit-Learn
MatrizFeatures: TypeAlias = npt.NDArray[np.float64]
VectorEtiquetas: TypeAlias = npt.NDArray[np.int64]


def estandarizar_telemetria(X: MatrizFeatures) -> MatrizFeatures:
    """Aplica escalado z-score por columna a la matriz de telemetría."""
    media = np.mean(X, axis=0)
    desviacion_std = np.std(X, axis=0)

    # Evitar división por cero si un sensor permanece constante
    desviacion_std = np.where(desviacion_std == 0.0, 1.0, desviacion_std)

    return (X - media) / desviacion_std
```

---

## 5. Autoevaluación Formativa y Caza de Código Alucinado

### Pregunta de Razonamiento Conceptual
1. Si un sensor de tensión transmite una señal continua de 10.000 lecturas por segundo durante 1 hora, ¿cuál es la forma (`shape`) del tensor NumPy resultante para un único alimentador trifásico (3 fases simultáneas)?
   - *Respuesta:* Un arreglo 2D de `shape = (36_000_000, 3)` con `dtype=np.float32` o `float64`.

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente fragmento propuesto por un asistente de IA para calcular la distancia euclidiana entre una nueva muestra de telemetría `x_nuevo` (vector 1D) y un lote histórico `X_historico` (matriz 2D):

```python
# CÓDIGO CON ERROR PROPUESTO POR LA IA:
def calcular_distancias_alucinado(X_historico, x_nuevo):
    distancias = []
    for i in range(len(X_historico)):
        fila = X_historico[i]
        d = 0
        for j in range(len(fila)):
            d += (fila[j] - x_nuevo[j]) ** 2
        distancias.append(d**0.5)
    return distancias
```

**Diagnóstico del Revisor Humano:**
1. **Pérdida de Vectorización:** El código destruye el beneficio de NumPy implementando dos bucles anidados en Python interpretado, ralentizando la inferencia hasta 500 veces.
2. **Corrección Idiomática Vectorizada ($0 bucles):**
   ```python
   def calcular_distancias_vectorizado(
       X_historico: np.ndarray, x_nuevo: np.ndarray
   ) -> np.ndarray:
       # Broadcasting de la resta, elevación al cuadrado y suma por fila (axis=1)
       return np.linalg.norm(X_historico - x_nuevo, axis=1)
   ```

---

## 6. Comando de Verificación de 1 Minuto

Verifica en tu terminal la instalación y funcionamiento de las operaciones vectorizadas de NumPy:

```bash
python3 -c "
import numpy as np
X = np.random.randn(1000, 4)
print('Shape:', X.shape, '| Media global:', round(float(X.mean()), 4), '| Vectorización OK')
"
```

Con este andamiaje consolidado, estamos listos para adentrarnos en el **Capítulo 1 de la Unidad 2**, modelando esquemas Pydantic y administrando la memoria del servidor FastAPI con total solvencia.
