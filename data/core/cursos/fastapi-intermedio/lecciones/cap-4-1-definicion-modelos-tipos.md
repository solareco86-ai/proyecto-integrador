### 4.1 Definición de Modelos y Tipos de Campos con Pydantic (Defining Models & Field Types)

**Pydantic** es la librería estándar utilizada por FastAPI para la definición de esquemas de datos, conversión automática de tipos (*parsing*) y validación estricta en tiempo de ejecución basada en las anotaciones de tipo de Python.

---

### 1. Definición de un Modelo con `BaseModel`

Para definir un esquema de datos en Pydantic V2, creamos una clase que herede de `pydantic.BaseModel` y declaramos sus atributos con anotaciones de tipo:

```python
from datetime import datetime
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, HttpUrl

class SensorLectura(BaseModel):
    id: UUID = uuid4()                         # Valor por defecto generado dinámicamente
    sensor_id: str                              # Campo obligatorio
    temperatura: float                          # Coma flotante obligatorio
    humedad_relativa: float | None = None       # Opcional (puede ser None)
    timestamp: datetime = datetime.now()        # Fecha/hora ISO 8601
    activo: bool = True                         # Booleano con valor por defecto
```

---

### 2. Tipos de Campos Complejos de Pydantic

Pydantic incluye tipos de datos especializados para validar formatos comunes sin escribir expresiones regulares manuales:

- **`EmailStr`**: Valida que la cadena sea una dirección de correo electrónico válida (requiere `pip install email-validator`).
- **`HttpUrl` / `AnyUrl`**: Valida esquemas de URL sintácticamente válidos (`http://`, `https://`).
- **`UUID`**: Valida identificadores únicos universales (`UUID4`, `UUID1`).
- **`SecretStr`**: Oculta valores sensibles (como contraseñas o API keys) al imprimir o serializar el objeto (`repr()` mostrará `'**********'`).

```python
from pydantic import BaseModel, EmailStr, HttpUrl, SecretStr

class UsuarioRegistro(BaseModel):
    username: str
    email: EmailStr
    sitio_web: HttpUrl | None = None
    api_key_privada: SecretStr
```

---

### 3. Restricciones y Metadatos con `Field()`

La función **`Field()`** de Pydantic permite establecer restricciones numéricas, límites de longitud, metadatos para la documentación OpenAPI y descripciones detalladas:

```python
from pydantic import BaseModel, Field

class TelemetriaIndustrialInput(BaseModel):
    equipo_tag: str = Field(
        ...,
        title="Etiqueta del Equipo",
        description="Código identificador en formato TAG-XXX (ej. TAG-001)",
        min_length=5,
        max_length=20,
        pattern=r"^TAG-\d{3,5}$",
        examples=["TAG-001", "TAG-1050"]
    )
    presion_psi: float = Field(
        ...,
        title="Presión de Operación",
        description="Presión medida en libras por pulgada cuadrada (PSI)",
        gt=0.0,
        le=500.0
    )
    frecuencia_hz: float = Field(
        default=50.0,
        title="Frecuencia Eléctrica",
        ge=45.0,
        le=65.0
    )
```

#### Atributos Principales de `Field()`:
- `...` (Ellipsis): Indica que el campo es **estrictamente obligatorio**.
- `gt` / `ge`: Estrictamente mayor que / Mayor o igual que ($>$, $\ge$).
- `lt` / `le`: Estrictamente menor que / Menor o igual que ($<$, $\le$).
- `min_length` / `max_length`: Límites de longitud de caracteres para cadenas de texto.
- `pattern`: Expresión regular que debe cumplir el valor.
- `examples`: Lista de valores de ejemplo para la documentación de Swagger UI.

---

### Resumen de la Lección
`BaseModel` y `Field()` forman el núcleo del tipado en Pydantic y FastAPI. Permitir que Pydantic gestione la conversión e inspección de tipos garantiza que los controladores de FastAPI reciban datos limpios y seguros.
