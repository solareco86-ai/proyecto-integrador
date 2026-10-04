# 1.1 Fuentes de datos: sensores energéticos, logs académicos y APIs

## Objetivo

Identificar y conectar las múltiples fuentes de datos que alimentarán el proyecto integrador:
- **Proyecto energético**: Telemetría de sensores de consumo eléctrico, facturas, reportes de distribuidoras
- **Proyecto académico**: Logs de plataforma de aprendizaje, datos de inscripción, métricas de interacción

## Contenidos

### 1. Fuentes de datos del proyecto energético

#### a) Sensores de energía (telemetría en tiempo real)

**Datos disponibles:**
- Consumo de potencia (kW) cada X minutos
- Voltaje, corriente, factor de potencia
- Temperatura ambiente (correlación)
- Marca de tiempo y geolocalización

**Formato típico:** CSV, JSON desde API REST o MQTT

**Ejemplo de estructura:**
```csv
timestamp,facility_id,power_kw,voltage_v,current_a,pf,temp_c
2026-10-01 06:00:00,001,2.5,230,10.8,0.95,18.2
2026-10-01 06:05:00,001,2.3,230,10.0,0.94,18.5
2026-10-01 06:10:00,001,2.8,229,12.2,0.96,18.1
```

#### b) Facturas de electricidad

**Fuentes:**
- Archivos PDF de distribuidoras (EDENOR, EDESUR, etc.)
- Fotografías de facturas capturadas
- APIs de distribuidoras (si disponibles)

**Datos relevantes:**
- Período de facturación
- Consumo en kWh
- Tarifa aplicada
- Monto total

#### c) Reportes históricos

- Bases de datos de consumo mensual
- Reportes anuales del instituto
- Información de proyectos anteriores

### 2. Fuentes de datos del proyecto académico

#### a) Plataforma de Learning Management System (LMS)

**Datos disponibles:**
- Logs de acceso a cursos (timestamp, estudiante, duración)
- Calificaciones y entregas
- Participación en foros
- Acceso a recursos

**Formato:** Base de datos SQL, exportaciones CSV

**Ejemplo:**
```csv
student_id,course_id,event_type,timestamp,score,duration_min
STU001,CIS-301,login,2026-10-01 08:15:00,,2
STU001,CIS-301,resource_access,2026-10-01 08:17:00,,5
STU001,CIS-301,assignment_submit,2026-10-01 09:30:00,85,45
```

#### b) Sistema de inscripción y documentación

- DNI, nombre, fecha de ingreso
- Carrera, año y comisión
- Antecedentes académicos
- Información de contacto

#### c) Encuestas y feedback

- Satisfacción con cursos
- Dificultades reportadas
- Datos de clima institucional

### 3. Patrones de Ingesta (Clean Architecture)

Según [spec/backend/srs-spec](https://github.com/datamaq-automation/spec/blob/main/backend/srs-spec-backend-fastapi.md), **la ingesta de datos es responsabilidad de la capa Infrastructure**. No debe haber conexiones directas desde `application/` o `domain/`.

**Arquitectura recomendada:**
```
src/
├── domain/           (entidades, value objects, sin dependencias externas)
├── application/      (servicios, DTOs, mappers - nunca acceso directo a BD)
├── adapters/         (presenters, repositorio abstracto)
└── infrastructure/   (implementación de repositorio, inicialización de FastAPI)
    ├── db/
    │   ├── connection.py      (SQLAlchemy engine)
    │   └── repositories.py    (hereda de adapter.repositories.BaseRepository)
    ├── integrations/
    │   ├── mqtt_client.py     (sensores energéticos en vivo)
    │   ├── api_client.py      (consultas REST a servicios externos)
    │   └── pdf_extractor.py   (OCR de facturas)
    └── config.py
```

### 3.1 Lectura desde CSV (datos históricos)

```python
# src/infrastructure/integrations/csv_loader.py
from pathlib import Path
import pandas as pd
from typing import Tuple

class CSVDataLoader:
    """Carga datos históricos desde archivos CSV"""
    
    @staticmethod
    def load_energy_sensors(filepath: str) -> pd.DataFrame:
        """Carga telemetría energética con validación de tipos"""
        df = pd.read_csv(filepath, parse_dates=['timestamp'])
        # Validar tipos según dominio (ver src/domain/energetica/value_objects.py)
        assert df['power_kw'].dtype == 'float64'
        assert df['timestamp'].dtype == 'datetime64[ns]'
        return df
    
    @staticmethod
    def load_academic_events(filepath: str) -> pd.DataFrame:
        """Carga logs de LMS"""
        df = pd.read_csv(filepath, parse_dates=['event_timestamp'])
        return df
```

### 3.2 Conexión a Base de Datos SQL (Clean Architecture)

```python
# src/infrastructure/db/connection.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.infrastructure.config import Settings

class DatabaseConnection:
    def __init__(self, settings: Settings):
        self.engine = create_async_engine(
            f"mysql+aiomysql://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}/{settings.DB_NAME}",
            echo=False  # Loguear queries en desarrollo: echo=settings.DEBUG
        )
        self.SessionLocal = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)
    
    async def get_session(self) -> AsyncSession:
        async with self.SessionLocal() as session:
            yield session
```

**Inyección en FastAPI (sin hardcodeo):**
```python
# src/infrastructure/fastapi/routes/academic_events.py
from fastapi import APIRouter, Depends
from src.application.services.academic_service import AcademicService
from src.infrastructure.db.connection import DatabaseConnection

router = APIRouter()

@router.get("/events/{student_id}")
async def get_student_events(
    student_id: str,
    service: AcademicService = Depends(AcademicService)
):
    """Obtiene eventos de un estudiante desde DB"""
    return await service.fetch_events(student_id)
```

### 3.3 Lectura desde API REST

```python
# src/infrastructure/integrations/api_client.py
import httpx
from typing import AsyncGenerator
import logging

logger = logging.getLogger(__name__)

class EnergyAPIClient:
    """Cliente REST para API de sensores (implementa patrón Repository)"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.api_key = api_key
    
    async def fetch_telemetry(self, facility_id: str, period: str) -> list[dict]:
        """
        Obtiene telemetría de sensores energéticos
        Args:
            facility_id: ID de instalación (ej: 'ISFT-001')
            period: Período ISO 8601 (ej: '2026-10')
        Returns:
            Lista de registros con timestamp, power_kw, voltage_v, etc.
        """
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/v1/sensores",
                    params={"facility": facility_id, "period": period},
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    timeout=10.0
                )
                response.raise_for_status()
                return response.json()['records']
            except httpx.HTTPError as e:
                logger.error(f"Error fetching telemetry: {e}")
                raise  # Propagar; la capa application maneja el error
```

### 3.4 Lectura desde PDFs (OCR de facturas)

```python
# src/infrastructure/integrations/pdf_extractor.py
import pdfplumber
from pathlib import Path
from dataclasses import dataclass

@dataclass
class InvoiceData:
    """Value object de datos extraídos de factura"""
    periodo_inicio: str  # ISO 8601
    periodo_fin: str
    consumo_kwh: float
    distribuidor: str  # EDENOR, EDESUR, etc.
    monto_total: float

class BillExtractor:
    """Extrae datos estructurados de facturas de electricidad"""
    
    @staticmethod
    def extract_from_pdf(filepath: str) -> InvoiceData:
        """Extrae consumo, período y distribuidor de PDF"""
        with pdfplumber.open(filepath) as pdf:
            tabla = pdf.pages[0].extract_table()
            # Parsear según formato de distribuidor
            # (EDENOR vs EDESUR tienen formatos diferentes)
            return BillExtractor._parse_table(tabla)
    
    @staticmethod
    def _parse_table(tabla: list) -> InvoiceData:
        # Lógica de parsing específica por distribuidor
        # Ver Cap 2.2 (OCR) para detalles
        pass
```

### 4. Validación inicial de fuentes

**Preguntas clave antes de empezar:**

1. ¿Qué período de datos históricos tenemos disponibles?
2. ¿Cuál es la frecuencia de actualización de cada fuente?
3. ¿Existen valores faltantes o inconsistencias conocidas?
4. ¿Hay restricciones de acceso o confidencialidad?
5. ¿Los datos están en el mismo zona horaria?
6. ¿Existen identificadores comunes para cruzar datos (ej: facility_id, student_id)?

## Actividad práctica

**Tarea:** Conectar a una de las fuentes de datos reales del proyecto y mostrar las primeras 10 filas + info básica.

```python
# Pseudocódigo - adaptar según tu fuente
import pandas as pd

# 1. Cargar datos
datos = pd.read_csv('ruta/a/archivo.csv')  # O tu método de lectura

# 2. Inspeccionar
print(f"Shape: {datos.shape}")
print(f"\nPrimeras filas:\n{datos.head(10)}")
print(f"\nTipos de datos:\n{datos.dtypes}")
print(f"\nValores faltantes:\n{datos.isnull().sum()}")

# 3. Resumen estadístico
print(f"\nResumen:\n{datos.describe()}")
```

## Palabras clave

Ingesta, ETL (Extract-Transform-Load), fuentes heterogéneas, conectores, pandas, sqlalchemy, API REST, CSV, JSON, PDF, MQTT

## Referencias

- [Pandas read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [Requests: HTTP library](https://requests.readthedocs.io/)
- [pdfplumber: PDF parsing](https://github.com/jsvine/pdfplumber)
