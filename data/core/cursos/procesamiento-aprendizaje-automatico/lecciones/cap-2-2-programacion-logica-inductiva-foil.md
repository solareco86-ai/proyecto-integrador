# Lección 2.2: Programación Lógica Inductiva (FOIL): Aprendizaje de Relaciones de Primer Orden en Redes Eléctricas

En las lecciones anteriores trabajamos con representaciones **atributivas** (vectores de características o tablas de datos planas). Si bien una tabla es apta para describir el estado termomecánico puntual de un transformador individual, fracasa rotundamente al intentar modelar sistemas interconectados en red, tales como la infraestructura de transporte y distribución eléctrica en ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md).

Una red eléctrica real es un **grafo dinámico** de generadores, barras, transformadores, alimentadores y centros de carga. El fenómeno de mayor gravedad operativa —el **apagón en cascada** o colapso por contingencia $N-1$— no depende de un único sensor aislado, sino de relaciones de topología y adyacencia.

En esta lección abordamos la **Programación Lógica Inductiva (ILP)** y el algoritmo **FOIL** (*First-Order Inductive Learner*), diseñado para inducir conocimiento expresado en **lógica de predicados de primer orden** (cláusulas de Horn).

---

## 1. De Tablas Planas a Lógica de Predicados

El aprendizaje supervisado convencional asume que cada fila es independiente e idénticamente distribuida (i.i.d.). En contraste, la lógica relacional describe el mundo mediante **hechos**, **relaciones** y **reglas universales**:

```
                       Base de Conocimiento Relacional
                       
  Hechos de Topología:
    subestacion("tigre_norte", "transmision").
    subestacion("pacheco_centro", "distribucion").
    linea_enlace("L-101", "tigre_norte", "pacheco_centro", 45.0).
    
  Hechos de Telemetría Dinámica:
    sobrecargado("L-101").
    disparo_proteccion("L-101").
```

Si intentáramos aplanar esta topología en una tabla convencional, sufriríamos explosión combinatoria de columnas o pérdida irreversible del contexto relacional.

---

## 2. El Algoritmo FOIL: Inducción de Cláusulas de Horn

Desarrollado por Ross Quinlan (autor también de ID3 y C4.5), **FOIL** combina la estrategia de cobertura secuencial (*Separate-and-Conquer*) con la búsqueda guiada por ganancia de información relacional.

### Estructura de una Cláusula de Horn
Una cláusula inducida por FOIL tiene la estructura:
```
Cabeza :- Literal_1, Literal_2, ..., Literal_k.
```
Donde el operador `:-` se lee como *"SI es verdad que..."*. Por ejemplo:
```
falla_cascada(NodoOrigen, NodoDestino) :- 
    linea_enlace(Linea, NodoOrigen, NodoDestino, Capacidad),
    sobrecargado(Linea),
    temperatura_critica(NodoOrigen).
```

### Dinámica de Inducción de FOIL:
1. Comienza con una regla con cuerpo vacío: `falla_cascada(X, Y) :- verdadero.`
2. Evalúa todos los predicados candidatos que introduzcan variables existentes o nuevas.
3. Calcula la **Ganancia de Información FOIL** de cada literal candidato:
   ```
   Ganancia = T_pos * ( log2( p1 / (p1 + n1) ) - log2( p0 / (p0 + n0) ) )
   ```
   Donde:
   - `p0`, `n0`: Cantidad de tuplas positivas y negativas cubiertas antes de agregar el literal.
   - `p1`, `n1`: Cantidad de tuplas positivas y negativas cubiertas después de agregar el literal.
   - `T_pos`: Cantidad de tuplas positivas originales que continúan cubiertas por el nuevo cuerpo ampliado.
4. Selecciona el literal que maximice la ganancia y especialice la regla para excluir tuplas negativas.
5. Continúa agregando literales hasta que la regla no cubra ninguna tupla negativa.
6. Separa las tuplas positivas cubiertas y repite el proceso para aprender nuevas reglas disyuntivas.

---

## 3. Inducción de Fallas en Cascada en energy-ml

Imaginemos que en `energy-ml` registramos los siguientes eventos históricos de contingencia en Zona Norte:

### Hechos de Fondo (*Background Knowledge*):
- `alimenta("benavidez", "barrio_las_palmas")`
- `alimenta("pacheco", "parque_industrial")`
- `linea_transmision("L-201", "tigre", "benavidez", 30.0)`
- `linea_transmision("L-202", "tigre", "pacheco", 40.0)`
- `interconexion("benavidez", "pacheco")`

### Ejemplos Positivos de Falla en Cascada:
- `falla_cascada("tigre", "benavidez") -> Positivo`
- `falla_cascada("tigre", "pacheco") -> Positivo`

### Ejemplos Negativos (Operación Segura):
- `falla_cascada("benavidez", "parque_industrial") -> Negativo`
- `falla_cascada("pacheco", "barrio_las_palmas") -> Negativo`

FOIL analiza los hechos de fondo e induce inductivamente la regla relacional:
```prolog
falla_cascada(SubestacionA, SubestacionB) :-
    linea_transmision(L, SubestacionA, SubestacionB, Capacidad),
    flujo_potencia(L, FlujoActual),
    mayor(FlujoActual, Capacidad).
```

Esta regla universal es independiente de nombres específicos de subestaciones: se aplica a cualquier nuevo nodo que se incorpore a la red eléctrica en el futuro.

---

## 4. FOIL y el Razonamiento de Agentes Autónomos de IA

¿Por qué un ingeniero de software y estudiante de Inteligencia Artificial debe comprender FOIL?

Porque las herramientas avanzadas de asistencia agéntica (como **AGY CLI**, **OpenCode** y **Aider**) **no operan como clasificadores tabulares**. Para entender un proyecto como `energy-ml`, los agentes construyen representaciones relacionales sobre el código:

```
  relaciones_codigo:
    modulo("src.infrastructure.fastapi.main").
    endpoint("POST /api/v1/predict/consumo").
    depende_de("main", "predictor_service").
    invoca("predictor_service", "joblib.load").
    falta_manejo_excepcion("joblib.load", "FileNotFoundError").
```

Cuando un agente autónomo infiere:
> *"Si un endpoint invoca un modelo serializado con `joblib.load` y no captura `FileNotFoundError`, existe un riesgo de caída del servidor (HTTP 500)"*

El agente está ejecutando una inferencia lógica sobre cláusulas de Horn análogas a las inducidas por FOIL.

---

## 5. Resumen de la Lección

1. **Expresividad Superior:** La lógica de predicados de primer orden permite modelar relaciones estructurales y topológicas que las tablas planas no pueden capturar.
2. **Generalización Relacional:** FOIL induce reglas con variables libres aplicables universalmente a cualquier grafo de red.
3. **Fundamento Neuro-Simbólico:** Comprender cláusulas de Horn y razonamiento relacional es el puente directo entre el Machine Learning tradicional y los agentes de software modernos.

En la próxima lección expondremos estas reglas operativas a través de un servicio de auditoría en FastAPI (`GET /api/v1/rules`).
---

## Autoevaluación Formativa y Caza de Código Alucinado

### Preguntas de Razonamiento Conceptual
1. ¿Por qué FOIL es especialmente útil para descubrir relaciones de primer orden que k-NN o árboles de decisión no pueden capturar?
2. ¿Qué síntoma de alucinación de IA verías si un algoritmo FOIL no ordena las variables por ganancia de información?

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente código generado por un asistente de IA:

```python
# CÓDIGO CON BUG DE ALGORITMO GENERADO POR IA:
def foil_step(ejemplos_positivos, ejemplos_negativos):
    # IA generó esto sin minimizar falsos positivos
    mejor_literal = None
    for literal in generar_literales():
        coberturas_pos = contar(ejemplos_positivos, literal)
        # ¡Falta considerar los falsos positivos (negativos cubiertos)!
        if coberturas_pos > mejor_literal[1]:
            mejor_literal = (literal, coberturas_pos)
    return mejor_literal
```

**Diagnóstico del Revisor Humano:**
1. **Sin Ganancia de Información:** Solo cuenta positivos, ignora negativos cubiertos.
2. **Riesgo de Overfitting:** La regla puede ser demasiado específica.
3. **Corrección Obligatoria en energy-ml:**
   ```python
   import math

   def foil_step(ejemplos_positivos, ejemplos_negativos):
       mejor_literal = None
       mejor_ganancia = -float('inf')

       for literal in generar_literales():
           pos_cubiertos = contar(ejemplos_positivos, literal)
           neg_cubiertos = contar(ejemplos_negativos, literal)

           if pos_cubiertos > 0 and neg_cubiertos > 0:
               ganancia = pos_cubiertos * (math.log2(pos_cubiertos / (pos_cubiertos + neg_cubiertos)) -
                                           math.log2(len(ejemplos_positivos) / (len(ejemplos_positivos) + len(ejemplos_negativos))))
               if ganancia > mejor_ganancia:
                   mejor_literal = (literal, pos_cubiertos, neg_cubiertos)
                   mejor_ganancia = ganancia

       return mejor_literal
   ```

---
