### 2.3 Programación Orientada a Objetos en Python (Writing Object-Oriented Programs)

La **Programación Orientada a Objetos (POO / OOP)** en Python permite agrupar datos (atributos) y comportamientos (métodos) en estructuras modulares mediante la sintaxis de clases (`class`).

---

### 1. Definición de Clases e Instanciación

Toda clase en Python define un método constructor `__init__` que inicializa los atributos de la instancia. El primer parámetro de cualquier método de instancia debe ser **`self`**, el cual hace referencia al objeto actual.

```python
class DispositivoIndustrial:
    # Atributo de clase (compartido por todas las instancias)
    protocolo: str = "Modbus-TCP"

    def __init__(self, tag: str, ubicacion: str):
        # Atributos de instancia (únicos para cada objeto)
        self.tag = tag
        self.ubicacion = ubicacion
        self.activo = True

    def desactivar(self) -> None:
        self.activo = False
```

---

### 2. Métodos Mágicos (Dunder Methods)

Los **Dunder Methods** (*Double Underscore Methods*) son métodos especiales prefijados y sufijados con doble guión bajo `__` que permiten personalizar el comportamiento nativo de los objetos de Python.

#### A. Representación de Objetos (`__str__` y `__repr__`)
- **`__str__`**: Retorna una representación amigable y legible para el usuario final (invocado por `str()` o `print()`).
- **`__repr__`**: Retorna una representación inequívoca y formal orientada al desarrollador (invocado en la consola interactiva o depuración).

```python
class Sensor:
    def __init__(self, id_sensor: str, valor: float):
        self.id_sensor = id_sensor
        self.valor = valor

    def __str__(self) -> str:
        return f"Sensor {self.id_sensor}: {self.valor}"

    def __repr__(self) -> str:
        return f"Sensor(id_sensor={self.id_sensor!r}, valor={self.valor!r})"
```

#### B. Métodos de Comparación (`__eq__`, `__lt__`, `__gt__`)
Permiten comparar instancias usando los operadores estándar (`==`, `<`, `>`):

```python
class LecturaMétrica:
    def __init__(self, valor: float):
        self.valor = valor

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, LecturaMétrica):
            return False
        return self.valor == otro.valor

    def __lt__(self, otro: "LecturaMétrica") -> bool:
        return self.valor < otro.valor
```

#### C. Sobrecarga de Operadores Aritméticos (`__add__`, `__sub__`, `__mul__`)
Permiten sumar, restar o multiplicar objetos personalizados:

```python
class VectorPresion:
    def __init__(self, psi: float):
        self.psi = psi

    def __add__(self, otro: "VectorPresion") -> "VectorPresion":
        return VectorPresion(self.psi + otro.psi)
```

---

### 3. Reutilización de Lógica: Herencia y Herencia Múltiple

#### A. Herencia Simple y `super()`
La herencia permite extender las capacidades de una clase base. Mediante **`super()`** invocamos los métodos de la clase padre:

```python
class SensorBase:
    def __init__(self, id_sensor: str):
        self.id_sensor = id_sensor

class SensorTemperatura(SensorBase):
    def __init__(self, id_sensor: str, fahrenheit: float):
        super().__init__(id_sensor)  # Inicializa el atributo id_sensor del padre
        self.fahrenheit = fahrenheit
```

#### B. Herencia Múltiple y MRO (Method Resolution Order)
Python soporta la **Herencia Múltiple** (una clase puede heredar de múltiples clases padre). Para resolver qué método ejecutar cuando existen nombres coincidentes, Python utiliza el algoritmo C3 Linearization para establecer el **MRO**:

```python
class ConectableRed:
    def conectar((self):
        print("Conectando a la red industrial...")

class RegistradorLogs:
    def registrar(self):
        print("Escribiendo log de evento...")

# Herencia Múltiple
class SmartGateWay(ConectableRed, RegistradorLogs):
    pass

gateway = SmartGateWay()
gateway.conectar()
gateway.registrar()

# Inspeccionar el orden de resolución de métodos (MRO)
print(SmartGateWay.__mro__)
```

---

### Resumen de la Lección
La POO en Python combina clases, métodos mágicos dunder (`__str__`, `__repr__`, `__eq__`, `__add__`), herencia simple y herencia múltiple gestionada mediante el orden MRO para construir componentes de software robustos.
