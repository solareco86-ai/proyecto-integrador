### 2.2 Estructura Condicional Anidada y Múltiple

Cuando un problema presenta más de dos escenarios posibles, se emplean estructuras condicionales anidadas o de selección múltiple.

#### Condicional Anidado
Un bloque condicional dentro de la rama verdadera o falsa de otro condicional:
```text
Si promedio >= 7 Entonces
    Escribir "Promocionado";
SiNo
    Si promedio >= 4 Entonces
        Escribir "Regularizado";
    SiNo
        Escribir "Desaprobado";
    FinSi
FinSi
```

#### Estructura Múltiple (`Segun / Hacer`)
Evalúa el valor de una variable contra múltiples casos discretos:
```text
Segun opcion Hacer
    1: Escribir "Operación: Cargar Alumno";
    2: Escribir "Operación: Listar Notas";
    3: Escribir "Operación: Salir";
    De Otro Modo:
        Escribir "Opción inválida";
FinSegun
```
