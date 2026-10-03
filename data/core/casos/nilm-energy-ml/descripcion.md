# NILM: Identificador de cargas energéticas

## Introducción al problema

**NILM (Non-Intrusive Load Monitoring)** es una técnica de inteligencia artificial que permite **identificar qué electrodomésticos están encendidos en una vivienda** analizando solo la **corriente total del tablero eléctrico**, sin instalar medidores independientes en cada aparato.

### ¿Por qué es importante?

- **Auditoría energética automática:** Detectar cuáles electrodomésticos consumen más energía.
- **Facturación inteligente:** En edificios multifamiliares, cobrar a cada inquilino según tipo de carga (diferenciando riego de climatización).
- **Automatización:** Apagar automáticamente cargas o alertar al usuario cuando detecta derroche.
- **Smart grids:** Estabilizar la red eléctrica prediciendo cambios de demanda.

### La analogía del cocinero

Así como un cocinero experimentado puede identificar ingredientes en un plato solo por el olfato, NILM identifica cargas observando patrones de consumo total sin "abrir" cada circuito.

---

## Proyectos y desafíos reales

### 1. Dataset: Mediciones reales en CSV

```csv
timestamp,voltage,current,power
2024-10-01 08:00:00,230.5,8.2,1886
2024-10-01 08:00:01,230.4,8.2,1885
2024-10-01 08:00:02,230.6,12.5,2880
2024-10-01 08:00:03,231.0,12.5,2887
```

**Desafío 1:** ¿Cómo pasar de columnas numéricas a identificación de cargas?  
→ Solución: Detectar *cambios* (eventos) en potencia.

### 2. Detección de eventos

Cuando el consumo salta de 1886W a 2880W, algo se activó (+994W).

```python
# Pseudocódigo: derivada de potencia
delta = potencia[t] - potencia[t-1]
if abs(delta) > umbral_deteccion:
    # Evento: activación/desactivación
```

**Desafío 2:** ¿Qué umbral elegir? ¿Fijo o adaptativo?  
→ Solución: Usar estadística (desviación estándar).

### 3. Clustering: Agrupar eventos similares

Eventos con Delta ≈ +994W probablemente son el mismo electrodoméstico (aire acondicionado). Eventos con Delta ≈ +100W podrían ser heladera.

**Algoritmo:** DBSCAN (Density-Based Spatial Clustering)

```python
from sklearn.cluster import DBSCAN

features = [
    [delta_potencia, duracion_evento, firma_armonica],
    # Fila 0: [+994W, 3600s, harmonicas_aire]
    # Fila 1: [+994W, 3610s, harmonicas_aire]  <- mismo cluster
    # Fila 2: [+100W,   30s, harmonicas_hela]  <- cluster distinto
]

clustering = DBSCAN(eps=50, min_samples=3).fit(features)
labels = clustering.labels_
# labels = [0, 0, 1, 1, 2, ...]
#          aire, aire, heladera, heladera, horno
```

**Desafío 3:** ¿Cómo garantizar que dos clusters son realmente cargas diferentes?  
→ Solución: Matriz de confusión contra etiquetas conocidas.

### 4. Evaluación: Matriz de confusión

Validar la precisión del clustering si tenemos un conjunto de mediciones etiquetadas manualmente:

```
              Aire  Heladera  Horno
Aire      [ 145,      3,        2]   → Precisión Aire: 145/150 = 96.7%
Heladera  [   2,    138,        5]   → Precisión Heladera: 138/145 = 95.2%
Horno     [   1,      4,      141]   → Precisión Horno: 141/146 = 96.6%

F1-Score (harmónico): 0.96
Recall (cobertura): 0.95
```

---

## Arquitectura: Capas limpias

### 1. Domain (Lógica pura)

```
src/domain/
├── carga.py          # Entidad: electrodoméstico
├── medicion.py       # Value Object: lectura puntual
├── evento.py         # Cambio de estado
└── clustering.py     # Política de agrupamiento (abstracta)
```

Cero dependencias externas: `@dataclass`, `@dataclass(frozen=True)`, tipado estándar.

### 2. Application (Casos de uso)

```
src/application/
├── cargas/
│   ├── identify_cargas_use_case.py  # Orquestador principal
│   ├── metricas.py                  # Cálculo F1, precisión
│   └── mappers/
│       └── carga_mapper.py           # Domain ↔ DTO
└── dtos/
    ├── identify_request.py
    └── identify_response.py
```

DTOs con **Pydantic** para validación y serialización.

### 3. Infrastructure (Frameworks, librerías)

```
src/infrastructure/
├── fastapi/
│   ├── app.py        # Inicialización Uvicorn
│   ├── lifespan.py   # Cargar modelo en memoria
│   └── routes.py     # Endpoints REST
├── sklearn/
│   └── clustering.py # Pipeline DBSCAN, normalización
├── repositories/
│   └── medicion_repository.py  # Lectura CSV
└── persistencia/
    └── model_storage.py  # Guardar/cargar con joblib
```

### 4. Adapters (Presenters agnósticos)

```
src/adapters/
├── cargas_presenter.py     # Domain → JSON
├── tree_presenter.py       # Serializar árbol de decisión
└── metrics_presenter.py    # Formatear métricas
```

---

## Mapeo: Lecciones → Código

| Lección | Concepto | Ubicación |
|---------|----------|-----------|
| 1.1 Terminal Bash | Navegación, archivos | `data/raw/` contiene CSVs |
| 1.2 venv | Aislamiento | `Makefile` con targets de instalación |
| 1.3 .env | Secretos | `.env.example` (rutas, thresholds) |
| 2.1 Git diff | Auditoría | Historial de entrenamientos en commits |
| 4.2 FastAPI | Servidor básico | `POST /api/v1/identify-loads` |
| 5.1 Matriz confusión | Evaluación | `src/application/cargas/metricas.py` |
| 5.2 pytest + TDD | Pruebas | `tests/application/cargas/test_identify_use_case.py` |
| 5.3 /metrics | Observabilidad | `GET /api/v1/metrics` retorna F1, recall |
| 3.1 Entropía/Gini | Decisiones | DBSCAN usa densidad (forma de Gini) |
| 3.2 Árboles regresión | CART, poda | `src/infrastructure/sklearn/arbol_decision.py` (futuro) |

---

## Flujo de trabajo con agentes

### Escenario: Agregar soporte para lámparas LED inteligentes

```bash
# 1. Descripción del cambio
$ aider --message "Agregar detección de lámparas LED"

# 2. Aider actualiza atómicamente:
#    ✅ src/domain/carga.py (nueva entidad Lampara)
#    ✅ src/application/cargas/ (lógica de clustering)
#    ✅ src/infrastructure/fastapi/routes.py (endpoint)
#    ✅ tests/ (cobertura pytest)

# 3. Pre-push valida (hook git)
$ pytest --cov=src --cov-fail-under=85 tests/
$ pyright src/ infrastructure/

# 4. Deploy automático por GitHub Actions
# (usa VPS datamaq sin intervención manual)

# 5. Cliente llama el endpoint
$ curl -X POST https://energy-ml.api/identify-loads \
  -F "file=@mediciones.csv" \
  | jq '.cargas[].nombre'
# aire_acondicionado
# heladera
# lampara_led
```

---

## Expectativas de aprendizaje

Al completar este caso, los estudiantes sabrán:

1. **Separación de capas:** Cómo mantener domain puro sin Pydantic, FastAPI o sklearn.
2. **DTOs:** Validar y serializar datos con Pydantic.
3. **APIs REST:** Servir modelos ML en endpoints con Swagger/OpenAPI.
4. **Clustering:** Agrupar datos sin etiquetas usando DBSCAN.
5. **Evaluación:** Medir precisión con matriz de confusión y F1-Score.
6. **Tipado estricto:** Pyright y type hints en Python.
7. **TDD:** Cobertura de pruebas >= 85% con pytest.
8. **Agentes auditores:** Cómo agentes pueden leer la decisión del árbol exportada en JSON.

---

## Referencias

- **Repositorio:** https://github.com/datamaq-automation/energy-ml
- **Documentación:** https://github.com/datamaq-automation/energy-ml/blob/main/README.md
- **Datos de prueba:** https://github.com/datamaq-automation/energy-ml/tree/main/data/raw
- **Cuaderno de alumno:** https://github.com/datamaq-automation/energy-ml/blob/main/docs/cuaderno-alumno.md
- **Especificaciones técnicas:** https://github.com/datamaq-automation/energy-ml/blob/main/docs/specs.md

---

## Notas finales

**Bidireccionaldad:** El curso referencia energy-ml EN el contenido, y energy-ml referencia el curso en su README.  
**No inventar datos:** Todo dato de contenido vive en `data/`, nunca hardcodeado en Python.  
**Agentes de auditoría:** Los LLMs pueden leer el árbol de decisión exportado para explicar *por qué* se identificó una carga.
