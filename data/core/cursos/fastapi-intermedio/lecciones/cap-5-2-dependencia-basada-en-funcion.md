### 5.2 Creación y Uso de Dependencias basadas en Funciones (Function Dependencies & Yield)

En FastAPI, cualquier función de Python que acepte argumentos puede ser utilizada como una dependencia mediante la función **`Depends()`**.

---

### 1. Inyección de una Función de Dependencia Básica

Definimos una función estándar de Python y la inyectamos en el parámetro del controlador envuelta en `Depends(nombre_funcion)`:

```python
from fastapi import FastAPI, Depends, Header, HTTPException, status

app = FastAPI(title="API con Dependencia basada en Función")

# 1. FUNCIÓN DE DEPENDENCIA: Extrae y valida el encabezado X-Token
def validar_token_autorizacion(x_token: str = Header(..., description="Token de acceso")):
    if x_token != "token-secreto-datamaq":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de autorización inválido o ausente"
        )
    return {"usuario": "operador_industrial", "rol": "admin"}

# 2. CONTROLADOR: Inyecta el resultado devuelto por la dependencia
@app.get("/telemetria/protegida")
def obtener_telemetria_privada(user_info: dict = Depends(validar_token_autorizacion)):
    return {
        "status": "acceso_autorizado",
        "usuario": user_info["usuario"],
        "datos": {"temperatura": 45.2, "vibracion": 0.04}
    }
```

---

### 2. Sub-dependencias (Enlace de Dependencias)

Una función de dependencia puede requerir a su vez **otra dependencia**, creando un árbol de resolución ejecutado automáticamente por FastAPI:

```python
# Sub-dependencia 1: Lee el encabezado User-Agent
def obtener_user_agent(user_agent: str | None = Header(default=None)):
    return user_agent or "Desconocido"

# Dependencia Principal: Depende de Sub-dependencia 1
def auditar_peticion(
    user_info: dict = Depends(validar_token_autorizacion),
    agent: str = Depends(obtener_user_agent)
):
    return {
        "usuario": user_info["usuario"],
        "client_agent": agent,
        "timestamp_acceso": "2026-07-21"
    }

@app.get("/reporte/auditoria")
def get_reporte_auditoria(audit_data: dict = Depends(auditar_peticion)):
    return audit_data
```

---

### 3. Dependencias con Cierre de Recursos (`yield` y Clean-up)

Para gestionar recursos que requieren apertura y cierre (como sesiones de base de datos SQL o conexiones a sockets), utilizamos la palabra clave **`yield`**.

El código **antes del `yield`** se ejecuta antes de llamar al controlador, y el código **después del `yield`** se ejecuta automáticamente al finalizar la respuesta, incluso si ocurrió una excepción durante la petición:

```python
from typing import Generator
from fastapi import FastAPI, Depends

app = FastAPI()

# Simulación de conexión a Base de Datos
class SesionBaseDatos:
    def __init__(self):
        self.conectado = True
        print("-> Conexión a Base de Datos ABRIERTA")

    def cerrar(self):
        self.conectado = False
        print("<- Conexión a Base de Datos CERRADA")

# Dependencia con yield (Context Manager)
def obtener_db_session() -> Generator[SesionBaseDatos, None, None]:
    db = SesionBaseDatos()
    try:
        yield db  # Retorna la sesión al controlador
    finally:
        db.cerrar()  # Garantiza el cierre del recurso al finalizar la llamada HTTP

@app.get("/equipos/db")
def listar_equipos_db(db: SesionBaseDatos = Depends(obtener_db_session)):
    return {"status": "ok", "db_activa": db.conectado}
```

---

### Resumen de la Lección
Las dependencias basadas en funciones con `Depends()` y `yield` permiten resolver parámetros, encadenar sub-dependencias y garantizar la liberación limpia de recursos de base de datos sin contaminar los controladores web.
