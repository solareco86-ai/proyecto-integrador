### 4.1 Concepto de Subproceso: Funciones y Procedimientos

La **modularización** divide un problema complejo en subproblemas más pequeños y manejables bajo el principio de "divide y vencerás".

#### Diferencias clave:
- **Función:** Es un subproceso que realiza cálculos y **retorna un valor** al punto desde donde fue invocado.
- **Procedimiento:** Es un subproceso que ejecuta una serie de acciones o tareas pero **no retorna un valor** directamente (suele realizar salidas por pantalla o modificaciones de estado).

#### Ejemplo de Función en PSeInt:
```text
Funcion resultado <- CalcularAreaTriangulo(base, altura)
    Definir resultado Como Real;
    resultado <- (base * altura) / 2;
FinFuncion
```
