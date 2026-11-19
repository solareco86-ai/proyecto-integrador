### 2.1 Estructura Condicional Simple y Doble

Las estructuras condicionales permiten evaluar una expresión booleana y ramificar la ejecución del programa.

#### Condicional Simple (`Si / Entonces`)
Ejecuta un bloque de instrucciones únicamente si la condición resulta verdadera:
```text
Si nota >= 4 Entonces
    Escribir "Cursada regularizada";
FinSi
```

#### Condicional Doble (`Si / Entonces / SiNo`)
Permite definir una vía alternativa cuando la condición es falsa:
```text
Si nota >= 7 Entonces
    Escribir "Materia promocionada";
SiNo
    Escribir "Debe rendir examen final";
FinSi
```
