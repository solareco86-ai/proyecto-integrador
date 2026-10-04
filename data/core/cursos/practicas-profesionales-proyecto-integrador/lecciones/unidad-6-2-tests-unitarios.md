# 6.2 Tests Unitarios e Integración: pytest con Cobertura >= 85%

## Objetivo

Escribir tests que verifiquen que código funciona correctamente. NO es buscar errores; es **garantizar comportamiento esperado**. Meta: >= 85% cobertura de código.

## Referencia

**spec § 5.5:** "Suite Completa de Pruebas en Pytest (Unit, Integration, E2E)"

**Plan Oficial:** § Verificación de Cobertura (>= 85%)

## Contenidos

### 1. Tests Unitarios vs Integración (Repaso Unidad 5B)

**Test Unitario:** Función aislada, dependencias mockeadas.
```python
def test_is_anomaly_with_high_consumption():
    """Verifica que Reading detecta consumo alto como anomalía"""
    reading = Reading(timestamp=now(), power_kw=60)
    avg_kw = 50
    
    assert reading.is_anomaly(avg_kw) == True  # 60 > 50*1.2
```

**Test Integración:** Componentes reales conectados (no mocks).
```python
def test_ocr_nlp_integration_extracts_and_understands():
    """Verifica que OCR output puede ser procesado por NLP"""
    image = load_image("test_data/invoice.png")
    
    # Execute: OCR real
    text = ocr.extract_text(image)
    
    # Verify: NLP puede procesar
    intent = nlp.understand(text)
    assert intent is not None
```

En Unidad 6, combinamos ambos.

### 2. Estructura de Tests en pytest

```
tests/
├── conftest.py                 # Fixtures compartidas
├── unit/
│   ├── test_domain_entities.py
│   ├── test_application_services.py
│   └── test_value_objects.py
├── integration/
│   ├── test_ocr_nlp_flow.py
│   ├── test_api_database.py
│   └── test_email_notification.py
└── e2e/
    └── test_full_workflow.py
```

### 3. Escritura de Tests Unitarios

**Template:**
```python
# tests/unit/test_reading_service.py

import pytest
from src.domain.entities import Reading
from src.application.services import ReadingService

class TestReadingService:
    """Tests de ReadingService"""
    
    def test_get_reading_by_id_returns_correct_reading(self):
        """Verifica que obtener por ID retorna lectura correcta"""
        # Arrange: Setup
        service = ReadingService()
        expected_id = 123
        
        # Act: Execute
        reading = service.get_reading(expected_id)
        
        # Assert: Verify
        assert reading.id == expected_id
        assert isinstance(reading, Reading)
    
    def test_create_reading_with_invalid_power_raises_error(self):
        """Verifica que potencia negativa levanta excepción"""
        service = ReadingService()
        
        with pytest.raises(ValueError):
            service.create_reading(power_kw=-10)
    
    def test_is_anomaly_detection(self):
        """Verifica lógica de anomalía"""
        reading = Reading(timestamp=now(), power_kw=60)
        
        assert reading.is_anomaly(avg_kw=50) == True
        assert reading.is_anomaly(avg_kw=70) == False
```

**Patrones:**
- **Arrange-Act-Assert:** Setup → Execute → Verify
- **Nombres descriptivos:** `test_<función>_<condición>_<resultado>`
- **Doctring:** Explica qué verifica
- **Fixtures:** Para datos comunes (próximo)

### 4. Fixtures (Datos Reutilizables)

En `conftest.py` (cargado automáticamente):

```python
# tests/conftest.py

import pytest
from datetime import datetime
from src.domain.entities import Reading

@pytest.fixture
def sample_reading():
    """Crea una Reading de prueba"""
    return Reading(
        timestamp=datetime(2026, 10, 4, 18, 0),
        power_kw=50.0
    )

@pytest.fixture
def mock_database(mocker):
    """Mock de base de datos"""
    mock_db = mocker.MagicMock()
    mock_db.save.return_value = True
    return mock_db

# Uso en tests:
def test_with_fixture(sample_reading):
    assert sample_reading.power_kw == 50.0

def test_with_mock(mock_database):
    result = mock_database.save()
    assert result == True
```

### 5. Mocking para Aislar Componentes

```python
# tests/unit/test_reading_service.py

from unittest.mock import MagicMock, patch
import pytest

class TestReadingServiceWithMocks:
    def test_save_reading_calls_database_save(self, mocker):
        """Verifica que save() llama a base de datos"""
        # Arrange: Mock de DB
        mock_db = MagicMock()
        mock_db.save.return_value = True
        
        service = ReadingService(db=mock_db)
        reading = Reading(timestamp=now(), power_kw=60)
        
        # Act
        service.save(reading)
        
        # Assert
        mock_db.save.assert_called_once_with(reading)
```

**Regla:** Mock = dependencia externa. NO mockees lógica propia.

### 6. Tests de Integración (sin Mocks)

```python
# tests/integration/test_ocr_nlp_integration.py

import pytest
from src.infrastructure.ocr import OCREngine
from src.infrastructure.nlp import NLPEngine
from pathlib import Path

class TestOCRNLPIntegration:
    def test_ocr_output_can_be_processed_by_nlp(self):
        """Integración: OCR → NLP funciona sin errores"""
        # Setup real
        ocr = OCREngine()
        nlp = NLPEngine()
        
        # Load image real (no mock)
        image_path = Path("test_data/invoice.png")
        assert image_path.exists()
        
        # Execute: OCR real
        extracted_text = ocr.extract(image_path)
        assert len(extracted_text) > 0
        
        # Execute: NLP real procesa output de OCR
        intent = nlp.understand(extracted_text)
        
        # Verify
        assert intent is not None
        assert intent.type in ["measurement", "query", "unknown"]
```

### 7. Cobertura de Código (>= 85%)

**Ejecutar con coverage:**
```bash
pytest --cov=src --cov-report=html --cov-fail-under=85
```

**Archivo generado:** `htmlcov/index.html` (abre en navegador).

**¿Qué cuenta como "cubierto"?**
```python
def calculate_fee(amount):
    if amount < 0:        # ← Línea 1
        raise ValueError  # ← Línea 2
    return amount * 0.1   # ← Línea 3

# Test 1: cantidad normal
assert calculate_fee(100) == 10.0  # Cubre línea 3

# Test 2: cantidad negativa
with pytest.raises(ValueError):
    calculate_fee(-10)  # Cubre líneas 1-2

# Cobertura: 3/3 líneas = 100%
```

**¿Qué NO contar?**
- Líneas no alcanzables (dead code)
- `pass` en except
- Código de test mismo

### 8. Estructura de Cobertura por Capa

**Domain (100% esperado):**
- Lógica pura, sin dependencias
- Fácil de testear completamente

**Application (>= 85%):**
- Servicios, DTOs, mappers
- Algunos paths pueden requerir integración

**Infrastructure (>= 70% OK):**
- FastAPI routes, configuración
- Difícil testear completamente sin integración

### 9. Ejemplo: Energy-ML

**Test unitario (domain):**
```python
def test_reading_is_anomaly():
    """Reading.is_anomaly() detects anomalies correctly"""
    reading = Reading(timestamp=now(), power_kw=60)
    
    assert reading.is_anomaly(avg_kw=50) == True   # 60 > 50*1.2
    assert reading.is_anomaly(avg_kw=70) == False  # 60 < 70*1.2
```

**Test integración (application + infrastructure):**
```python
def test_mqtt_to_anomaly_detection_flow():
    """Full flow: MQTT → normalization → anomaly detection"""
    # Real MQTT data
    mqtt_message = {
        "timestamp": "2026-10-04T18:00:00",
        "power_kw": 52.3
    }
    
    # Real pipeline
    validated = validate(mqtt_message)
    normalized = normalize(validated)
    prediction = ml_model.predict(normalized)
    is_anomaly = prediction.predicted_kw > normalized.percent_of_average * 1.2
    
    # Verify
    assert isinstance(normalized, MedidaNormalizada)
    assert isinstance(is_anomaly, bool)
```

### 10. CI/CD Integration

En `.github/workflows/test.yml`:
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: pip install -r requirements-dev.txt
      - run: pytest --cov=src --cov-fail-under=85
      - run: coverage report
```

Si cubre < 85%, PR falla.

## Actividad Práctica

1. **Escribir tests para funcionalidades de Sprint 1-2 (Semana 14):**
   ```bash
   pytest tests/unit/ -v
   pytest tests/integration/ -v
   pytest --cov=src --cov-report=html
   
   # Abrir htmlcov/index.html para ver gaps
   ```

2. **Documentar cobertura en `COVERAGE_REPORT.md`:**
   ```markdown
   # Coverage Report - Semana 14
   
   ## Por Capa
   - domain: 100% (20 funciones, 20 testeadas)
   - application: 87% (45 funciones, 39 testeadas)
   - adapters: 75% (20 funciones, 15 testeadas)
   - infrastructure: 60% (30 funciones, 18 testeadas)
   
   **Promedio: 86% ✅**
   
   ## Gaps (< 80%)
   - infrastructure/fastapi/routes.py: 60%
     - Falta: GET /health, POST /admin
   
   ## Plan para Semana 15
   - Agregar tests para routes faltantes (2-3 horas)
   - Target: 88%
   ```

3. **Integrar en pre-push:**
   ```bash
   # .git/hooks/pre-push
   pytest --cov=src --cov-fail-under=85 || exit 1
   ```

## Palabras clave

Unit Tests, Integration Tests, Mocking, Fixtures, Coverage, pytest, Arrange-Act-Assert, Code Quality

## Referencias

- spec § 5.5 (Suite completa)
- pytest documentation: https://docs.pytest.org/
- Coverage.py: https://coverage.readthedocs.io/
- Plan Oficial § Verificación de Cobertura
