### 3.3 Personalización de la Respuesta (Customizing the Response)

FastAPI proporciona control total sobre las respuestas enviadas al cliente: filtrado automático con `response_model`, modificación de códigos de estado HTTP y encabezados, escritura de cookies seguras con `response.set_cookie()`, manejo de excepciones con `HTTPException` y retorno de clases de respuesta personalizadas (`JSONResponse`, `HTMLResponse`, `FileResponse`, `StreamingResponse`).

---

### 1. El Parámetro `response_model` y Filtrado de Datos

El parámetro `response_model` en el decorador garantiza que únicamente los campos declarados en el modelo Pydantic de salida sean expuestos al cliente, ocultando datos sensibles (como contraseñas u hashes):

```python
from fastapi import FastAPI, status
from pydantic import BaseModel, EmailStr

app = FastAPI()

class UsuarioInput(BaseModel):
    username: str
    email: EmailStr
    password: str

class UsuarioOutput(BaseModel):
    id: int
    username: str
    email: EmailStr

@app.post("/usuarios", response_model=UsuarioOutput, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioInput):
    # Se retorna el diccionario completo con hash, pero FastAPI filtrará solo UsuarioOutput
    return {
        "id": 1,
        "username": usuario.username,
        "email": usuario.email,
        "hashed_password": f"hash_{usuario.password}"
    }
```

---

### 2. Modificación Dinámica de Headers, Cookies y Status Code

Inyectando el objeto **`response: Response`** podemos ajustar el código de estado dinámicamente (`response.status_code`), añadir encabezados y configurar cookies seguras con `response.set_cookie()`:

```python
from fastapi import Response, status

@app.post("/auth/login")
def login(response: Response, usuario: str):
    # 1. Código de estado dinámico (202 Accepted)
    response.status_code = status.HTTP_202_ACCEPTED
    
    # 2. Añadir cabecera personalizada
    response.headers["X-DataMaq-Server"] = "Node-01"
    
    # 3. Configurar cookie segura (HttpOnly + Secure + SameSite)
    response.set_cookie(
        key="access_token",
        value="secret_jwt_token_123",
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600
    )
    return {"status": "login_exitoso"}
```

---

### 3. Elevando Errores con `HTTPException` y Clases de Respuesta Personalizadas

#### A. Elevación de Errores con `HTTPException`
```python
from fastapi import HTTPException, status

@app.get("/items/{item_id}")
def obtener_item(item_id: int):
    if item_id > 100:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"El recurso con ID {item_id} no fue encontrado."
        )
    return {"item_id": item_id}
```

#### B. Clases de Respuesta Específicas (`JSONResponse`, `HTMLResponse`, `FileResponse`)
```python
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse

@app.get("/landing", response_class=HTMLResponse)
def get_html():
    return "<h1>Panel de Control DataMaq</h1>"

@app.get("/descargar-reporte")
def descargar_reporte():
    return FileResponse(
        path="data/export/reporte.csv",
        filename="reporte_2026.csv",
        media_type="text/csv"
    )

@app.get("/legacy")
def redirigir():
    return RedirectResponse(url="/landing", status_code=307)
```

---

### Resumen de la Lección
Mediante `response_model`, la inyección del parámetro `Response`, la elevación de `HTTPException` y las clases de respuesta nativas, podés personalizar de forma precisa el contenido, seguridad y cabeceras de cada respuesta HTTP.
