### 2.1 Fundamentos de Programación en Python (Basics of Programming)

Python es un lenguaje de programación interpretado, de alto nivel, con **tipado dinámico y fuerte**, diseñado con un énfasis primordial en la legibilidad del código. En esta lección exploraremos los pilares fundamentales del lenguaje: su modelo de ejecución, reglas de indentación, tipos de datos nativos, lógica booleana, flujo de control y funciones.

---

### 1. Modelo de Ejecución, Tipado e Indentación

- **Interpretado y Bytecode**: Python compila el código fuente (`.py`) a un formato intermedio denominado **Bytecode** (`.pyc`), el cual es ejecutado por la Máquina Virtual de Python (**PVM**).
- **Tipado Dinámico y Fuerte**: Las variables no requieren declaración de tipo explícita (dinámico), pero el lenguaje no realiza conversiones implícitas incompatibles entre tipos (fuerte). Por ejemplo, `'10' + 5` elevará un `TypeError`.
- **Indentación (PEP 8)**: A diferencia de otros lenguajes que utilizan llaves `{}` para delimitar bloques de código, Python utiliza **4 espacios de sangría**. Una indentación inconsistente generará un `IndentationError` o `TabError`.

```python
# Punto de entrada estándar para ejecución de scripts
if __name__ == "__main__":
    print("Ejecutando script directamente")
```

---

### 2. Tipos de Datos Nativos (Built-in Types) y Lógica Booleana

Python incluye tipos de datos primarios integrados:
- **Numéricos**: Enteros (`int`), flotantes (`float`), complejos (`complex`).
- **Texto**: Cadenas de caracteres inmutables (`str`).
- **Nulo**: `NoneType` (representado por el singleton `None`).
- **Booleanos**: `bool` (`True` o `False`).

```python
# Evaluaciones Booleanas y Operadores Logicos (and, or, not)
temperatura = 85.5
presion = 12.0
sensor_activo = True

# Operadores de Pertenencia (in, not in)
sensores_habilitados = ["temp_01", "pres_02", "vib_01"]

es_critico = (temperatura > 80.0 and presion > 10.0) and sensor_activo
sensor_registrado = "temp_01" in sensores_habilitados
```

---

### 3. Control de Flujo y Bucles

#### A. Condicionales (`if`, `elif`, `else`)
```python
if temperatura > 100.0:
    estado = "CRÍTICO"
elif temperatura > 75.0:
    estado = "ADVERTENCIA"
else:
    estado = "NORMAL"
```

#### B. Bucles `while` y `for` (con `break`, `continue` y `else`)
El bucle **`while`** repite una secuencia mientras se cumpla una condición booleana, mientras que **`for`** itera sobre secuencias.

```python
# Bucle while con control fino
contador = 0
while contador < 5:
    contador += 1
    if contador == 2:
        continue  # Salta a la siguiente iteración
    if contador == 4:
        break     # Interrumpe el bucle por completo
else:
    print("Bucle completado sin interrupciones por break")
```

---

### 4. Definición de Funciones y Parámetros Dinámicos (`*args` y `**kwargs`)

Las funciones se declaran con la palabra clave `def`. Para aceptar una cantidad arbitraria de argumentos posicionales o de clave-valor, utilizamos `*args` (tupla) y `**kwargs` (diccionario):

```python
def calcular_telemetria_dinamica(sensor_id: str, *lecturas: float, **metadatos) -> dict:
    """
    *args captura lecturas posicionales infinitas como una tupla.
    **kwargs captura metadatos clave-valor como un diccionario.
    """
    promedio = sum(lecturas) / len(lecturas) if lecturas else 0.0
    return {
        "sensor_id": sensor_id,
        "promedio": promedio,
        "detalles": metadatos
    }

# Invocación dinámica
resultado = calcular_telemetria_dinamica(
    "S-101", 40.2, 45.8, 43.1,
    planta="Avellaneda", operador="Juan"
)
```

---

### Resumen de la Lección
Has repasado la sintaxis fundamental de Python: tipado dinámico, indentación estricta (PEP 8), lógica booleana, comprobación de existencia con `in`/`not in`, control de flujo con `while`/`for` y funciones dinámicas con `*args` y `**kwargs`.
