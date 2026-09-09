### 5.3 Dependencias Parametrizadas basadas en Clases (Class-Based Dependencies)

Mientras que las dependencias basadas en funciones son excelentes para tareas directas, las **dependencias basadas en clases** permiten mantener estado, recibir parámetros de configuración al instanciarse y reutilizar lógica avanzada mediante el método ejecutable **`__call__`**.

---

### 1. Reutilización de Parámetros de Consulta con Clases

En lugar de repetir los parámetros de paginación (`skip`, `limit`, `order_by`) en cada función controladora, creamos una clase dedicada:

```python
from fastapi import FastAPI, Depends, Query

app = FastAPI(title="API de Dependencias basadas en Clases")

# CLASE DE DEPENDENCIA: Agrupa parámetros de paginación reutilizables
class ParamsPaginacion:
    def __init__(
        self,
        skip: int = Query(default=0, ge=0, description="Registros a omitir"),
        limit: int = Query(default=10, ge=1, le=100, description="Límite por página"),
        order_by: str = Query(default="id", pattern=r"^[a-zA-Z_]+$")
    ):
        self.skip = skip
        self.limit = limit
        self.order_by = order_by

@app.get("/sensores")
def listar_sensores(pagination: ParamsPaginacion = Depends(ParamsPaginacion)):
    """
    Sintaxis extendida: Depends(ParamsPaginacion)
    """
    return {
        "skip": pagination.skip,
        "limit": pagination.limit,
        "order_by": pagination.order_by
    }

@app.get("/modelos")
def listar_modelos(pagination: ParamsPaginacion = Depends()):
    """
    Sintaxis atajo (Shortcut): Depends() deduce automáticamente la clase ParamsPaginacion
    partiendo de la anotación de tipo.
    """
    return {"skip": pagination.skip, "limit": pagination.limit}
```

---

### 2. Dependencias Parametrizadas con `__call__`

Para crear una dependencia **parametrizable** (que reciba configuraciones previas al ejecutarse), creamos una clase cuyo método `__init__` recibe los parámetros de configuración y cuyo método `__call__` realiza la validación HTTP:

```python
from fastapi import FastAPI, Depends, HTTPException, status, Header

app = FastAPI()

# CLASE DE DEPENDENCIA PARAMETRIZABLE
class EvaluadorPermisosRol:
    def __init__(self, rol_requerido: str):
        # Configuramos el rol exigido al instanciar la clase
        self.rol_requerido = rol_requerido

    def __call__(self, x_user_role: str = Header(..., alias="X-User-Role")) -> bool:
        # Se ejecuta cuando llega la petición HTTP
        if x_user_role != self.rol_requerido:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Acceso denegado. Se requiere el rol '{self.rol_requerido}'."
            )
        return True

# Instanciamos dependencias parametrizadas para distintos roles
requiere_admin = EvaluadorPermisosRol(rol_requerido="admin")
requiere_operador = EvaluadorPermisosRol(rol_requerido="operador")

@app.get("/panel/admin", dependencies=[Depends(requiere_admin)])
def panel_administracion():
    return {"status": "Bienvenido al panel de control de administración"}

@app.get("/panel/monitoreo", dependencies=[Depends(requiere_operador)])
def panel_monitoreo():
    return {"status": "Bienvenido al panel de monitoreo de planta"}
```

---

### Resumen de la Lección
Las dependencias basadas en clases encapsulan conjuntos de parámetros de consulta con la sintaxis abreviada `Depends()`, y permiten crear validadores configurables mediante el método dunder `__call__`.
