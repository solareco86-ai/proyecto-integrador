# 7.2 README Ejecutable y Docstrings de Código

## Objetivo

Documentar **cómo usar y modificar** el proyecto. README es la puerta de entrada. Docstrings son la puerta de entrada al código.

## Referencia

**spec § 5.4:** Documentación de Código

**Plan Oficial:** Documentación aportada

## Contenidos

### 1. README.md (Ejecutable, No Aspiracional)

**Estructura:**

```markdown
# Proyecto Integrador: Energy-ML

One-liner descripción.

## Descripción Rápida

Qué es, por qué existe, quién lo usa.

## Instalación

```bash
git clone https://github.com/isft199/energy-ml.git
cd energy-ml
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configuración

```bash
cp .env.example .env
# Editar .env con credenciales locales
```

## Ejecución

```bash
# Desarrollo local
uvicorn src.infrastructure.fastapi.main:app --reload

# Tests
pytest --cov=src

# Validación completa (pre-push)
python3 tests/test_architecture.py
pytest --cov=src --cov-fail-under=85
```

## Arquitectura

```
src/
├── domain/       # Entidades, lógica pura
├── application/  # Servicios, DTOs
├── adapters/     # Presenters
└── infrastructure/  # FastAPI, DB
```

## API Endpoints

```
GET  /health          - Status del sistema
GET  /api/readings    - Obtener todas las lecturas
GET  /api/readings/:id - Obtener lectura por ID
POST /api/readings    - Crear lectura nueva
```

## Troubleshooting

### ¿Sensores MQTT no conectan?
```bash
# Verificar broker está corriendo
mosquitto -v

# Publicar mensaje de test
mosquitto_pub -h localhost -t "test" -m "hello"

# Verificar logs
tail -f .logs/mqtt.log
```

### ¿Tests fallan?
```bash
# Verificar DB está corriendo
psql postgresql://localhost/energy_ml_test

# Reset DB
python3 scripts/reset_db.py

# Rerun tests
pytest -vv
```

## Contribuir

Pull requests bienvenidas. Ver CONTRIBUTING.md

## Licencia

MIT

## Contacto

- Email: isft199@abc.gob.ar
- Issues: GitHub Issues
```

### 2. Docstrings de Código (Exhaustivos)

**Formato Google / NumPy:**

```python
# src/domain/entities/reading.py
"""
src/domain/entities/reading.py

Entidades del dominio para lecturas de consumo eléctrico.
"""

from dataclasses import dataclass
from datetime import datetime

@dataclass
class Reading:
    """
    Lectura de consumo eléctrico en un momento.
    
    Attributes:
        timestamp (datetime): Momento de la lectura (UTC).
        power_kw (float): Consumo en kilovatios.
    
    Examples:
        >>> reading = Reading(
        ...     timestamp=datetime(2026, 10, 4, 18, 0),
        ...     power_kw=52.3
        ... )
        >>> reading.is_anomaly(avg_kw=50)
        True
    """
    timestamp: datetime
    power_kw: float
    
    def is_anomaly(self, avg_kw: float, threshold: float = 1.2) -> bool:
        """
        Detecta si lectura es anómala vs promedio.
        
        Args:
            avg_kw: Consumo promedio histórico en kW.
            threshold: Multiplicador para considerar anomalía (default 1.2 = 20%).
        
        Returns:
            bool: True si power_kw > avg_kw * threshold.
        
        Raises:
            ValueError: Si avg_kw < 0 o threshold < 1.
        
        Examples:
            >>> reading = Reading(timestamp=now(), power_kw=60)
            >>> reading.is_anomaly(avg_kw=50)  # 60 > 50*1.2
            True
            >>> reading.is_anomaly(avg_kw=70)  # 60 < 70*1.2
            False
        """
        if avg_kw < 0:
            raise ValueError("avg_kw debe ser >= 0")
        if threshold < 1:
            raise ValueError("threshold debe ser >= 1")
        
        return self.power_kw > avg_kw * threshold
```

**Formato para Servicios:**

```python
# src/application/services/reading_service.py
"""
src/application/services/reading_service.py

Servicio de aplicación para gestionar lecturas.
"""

class ReadingService:
    """
    Casos de uso para lecturas de consumo.
    
    Responsabilidades:
    - Obtener/crear lecturas
    - Detectar anomalías
    - Reportar estadísticas
    
    Ejemplo de uso:
        >>> service = ReadingService(db=real_db)
        >>> reading = service.create(power_kw=52.3)
        >>> is_anomaly = service.is_anomaly(reading.id)
    """
    
    def __init__(self, db: ReadingRepository):
        """
        Inicializa servicio.
        
        Args:
            db: Repositorio de lecturas (inyección de dependencia).
        """
        self.db = db
    
    def create(self, power_kw: float) -> Reading:
        """
        Crea lectura nueva.
        
        Args:
            power_kw: Consumo en kW.
        
        Returns:
            Reading: Entidad creada.
        
        Raises:
            ValueError: Si power_kw < 0.
        """
        if power_kw < 0:
            raise ValueError("power_kw debe ser >= 0")
        
        reading = Reading(timestamp=now(), power_kw=power_kw)
        self.db.save(reading)
        return reading
```

### 3. Generar Documentación con Sphinx

```bash
# Instalar
pip install sphinx sphinx-rtd-theme

# Crear estructura
sphinx-quickstart docs/

# Editar docs/conf.py
project = 'Energy-ML'
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon']
html_theme = 'sphinx_rtd_theme'

# Generar
cd docs/
make html

# Ver en navegador
open _build/html/index.html
```

**Sphinx extrae docstrings automáticamente:**
```rst
.. automodule:: src.domain.entities
   :members:
   :undoc-members:
```

### 4. Documento de Arquitectura (ARCHITECTURE.md)

```markdown
# Arquitectura del Proyecto

## Decisiones de Diseño

### 1. Clean Architecture (4 Capas)

**Por qué:** Permite cambiar frameworks/BD sin tocar lógica de negocio.

**Implementación:**
- Domain: @dataclass, sin dependencias externas
- Application: Servicios, DTOs, @pydantic
- Adapters: Presenters JSON, repositorio abstracto
- Infrastructure: FastAPI, PostgreSQL, MQTT

### 2. Inyección de Dependencias

**Por qué:** Facilita testing (pasar mocks), desacoplamiento.

**Ejemplo:**
```python
service = ReadingService(db=MockDB())  # en tests
service = ReadingService(db=PostgresDB())  # en prod
```

### 3. Tipado Exhaustivo (Pyright)

**Por qué:** Detecta bugs en edit time (IDE), no en runtime.

**Enforced en:** src/domain, src/application

### 4. Testing con Pytest

**Por qué:** Mejor sintaxis que unittest, fixtures reutilizables.

**Cobertura:** >= 85% (mandatory)

## Dependencias y Justificación

| Librería | Versión | Uso | Alternativa |
|----------|---------|-----|------------|
| fastapi | ^0.100 | Framework REST | Django (más pesado) |
| sqlalchemy | ^2.0 | ORM | Django ORM (menos flexible) |
| pydantic | ^2.0 | Validación DTOs | dataclasses (sin validación) |
| pytest | ^7.0 | Testing | unittest (menos ergonómico) |
| paho-mqtt | ^1.6 | Cliente MQTT | pika (RabbitMQ, not MQTT) |

## Rendimiento y Escalabilidad

### Benchmarks Actuales
- Dashboard GET /readings: 150ms (< 200ms OK)
- Predicción ML: 2s (ML es CPU-bound, aceptable)
- MQTT latency: 5s sensor → 50ms app (OK)

### Plan de Escalabilidad
- [ ] Índices BD en timestamp, power_kw
- [ ] Caché (Redis) de predicciones
- [ ] Async tasks para retraining ML (celery)
```

## Actividad Práctica

1. **Escribe README.md ejecutable:**
   - Debe poder clonar, instalar, ejecutar en 5 min
   - Secciones: Descripción, Instalación, Ejecución, Troubleshooting
   - Incluir 3-5 ejemplos funcionales

2. **Documenta TODO en docstrings:**
   ```bash
   # Validar cobertura de docstrings
   pydocstyle src/
   ```

3. **Genera docs con Sphinx:**
   ```bash
   sphinx-build -b html docs/ docs/_build/
   # Abre docs/_build/index.html
   ```

4. **Crea ARCHITECTURE.md:**
   - Decisiones clave justificadas
   - Benchmarks
   - Roadmap de escalabilidad

## Palabras clave

README, Docstrings, API Documentation, Sphinx, User Guide, Developer Guide

## Referencias

- spec § 5.4 (Documentación)
- Google Python Style Guide (docstrings)
- Sphinx documentation: https://www.sphinx-doc.org/
