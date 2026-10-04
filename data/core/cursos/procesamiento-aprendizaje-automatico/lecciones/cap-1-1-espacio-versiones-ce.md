# Lección 1.1: Generalización y especialización: algoritmo Candidate-Elimination en energy-ml

En las unidades anteriores exploramos modelos probabilísticos (Naive Bayes) y basados en distancias métricas (k-NN) para clasificar contingencias operativas en redes de distribución eléctrica. En esta tercera unidad nos adentramos en el **aprendizaje simbólico y la programación lógica**, donde el objetivo no es únicamente estimar una probabilidad continua, sino inducir representaciones declarativas exactas, interpretables y auditables por ingenieros de campo y agentes autónomos.

El aprendizaje de conceptos formula el entrenamiento como un problema de búsqueda formal a través de un espacio predefinido de hipótesis lógicas. El algoritmo **Candidate-Elimination** (propuesto originalmente por Tom Mitchell) es el método fundamental para delimitar y refinar el conjunto exacto de todas las hipótesis consistentes con los datos observados.

---

## 1. El Problema de Aprendizaje de Conceptos en Subestaciones Eléctricas

En la infraestructura de ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md), los centros de control requieren identificar condiciones determinísticas bajo las cuales se produce un evento crítico: **Disparo por Falla Térmica en Transformador** (`FallaDisparo = True`).

A diferencia de un modelo de caja negra, los inspectores regulatorios y los sistemas SCADA necesitan una regla lógica inequívoca que describa exactamente la combinación de factores causales. Para formalizar el problema, discretizamos la telemetría de monitoreo continuo en cuatro atributos clave:

1. **`tension_red`**: `["baja", "nominal", "alta"]`
2. **`carga_trafo`**: `["ligera", "nominal", "critica"]`
3. **`temperatura_aceite`**: `["normal", "elevada", "extrema"]`
4. **`armonicos_thd`**: `["admisible", "alto"]`

Una instancia de telemetría se describe como una tupla:
```python
x = ("alta", "critica", "elevada", "alto")
```
Y la función objetivo booleana es:
```
c: Instancia -> {True, False}
```

---

## 2. Lenguaje de Representación de Hipótesis

Una hipótesis `h` es una conjunción de restricciones sobre los atributos. Para cada atributo, la hipótesis puede exigir:
- Un valor específico (ej. `"alta"`).
- Cualquier valor admisible: denotado con el comodín `?` (máxima generalidad).
- Ningún valor admisible: denotado con `0` (hipótesis nula, máxima especificidad).

Por ejemplo, la hipótesis:
```
h = ("alta", "critica", "?", "alto")
```
Afirma que *ocurre un disparo térmico si la tensión de red es alta, la carga es crítica y los armónicos son altos, sin importar cuál sea la temperatura del aceite*.

### Relación de Generalidad Parcial (Más General o Igual Que)
Dadas dos hipótesis `h1` y `h2`, decimos que `h1` es más general o igual que `h2` (`h1 >= h2`) si y solo si todo ejemplo positivo satisfecho por `h2` también es satisfecho por `h1`.

- `("?", "?", "?", "?")`: La hipótesis más general posible. Clasifica todo evento como disparo inminente.
- `("0", "0", "0", "0")`: La hipótesis más específica posible. Rechaza todos los eventos (clasifica todo como `False`).

---

## 3. Estructura del Espacio de Versiones

El **Espacio de Versiones** respecto a un conjunto de ejemplos de entrenamiento `D` es el subconjunto de todas las hipótesis que son perfectamente consistentes con cada muestra en `D` (satisfacen todos los ejemplos positivos y rechazan todos los ejemplos negativos).

En lugar de almacenar exhaustivamente miles de hipótesis intermedias, el algoritmo Candidate-Elimination representa el espacio de versiones de forma compacta mediante sus dos límites extremos en el reticulado de orden parcial:

```
                  Frontera General (G)
               [ ("?", "?", "?", "?") ]
                         /    \
                       v        v
           Hipótesis intermedias consistentes
                       ^        ^
                         \    /
               [ ("0", "0", "0", "0") ]
                 Frontera Específica (S)
```

1. **Frontera Específica (`S`):** El conjunto de las hipótesis más específicas que cubren todos los ejemplos positivos observados y ningún ejemplo negativo.
2. **Frontera General (`G`):** El conjunto de las hipótesis más generales que son consistentes con todos los ejemplos positivos y no cubren ningún ejemplo negativo.

---

## 4. Dinámica de Actualización del Algoritmo Candidate-Elimination

El espacio se inicializa en sus extremos teóricos:
```
S_0 = { ("0", "0", "0", "0") }
G_0 = { ("?", "?", "?", "?") }
```

A medida que el sistema SCADA de `energy-ml` transmite nuevas muestras etiquetadas `(x, y)`:

### Caso 1: La muestra es un Ejemplo Positivo (`y = True`)
El sistema debe expandir la frontera específica para no dejar afuera este evento:
1. Eliminar de `G` cualquier hipótesis que no satisfaga `x` (hipótesis inconsistente con un caso real).
2. Para cada hipótesis `s` en `S` que no satisfaga `x`:
   - Reemplazar `s` por su mínima generalización `s'` tal que `s'` satisfaga `x`, y exista alguna hipótesis en `G` que sea más general o igual que `s'`.
3. Eliminar de `S` las hipótesis que sean más generales que otra hipótesis presente en `S`.

### Caso 2: La muestra es un Ejemplo Negativo (`y = False`)
El sistema debe recortar la frontera general para no cubrir este evento normal:
1. Eliminar de `S` cualquier hipótesis que satisfaga `x` (inconsistente con el negativo).
2. Para cada hipótesis `g` en `G` que satisfaga `x`:
   - Reemplazar `g` por sus mínimas especializaciones `g'` tales que `g'` no satisfaga `x`, y exista alguna hipótesis en `S` que sea más específica o igual que `g'`.
3. Eliminar de `G` las hipótesis que sean menos generales que otra hipótesis presente en `G`.

---

## 5. Traza Práctica de Ejecución en energy-ml

Analicemos la evolución de las fronteras ante 3 eventos de telemetría en la subestación "Tigre Centro":

### Muestra 1: Evento Positivo (Disparo Confirmado)
- Telemetría: `("alta", "critica", "elevada", "alto") -> True`
- **Actualización:**
  - `S_1 = { ("alta", "critica", "elevada", "alto") }`
  - `G_1 = { ("?", "?", "?", "?") }`

### Muestra 2: Evento Positivo (Disparo Confirmado)
- Telemetría: `("alta", "critica", "extrema", "alto") -> True`
- **Actualización:**
  - La temperatura difiere (`"elevada"` vs `"extrema"`), por lo que la mínima generalización en `S` introduce el comodín `?` en el tercer atributo:
  - `S_2 = { ("alta", "critica", "?", "alto") }`
  - `G_2 = { ("?", "?", "?", "?") }`

### Muestra 3: Evento Negativo (Operación Normal, Sin Disparo)
- Telemetría: `("nominal", "critica", "elevada", "alto") -> False`
- **Actualización:**
  - `G_2` cubre este ejemplo negativo (al ser completamente general), por lo que debemos especializarlo mínimamente sin descartar a `S_2`.
  - El único atributo donde `S_2` y la muestra 3 difieren determinísticamente es la `tension_red` (`"alta"` vs `"nominal"`):
  - `S_3 = { ("alta", "critica", "?", "alto") }`
  - `G_3 = { ("alta", "?", "?", "?") }`

El espacio de versiones se ha estrechado dramáticamente: cualquier hipótesis válida debe asegurar al menos que `tension_red = "alta"`, mientras que la frontera más cautelosa añade que la carga sea crítica y el armónico alto.

---

## 6. Convergencia, Inconsistencias y Ruido

El algoritmo presenta tres estados finales posibles:

| Estado del Espacio | Condición Matemática | Significado Operativo en Red Eléctrica |
| :--- | :--- | :--- |
| **Convergencia Unívoca** | `S == G` y `|S| == 1` | El concepto ha sido aprendido exactamente sin ambigüedad. |
| **Indeterminación Parcial** | `S` y `G` son consistentes pero `S != G` | Se requieren más muestras de telemetría para desambiguar hipótesis intermedias. |
| **Colapso del Espacio** | `S` o `G` quedan vacíos (`S = {}` o `G = {}`) | Existen datos ruidosos o contradictorios en el dataset (ej. misma telemetría con etiquetas opuestas). |

> [!WARNING] Fragilidad ante el Ruido
> Si un sensor defectuoso reporta un falso positivo o negativo, el algoritmo descartará las hipótesis correctas provocando el colapso del espacio. Por ello, en ingeniería real se utiliza Candidate-Elimination sobre datos verificados o en conjunto con técnicas de tolerancia a fallas.

En la siguiente lección, expondremos este algoritmo como un servicio web interactivo en FastAPI dentro de `energy-ml`.
