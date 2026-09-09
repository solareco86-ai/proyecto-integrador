### 5.4 Dependencias a Nivel de Ruta, Router y Global (Scope Levels of Dependencies)

No todas las dependencias devuelven valores que deben ser inyectados como argumentos en la función controladora. Muchas dependencias realizan tareas transversales (como verificar claves de API, registrar métricas o aplicar limitación de tasa - *rate-limiting*) que deben ejecutarse a nivel de **Ruta Individual**, **APIRouter** o **Aplicación Global**.

---

### 1. Dependencias a Nivel de Ruta (`dependencies=[Depends(...)]`)

Si deseamos que una dependencia se ejecute obligatoriamente antes del endpoint pero **no necesitamos recibir su valor de retorno** como parámetro de función, utilizamos la propiedad `dependencies` del decorador:

```python
from fastapi import FastAPI, Depends, Header, HTTPException

app = FastAPI()

def verificar_api_key(x_api_key: str = Header(...)):
    if x_api_key != "secret-api-key-2026":
        raise HTTPException(status_code=403, detail="API Key no válida")

# La dependencia se ejecuta antes del controlador sin inyectar ningún parámetro
@app.get("/reportes/exportar", dependencies=[Depends(verificar_api_key)])
def exportar_reporte():
    return {"status": "exportando_datos"}
```

---

### 2. Dependencias a Nivel de `APIRouter`

Para aplicar una o más dependencias a **todos los endpoints pertenecientes a un enrutador específico**, declaramos la lista en la instanciación de `APIRouter`:

```python
from fastapi import APIRouter, Depends, Header, HTTPException

# Todos los endpoints de este router requerirán la validación de API Key
router_sensores = APIRouter(
    prefix="/api/v1/sensores",
    tags=["Sensores Protegidos"],
    dependencies=[Depends(verificar_api_key)]
)

@router_sensores.get("/lecturas")
def obtener_lecturas():
    return [{"id": "s1", "val": 10.5}]

@router_sensores.get("/alerta")
def obtener_alertas():
    return [{"id": "s2", "alerta": "alta_temp"}]
```

---

### 3. Dependencias a Nivel Global (`FastAPI(dependencies=[...])`)

Para aplicar reglas de seguridad, auditoría o cortafuegos a **absolutamente todas las rutas de la aplicación web**, pasamos la lista de dependencias al instanciar la clase principal `FastAPI()`:

```python
from fastapi import FastAPI, Depends, Header, HTTPException

def cortafuegos_global(user_agent: str | None = Header(default=None)):
    # Bloquear clientes automatizados no deseados en toda la app
    if user_agent and "bad-bot" in user_agent.lower():
        raise HTTPException(status_code=403, detail="Cliente bloqueado por política de seguridad global")

# Aplicar dependencia de forma global a TODOS los endpoints de la API
app = FastAPI(
    title="API Segura Global",
    dependencies=[Depends(cortafuegos_global)]
)

@app.get("/")
def home():
    return {"mensaje": "API protegida globalmente"}
```

---

### Resumen de la Lección
Niveles de alcance (*Scopes*) de dependencias en FastAPI:
1. **Inyección en Parámetro de Función**: `def ep(val = Depends(dep))` $\rightarrow$ Se ejecuta y entrega el valor devuelto a la función.
2. **Nivel de Ruta**: `@app.get("/", dependencies=[Depends(dep)])` $\rightarrow$ Se ejecuta solo para esa URL.
3. **Nivel de APIRouter**: `APIRouter(dependencies=[Depends(dep)])` $\rightarrow$ Se ejecuta para todo el grupo de rutas del router.
4. **Nivel Global**: `FastAPI(dependencies=[Depends(dep)])` $\rightarrow$ Se ejecuta para toda la aplicación.
