### 4.4 Manejo e Inspección de Objetos Pydantic (Working with Pydantic Objects)

Una vez que un modelo de Pydantic V2 ha sido instanciado o recibido en un endpoint de FastAPI, Pydantic ofrece métodos avanzados para inspeccionar, exportar a diccionarios/JSON, clonar objetos y configurar el comportamiento global del esquema.

---

### 1. Conversión de Objetos Pydantic a Diccionario y JSON

#### A. Exportar a Diccionario con `.model_dump()`
En Pydantic V2, el antiguo método `.dict()` fue reemplazado por **`.model_dump()`**:

```python
from pydantic import BaseModel, Field

class Telemetria(BaseModel):
    sensor_id: str
    temperatura: float
    vibracion: float = 0.0
    nota_interna: str | None = None

t1 = Telemetria(sensor_id="s1", temperatura=45.2)

# Conversión a dict de Python
data_dict = t1.model_dump()
# {'sensor_id': 's1', 'temperatura': 45.2, 'vibracion': 0.0, 'nota_interna': None}

# Excluir valores no asignados (exclude_unset=True)
data_unset = t1.model_dump(exclude_unset=True)
# {'sensor_id': 's1', 'temperatura': 45.2}

# Excluir valores nulos (exclude_none=True)
data_no_none = t1.model_dump(exclude_none=True)
# {'sensor_id': 's1', 'temperatura': 45.2, 'vibracion': 0.0}
```

#### B. Exportar a Cadena JSON con `.model_dump_json()`
Reemplaza al antiguo `.json()`. Serializa tipos de datos complejos (como `datetime`, `UUID` o `Decimal`) a su representación válida en JSON:

```python
json_str = t1.model_dump_json(indent=2)
```

---

### 2. Creación e Invocación desde Cadenas o Diccionarios

Podemos construir instancias de modelos validadas a partir de diccionarios o cadenas JSON crudas usando los métodos de clase **`.model_validate()`** y **`.model_validate_json()`**:

```python
# 1. Crear desde un diccionario
dict_raw = {"sensor_id": "s99", "temperatura": 88.4}
objeto_desde_dict = Telemetria.model_validate(dict_raw)

# 2. Crear directamente desde una cadena JSON
json_raw = '{"sensor_id": "s100", "temperatura": 12.5}'
objeto_desde_json = Telemetria.model_validate_json(json_raw)
```

---

### 3. Copia y Modificación Inmutable con `.model_copy()`

Pydantic permite clonar una instancia modificando atributos específicos sin alterar la instancia original:

```python
t_original = Telemetria(sensor_id="s1", temperatura=20.0)

# Clonar actualizando solo la temperatura
t_modificada = t_original.model_copy(update={"temperatura": 25.5})

print(t_original.temperatura)   # 20.0 (permanece inalterada)
print(t_modificada.temperatura) # 25.5
```

---

### 4. Configuración del Modelo con `ConfigDict`

En Pydantic V2, la configuración del esquema se define declarando la variable de clase `model_config = ConfigDict(...)`:

```python
from pydantic import BaseModel, ConfigDict

class ConfiguredModel(BaseModel):
    sensor_name: str
    valor_float: float

    model_config = ConfigDict(
        # Elimina espacios en blanco de cadenas de texto automáticamente
        str_strip_whitespace=True,
        # Rechaza campos extra no declarados en el esquema (frozen / strict)
        extra="forbid",
        # Permite mapear atributos ORM (SQLAlchemy) con model_validate()
        from_attributes=True,
        # Si es True, hace el objeto inmutable (read-only)
        frozen=False
    )
```

---

### Resumen de la Lección
Métodos clave de Pydantic V2 para producción:
- `.model_dump()`: Exporta a diccionario.
- `.model_dump_json()`: Serializa a cadena JSON.
- `.model_validate()` / `.model_validate_json()`: Construye e inspecciona objetos desde datos externos.
- `.model_copy(update={...})`: Clona objetos aplicando cambios parciales.
- `ConfigDict`: Controla el rigor de validación y la conversión ORM.
