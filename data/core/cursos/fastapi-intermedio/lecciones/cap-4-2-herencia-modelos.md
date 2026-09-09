### 4.2 Herencia de Clases y Variaciones de Modelos (Model Inheritance Variations)

En aplicaciones reales de FastAPI, un mismo recurso de la base de datos (por ejemplo, un `Sensor` o un `Usuario`) requiere distintas representaciones según el contexto:
1. **Creación (`Create`)**: El cliente envía los datos sin ID ni campos generados por el servidor.
2. **Actualización (`Update`)**: Todos o la mayoría de los campos son opcionales.
3. **Persistencia (`InDB`)**: Incluye el ID asignado por la base de datos y hashes privados.
4. **Respuesta (`Response`)**: Filtra datos sensibles y formatea la salida para el cliente.

Para evitar duplicar código entre todos estos esquemas, aplicamos el patrón de **Herencia de Modelos en Pydantic**.

---

### 1. El Patrón de Herencia de Esquemas en Pydantic

Definimos una clase base con los atributos comunes y derivamos de ella las clases específicas para cada operación:

```python
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, EmailStr

# 1. CLASE BASE: Atributos compartidos por todas las variaciones
class SensorBase(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=50)
    ubicacion: str = Field(..., description="Planta o sector industrial")
    unidad_medida: str = Field(default="V")

# 2. ESQUEMA DE CREACIÓN (POST /sensores): El cliente envía estos datos
class SensorCreate(SensorBase):
    # Hereda nombre, ubicacion y unidad_medida sin modificar
    pass

# 3. ESQUEMA DE ACTUALIZACIÓN (PATCH /sensores/{id}): Todos los campos son opcionales
class SensorUpdate(BaseModel):
    nombre: str | None = None
    ubicacion: str | None = None
    unidad_medida: str | None = None
    activo: bool | None = None

# 4. ESQUEMA DE BASE DE DATOS (Interno): Incluye ID y clave secreta de API
class SensorInDB(SensorBase):
    id: UUID = Field(default_factory=uuid4)
    api_secret_key: str  # Dato privado interno de la base de datos
    creado_at: datetime = Field(default_factory=datetime.now)
    activo: bool = True

# 5. ESQUEMA DE RESPUESTA (response_model): Filtra api_secret_key
class SensorResponse(SensorBase):
    id: UUID
    creado_at: datetime
    activo: bool

    class Config:
        # Permite mapear automáticamente atributos desde objetos ORM (ej. SQLAlchemy)
        from_attributes = True
```

---

### 2. Integración en Endpoints de FastAPI

Con esta jerarquía de modelos, los controladores de FastAPI quedan fuertemente tipados y seguros:

```python
from fastapi import FastAPI, status, HTTPException
from uuid import UUID

app = FastAPI(title="API con Herencia de Modelos")

# Base de datos simulada
sensores_db: dict[UUID, SensorInDB] = {}

@app.post(
    "/sensores",
    response_model=SensorResponse,   # Salida limpia (sin api_secret_key)
    status_code=status.HTTP_201_CREATED
)
def crear_sensor(sensor_input: SensorCreate):
    # Convertimos el esquema de entrada al esquema de persistencia interna
    sensor_db = SensorInDB(
        **sensor_input.model_dump(),
        api_secret_key="sec_key_generada_999"
    )
    sensores_db[sensor_db.id] = sensor_db
    
    # Retornamos el objeto interno; FastAPI lo convertirá a SensorResponse automáticamente
    return sensor_db

@app.patch("/sensores/{sensor_id}", response_model=SensorResponse)
def actualizar_sensor_parcial(sensor_id: UUID, update_data: SensorUpdate):
    if sensor_id not in sensores_db:
        raise HTTPException(status_code=404, detail="Sensor no encontrado")
        
    sensor_actual = sensores_db[sensor_id]
    
    # Extraemos solo los campos explícitamente enviados en la petición (exclude_unset=True)
    datos_actualizados = update_data.model_dump(exclude_unset=True)
    
    # Actualizamos los atributos del modelo de BD
    sensor_modificado = sensor_actual.model_copy(update=datos_actualizados)
    sensores_db[sensor_id] = sensor_modificado
    
    return sensor_modificado
```

---

### Resumen de la Lección
La herencia de clases en Pydantic (`Base`, `Create`, `Update`, `InDB`, `Response`) es la mejor práctica para mantener un código DRY (*Don't Repeat Yourself*), separando estrictamente la validación de entrada de la seguridad en las respuestas de la API.
