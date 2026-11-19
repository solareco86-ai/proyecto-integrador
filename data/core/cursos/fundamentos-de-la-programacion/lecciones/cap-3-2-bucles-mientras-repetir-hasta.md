### 3.2 Bucles Mientras y Repetir Hasta

Cuando la cantidad de repeticiones depende de una condición dinámica (como la validación de una entrada del usuario), se utilizan los ciclos condicionales.

#### Bucle Mientras (`While`)
Evalúa la condición **antes** de ingresar al bloque. Si la condición es falsa inicialmente, el ciclo no se ejecuta ninguna vez:
```text
Mientras respuesta <> "S" Y respuesta <> "N" Hacer
    Escribir "¿Desea continuar? (S/N):";
    Leer respuesta;
FinMientras
```

#### Bucle Repetir / Hasta Que (`Do-While`)
Ejecuta el bloque **al menos una vez** y evalúa la condición de corte al final:
```text
Repetir
    Escribir "Ingrese una nota válida (1 a 10):";
    Leer nota;
Hasta Que nota >= 1 Y nota <= 10;
```
