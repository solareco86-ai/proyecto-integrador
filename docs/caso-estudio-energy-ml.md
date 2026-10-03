# Caso de Estudio: energy-ml — NILM (Identificación No Intrusiva de Cargas)

**Repositorio:** https://github.com/datamaq-automation/energy-ml  
**Curso asociado:** [Procesamiento de Aprendizaje Automático](https://isftn199.com.ar/cursos/procesamiento-aprendizaje-automatico)

---

## ¿Qué es NILM (Non-Intrusive Load Monitoring)?

**NILM** es una técnica de inteligencia artificial que permite **identificar qué electrodomésticos están encendidos en una vivienda** midiendo solamente la **corriente total del tablero eléctrico**, sin necesidad de instalar medidores independientes en cada aparato.

### Analogía: Como descifrar una receta por el aroma

Así como un cocinero experimentado puede identificar ingredientes en un plato solo por el olfato, NILM identifica cargas (aires, heladeras, hornos, etc.) observando el patrón de consumo total de energía, sin "abrir" cada circuito.

### Aplicaciones reales

- **Auditoría energética:** Detectar consumo anómalo o derrochador.
- **Facturación discriminatoria:** Tarificar según tipo de carga (distinguir riego vs. climatización).
- **Automatización del hogar:** Apagar automáticamente cargas cuando no se usan.
- **Smart grids:** Estabilizar la red eléctrica prediciendo cambios de demanda.

---

## Cómo energy-ml implementa los conceptos del curso

### Estructura del repositorio

```
energy-ml/
├── src/
│   ├── domain/              # Entidades (Medición, Carga, Evento)
│   ├── application/         # Casos de uso (IdentificarCargasUseCase)
│   │   └── cargas/
│   ├── infrastructure/
│   │   ├── fastapi/         # Endpoints REST
│   │   ├── sklearn/         # Pipelines de ML
│   │   └── repositorios/    # Persistencia
│   └── adapters/            # Presenters
├── data/
│   ├── raw/                 # CSVs de mediciones
│   └── processed/           # Features normalizadas
├── tests/                   # Suite pytest con cobertura >= 85%
└── docs/
    └── cuaderno-alumno.md   # Notebook conceptual
```

### Capas de la arquitectura

**1. Domain (Lógica pura, sin dependencias externas)**
- `Medicion`: registro puntual de voltaje y corriente
- `Carga`: entidad que representa un electrodoméstico (aire, heladera, etc.)
- `Evento`: cambio de estado que ocurre cuando una carga se activa/desactiva

```python
# Ejemplo: src/domain/carga.py
@dataclass
class Carga:
    id: str
    nombre: str  # "aire acondicionado", "heladera"
    potencia_nominal: float  # watts
    firma_espectral: dict[str, float]  # características eléctricas
```

**2. Application (Casos de uso + DTOs con Pydantic)**
- `IdentificarCargasUseCase`: orquesta lectura, detección, clustering y evaluación
- DTOs de validación: esquemas Pydantic para entrada/salida

```python
# Ejemplo: src/application/cargas/IdentificarCargasUseCase.py
class IdentificarCargasUseCase:
    def ejecutar(self, ruta_csv: str) -> IdentificacionResultado:
        # 1. Leer mediciones
        # 2. Detectar eventos
        # 3. Clustering (DBSCAN)
        # 4. Evaluar (matriz de confusión)
        # 5. Retornar resultado
```

**3. Infrastructure (FastAPI, sklearn, persistencia)**
- Endpoints REST: `POST /api/v1/identify-loads`, `GET /api/v1/metrics`
- Pipelines sklearn: DBSCAN, StandardScaler, normalización
- Repositorios: lectura de CSVs, serialización con joblib

```python
# Ejemplo: src/infrastructure/fastapi/routes.py
@app.post("/api/v1/identify-loads")
async def identify_loads(request: IdentificacionRequest) -> IdentificacionResponse:
    resultado = use_case.ejecutar(request.archivo_csv)
    return IdentificacionResponse.from_domain(resultado)
```

**4. Adapters (Presenters agnósticos)**
- Convierte objetos de dominio a DTOs para serializar JSON
- Desvincula la API REST de la lógica de negocio

---

## Flujo completo: Lectura CSV → Clustering → Evaluación

### Paso 1: Lectura de datos (Cap 1.1 - Terminal y entorno)
```bash
# El archivo CSV contiene columnas: timestamp, voltage, current, power
# Ejemplo:
# 2024-10-01 08:00:00,230.5,8.2,1886
# 2024-10-01 08:00:01,230.4,8.2,1885
# 2024-10-01 08:00:02,230.6,12.5,2880  <-- cambio de carga
```

**Concepto:** datos desacoplados en archivos estáticos (principio de AGENTS.md).

### Paso 2: Detección de eventos (Cap 3.1 - Entropía y Gini)
energy-ml **detecta cambios** en el consumo calculando la derivada de potencia:

```python
# Pseudocódigo
delta_potencia = potencia[t] - potencia[t-1]
if abs(delta_potencia) > umbral:
    # Evento detectado (carga se activó/desactivó)
    evento = Evento(timestamp, delta_potencia, tipo="activacion_o_desactivacion")
```

**Mapeo curricular:**
- Concepto: decisiones basadas en datos (Cap 4.4)
- No más if/else fijo: el umbral se calibra estadísticamente

### Paso 3: Clustering con DBSCAN (Cap 3.1-3.3)
energy-ml agrupa eventos similares usando **DBSCAN** (Density-Based Spatial Clustering):

```python
from sklearn.cluster import DBSCAN

# Features: [cambio_potencia, duración_evento, firma_armónica]
eventos_normalizados = StandardScaler().fit_transform(eventos)

clustering = DBSCAN(eps=0.5, min_samples=2).fit(eventos_normalizados)
etiquetas = clustering.labels_  # Cada etiqueta es una carga identificada

# etiquetas = [0, 0, 0, 1, 1, 2, ...]
#             aire  aire  aire heladera heladera horno
```

**Mapeo curricular:**
- Árboles de decisión (Cap 3.1): Las fronteras de separación entre clusters son regiones de decisión
- Ganancia de Gini: Cada cluster maximiza homogeneidad interna (baja impureza)

### Paso 4: Evaluación con matriz de confusión (Cap 5.1)
energy-ml valida la precisión del clustering comparando contra etiquetas conocidas:

```python
from sklearn.metrics import confusion_matrix, f1_score

# etiquetas_reales = [0, 0, 0, 1, 1, 2, ...]  # Sabe que eventos 0-2 son aire
# etiquetas_pred    = [0, 0, 0, 1, 1, 2, ...]  # Lo que predijo

matriz = confusion_matrix(etiquetas_reales, etiquetas_pred)
f1 = f1_score(etiquetas_reales, etiquetas_pred, average="weighted")

print(f"Precisión F1: {f1:.2%}")
```

**Salida esperada:**
```
Matriz de confusión:
             Aire  Heladera  Horno
Aire         [145,      3,       2]
Heladera     [  2,    138,       5]
Horno        [  1,      4,     141]

Precisión    Recall      F1-Score
Aire   0.97   0.95       0.96
Heladera 0.96  0.94       0.95
Horno  0.93   0.93       0.93
```

---

## Mapa: Dónde mirar el código para cada lección

| Lección del Curso | Concepto | Archivo en energy-ml |
|---|---|---|
| **1.1 Terminal Bash** | Navegación, archivos | `data/raw/` (CSVs de entrada) |
| **1.2 venv** | Aislamiento de dependencias | `requirements.txt`, `Makefile` |
| **1.3 .env** | Variables de entorno | `.env.example` (API keys, rutas de datos) |
| **2.1 Git diff** | Auditoría de cambios | `git log --oneline` (historial de modelos) |
| **2.2 Comandos Git** | Control de versiones | Rama `main` con MLP trainado estable |
| **3.1 FastAPI básico** | Servidor HTTP mínimo | `src/infrastructure/fastapi/app.py` |
| **4.2 FastAPI + Swagger** | Documentación auto | `src/infrastructure/fastapi/routes.py` |
| **5.1 Matriz de confusión** | Evaluación F1 | `src/application/cargas/metricas.py` |
| **5.2 pytest + TDD** | Pruebas unitarias | `tests/application/cargas/test_identify_use_case.py` |
| **5.3 /metrics endpoint** | Observabilidad | `GET /api/v1/metrics` devuelve F1, precision, recall |
| **3.1 Entropía/Gini** | Decisiones por datos | `src/infrastructure/sklearn/clustering.py` (DBSCAN) |
| **3.2 Árboles regresión** | CART, poda | `src/infrastructure/sklearn/arbol_decision.py` (futuro) |
| **3.3 JSON export** | Trazabilidad agentes | `src/adapters/tree_presenter.py` (serializar árbol) |
| **4.2 MCP** | Servidor Context Protocol | `src/infrastructure/mcp/` (futuro: exponer reglas lógicas) |

---

## Flujo de trabajo con agentes (Unidad 3, Cap 4)

### Scenario: "Agregar nueva carga (lámpara LED)"

```bash
# 1. Usuario proporciona datos de entrenamiento
$ aider -m "Agregar support para detección de lámparas LED"

# 2. Aider/OpenCode actualiza:
#    - domain/carga.py (nueva entidad Lampara)
#    - application/.../identify_use_case.py (lógica)
#    - tests/...test_lampara.py (cobertura)
#    - infrastructure/.../routes.py (nuevo endpoint)

# 3. Pre-push valida:
pytest --cov=src --cov-fail-under=85 tests/
pyright src/

# 4. Deploy automático a VPS por GitHub Actions

# 5. Agentes pueden auditar el árbol de decisión exportado en JSON
$ curl https://energy-ml.com/api/v1/tree/decision-rules | jq .
{
  "rule_0": "if delta_potencia > 50W and duración > 0.5s then LAMPARA",
  "confidence": 0.94
}
```

---

## Recursos

- **README energy-ml:** https://github.com/datamaq-automation/energy-ml#readme
- **Cuaderno de alumno:** https://github.com/datamaq-automation/energy-ml/blob/main/docs/cuaderno-alumno.md
- **Datos de prueba:** https://github.com/datamaq-automation/energy-ml/tree/main/data/raw
- **Especificación técnica:** https://github.com/datamaq-automation/energy-ml/blob/main/docs/specs.md

---

## Notas para docentes y estudiantes

1. **Desacoplamiento:** Así como energy-ml mantiene datos en archivos (no en código), el proyecto-integrador también cumple este principio.
2. **Bidireccionaldad:** El curso referencia energy-ml Y energy-ml referencia lecciones del curso en su README.
3. **Verborragia prohibida:** No inventar cargas, métricas ni datos en el código; todo está en `data/`.
4. **Agentes como auditores:** Los agentes deben poder leer el árbol de decisión exportado en JSON para explicar *por qué* se identificó una carga.
