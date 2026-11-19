### 3.1 Bucle Para / For

El ciclo **Para** (`For`) se utiliza cuando la cantidad de iteraciones es conocida antes de comenzar la repetición.

#### Componentes del bucle:
- **Variable de control:** Variable entera que actúa como contador.
- **Valor inicial y final:** Límites del recorrido.
- **Paso (incremento o decremento):** Valor sumado o restado en cada ciclo (por defecto `1`).

#### Ejemplo en PSeInt:
```text
Definir i, suma Como Entero;
suma <- 0;

Para i <- 1 Hasta 10 Con Paso 1 Hacer
    suma <- suma + i;
FinPara

Escribir "La suma de los primeros 10 números es: ", suma;
```
