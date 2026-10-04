# Lección 2.1: Algoritmo AQ y Cobertura Secuencial: Extracción de Reglas Interpretables en energy-ml

En entornos industriales críticos y sistemas eléctricos de potencia, la precisión predictiva de un modelo es insuficiente si no va acompañada de **explicabilidad total y auditoría determinística**. Cuando un transformador de 40 MVA o un alimentador de 33 kV experimenta un disparo de protección, los operadores del centro de control y los inspectores regulatorios (como el ENRE o CAMMESA) exigen conocer exactamente qué condiciones físicas motivaron la maniobra de despeje.

En esta lección estudiamos el **Algoritmo AQ** (desarrollado por Ryszard Michalski) y la estrategia de **cobertura secuencial** (*Separate-and-Conquer*), técnica fundacional del Machine Learning simbólico para inducir conjuntos de reglas de la forma:
```
SI [condición_1 Y condición_2 Y ...] ENTONCES [estado_contingencia]
```

---

## 1. Cobertura Secuencial: El Paradigma *Separate-and-Conquer*

A diferencia de los árboles de decisión, que particionan recursivamente el espacio completo mediante una estrategia jerárquica (*Divide-and-Conquer*), los algoritmos de cobertura secuencial construyen reglas disyuntivas una a una mediante la estrategia *Separate-and-Conquer* (Separar y Conquistar):

```
+-------------------------------------------------------+
| 1. Seleccionar un ejemplo positivo semilla (seed)      |
|    que aún no esté cubierto por ninguna regla.        |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
| 2. Encontrar la mejor regla (Estrella en AQ) que      |
|    cubra la semilla y la mayor cantidad de positivos, |
|    sin cubrir ningún ejemplo negativo.                |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
| 3. Añadir la regla inducida al conjunto final.        |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
| 4. Eliminar (Separar) del dataset todos los ejemplos   |
|    positivos cubiertos por la nueva regla.            |
+-------------------------------------------------------+
                           |
                           v
+-------------------------------------------------------+
| 5. ¿Quedan ejemplos positivos sin cubrir?             |
|    - SÍ: Repetir desde el paso 1.                     |
|    - NO: Finalizar inducción.                         |
+-------------------------------------------------------+
```

Al remover en cada iteración los ejemplos ya explicados, el algoritmo reduce progresivamente la complejidad del problema hasta alcanzar una cobertura exhaustiva del concepto.

---

## 2. Generación del Complejo Estrella (Star) en el Algoritmo AQ

En el algoritmo AQ, una condición elemental se denomina **selector** (ej. `temperatura_aceite > 85.0 °C` o `carga_trafo = 'critica'`). Una conjunción de selectores forma un **complejo** (término lógico equivalente a una regla conjuntiva).

El proceso de inducción de una regla individual para una semilla positiva `e+` opera del siguiente modo:
1. Se toma `e+` y se compara contra cada ejemplo negativo `e-` en el dataset de entrenamiento.
2. Para cada `e-`, se generan todos los selectores más generales que son verdaderos para `e+` pero falsos para `e-`.
3. Se realiza la intersección lógica (producto cartesiano conjuntivo) de estos selectores para formar la **Estrella** de hipótesis admisibles:
   ```
   Star(e+ | e-) = { complejo C | C cubre e+  Y  C no cubre ningún e- }
   ```
4. Para evitar la explosión combinatoria, el algoritmo implementa una búsqueda en haz (*Beam Search*) con un parámetro `max_star` que retiene únicamente los `k` mejores complejos ordenados por cobertura y simplicidad sintáctica (Principio de la Navaja de Ockham).

---

## 3. Inducción Práctica en la Telemetría de energy-ml

Consideremos un conjunto de telemetría de transformadores en la subestación Tigre de ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md):

| ID Muestra | Temperatura Aceite (°C) | Carga Potencia (%) | Vibración RMS (mm/s) | Nivel Gas DGA (ppm) | Estado Operativo (Clase) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **M-01** | 88.5 | 115% | 4.8 | 150 | `DISPARO_CRITICO` (+) |
| **M-02** | 92.0 | 120% | 5.2 | 180 | `DISPARO_CRITICO` (+) |
| **M-03** | 65.0 | 75% | 1.8 | 35 | `NORMAL` (-) |
| **M-04** | 72.0 | 95% | 2.1 | 40 | `NORMAL` (-) |
| **M-05** | 86.0 | 90% | 4.6 | 145 | `DISPARO_CRITICO` (+) |
| **M-06** | 68.0 | 110% | 2.0 | 30 | `NORMAL` (-) |

### Iteración 1 del Algoritmo:
1. **Semilla:** Se elige `M-01` (`T=88.5, Carga=115%, Vib=4.8, DGA=150`).
2. **Discriminación contra negativos:**
   - Contra `M-03` (`T=65.0, Vib=1.8`): Selectores válidos `[T > 75.0]`, `[Vib > 3.0]`, `[DGA > 50]`.
   - Contra `M-04` (`T=72.0, Vib=2.1`): Selectores válidos `[T > 75.0]`, `[Vib > 3.0]`, `[DGA > 50]`.
   - Contra `M-06` (`T=68.0, Carga=110%, Vib=2.0`): Nótese que `Carga > 100%` no sirve aquí porque `M-06` también tiene 110%. Pero `[T > 75.0]` y `[Vib > 3.0]` sí discriminan.
3. **Mejor Regla Seleccionada (Regla R-1):**
   ```
   SI [temperatura_aceite > 75.0 °C] Y [vibracion_rms > 3.5 mm/s]
   ENTONCES estado = 'DISPARO_CRITICO'
   ```
4. **Evaluación de Cobertura:**
   - `R-1` cubre a `M-01`, `M-02` y `M-05`.
   - Como cubre el 100% de los positivos y ningún negativo, se remueven `M-01`, `M-02` y `M-05`.
5. **Fin de Cobertura:** No quedan positivos sin explicar. El proceso finaliza en una única regla óptima.

---

## 4. Comparación: Reglas Lógicas (AQ/CN2) vs. Árboles de Decisión (CART)

| Dimensión Técnica | Algoritmos de Cobertura (AQ, CN2, RIPPER) | Árboles de Decisión (CART, C4.5) |
| :--- | :--- | :--- |
| **Estrategia de Búsqueda** | *Separate-and-Conquer* (modular, regla por regla). | *Divide-and-Conquer* (jerarquía monolítica global). |
| **Formato de Salida** | Lista o conjunto plano de reglas independientes `IF-THEN`. | Grafo de árbol con ramas anidadas obligatorias. |
| **Problema de Replicación** | Inmune al problema de replicación de subárboles idénticos. | Frecuente duplicación de pruebas idénticas en ramas paralelas. |
| **Comprensión Humana** | Cada regla se lee y audita de forma aislada. | Requiere evaluar todo el camino desde la raíz hasta la hoja. |
| **Traducción Operativa** | Mapeo 1:1 a configuraciones de relés de protección y SCADA. | Requiere estructuras `if/elif/else` profundamente anidadas. |

En la siguiente lección extenderemos este razonamiento desde datos tabulares hacia la **Programación Lógica Inductiva (FOIL)** para aprender sobre grafos y topologías de red eléctrica.
