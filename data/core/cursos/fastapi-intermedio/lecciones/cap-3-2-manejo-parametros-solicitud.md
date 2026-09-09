### 3.2 Manejo de Parámetros de Solicitud (Handling Request Parameters)

FastAPI abstrae y valida automáticamente todos los datos de entrada (*Request Parameters*) que un cliente envía al servidor: parámetros de ruta, parámetros de consulta, cuerpo de la petición (JSON), datos de formulario, carga de archivos, encabezados HTTP y cookies.

---

### 1. Parámetros de Ruta (Path Parameters) y `Path()`

Los **parámetros de ruta** se extraen de la URL (`/equipos/{equipo_id}`). Mediante `Path()` y `Enum` limitamos los valores aceptados y agregamos validaciones avanzadas:

```python
from enum import Enum
from fastapi import FastAPI, Path

app = FastAPI()

class CategoriaEquipo(str, Enum):
    BOMBA = "bomba"
    COMPRESOR = "compresor"

@app.get("/equipos/{categoria}/{equipo_id}")
def obtener_equipo(
    categoria: CategoriaEquipo,
    equipo_id: int = Path(..., title="ID del equipo", ge=1, le=9999)
):
    return {"categoria": categoria, "equipo_id": equipo_id}
```

---

### 2. Parámetros de Consulta (Query Parameters) y `Query()`

Los **parámetros de consulta** se envían en la URL a continuación del signo `?` (`/mediciones?planta=Pilar&limit=10`). La función `Query()` permite añadir alias, requerir valores obligatorios (`...`) o recibir múltiples valores (`list[str]`):

```python
from fastapi import Query

@app.get("/mediciones")
def listar_mediciones(
    planta: str = Query("Avellaneda", alias="planta-origen", min_length=3),
    limit: int = Query(10, ge=1, le=100),
    tags: list[str] = Query(default=[], description="Filtrar por tags ?tags=t1&tags=t2")
):
    return {"planta": planta, "limit": limit, "tags": tags}
```

---

### 3. Cuerpo de la Petición (`BaseModel`, `Body` y Múltiples Objetos)

Para peticiones `POST` o `PUT` con JSON, declaramos uno o varios modelos de **Pydantic** (`BaseModel`) en el controlador. FastAPI combina **múltiples objetos** o valores escalares con `Body()`:

```python
from pydantic import BaseModel, Field
from fastapi import Body

class DatosSensor(BaseModel):
    sensor_id: str
    temperatura: float

class Configuracion(BaseModel):
    modo: str = "auto"

@app.post("/sensor/configurar")
def registrar_sensor_completo(
    sensor: DatosSensor,                 # Objeto 1
    config: Configuracion,               # Objeto 2
    prioridad: int = Body(..., ge=1)     # Escalar en el body
):
    return {"sensor": sensor, "config": config, "prioridad": prioridad}
```

---

### 4. Formularios, Archivos, Encabezados y Cookies (`Form`, `UploadFile`, `Header`, `Cookie`)

FastAPI permite recibir datos de formulario `application/x-www-form-urlencoded` con `Form()`, archivos subidos con `UploadFile` ( streaming sin saturar la RAM), cabeceras HTTP con `Header()` y cookies con `Cookie()`:

```python
from fastapi import Form, File, UploadFile, Header, Cookie

@app.post("/dataset/subir")
async def subir_dataset(
    nombre_dataset: str = Form(...),
    archivo_csv: UploadFile = File(...),
    user_agent: str | None = Header(default=None),
    session_id: str | None = Cookie(default=None)
):
    contenido_bytes = await archivo_csv.read(1024)  # Lee 1 KB sin cargar todo en RAM
    return {
        "dataset": nombre_dataset,
        "filename": archivo_csv.filename,
        "user_agent": user_agent,
        "session_id": session_id
    }
```

---

### Resumen de la Lección
FastAPI ofrece una interfaz unificada para procesar y validar cualquier parámetro de solicitud (*Path*, *Query*, *Body*, *Form*, *File*, *Header*, *Cookie*) garantizando datos tipados y limpios antes de ejecutar la lógica del endpoint.
