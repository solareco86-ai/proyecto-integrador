### Operadores estándares en diagramas de flujo

Los **operadores** se utilizan para operaciones aritméticas y relaciones condicionales dentro de los diagramas. La siguiente es una lista de los símbolos más comunes usados al diagramar programas de microcontroladores:

| Operador | Propósito |
| :--- | :--- |
| `*` | Multiplicación |
| `+` | Suma |
| `-` | Resta |
| `/` | División |
| `=` o `eq` | Igualdad |
| `>` o `gt` | Mayor que |
| `>=` o `ge` | Mayor o igual que |
| `<` o `lt` | Menor que |
| `<=` o `le` | Menor o igual que |
| `<>` o `ne` | No igual a |
| `Low` | Byte bajo |
| `High` | Byte alto |
| `Mod` | Módulo (resto de la división) |
| `&` | AND (lógico) |
| `^` | EXOR (o exclusivo) |
| `\|` | OR (lógico) |
| `Not` | Complemento (negación) |
| `<<` o `shl` | Corrimiento a la izquierda |
| `>>` o `shr` | Corrimiento a la derecha |
| `Rol` | Rotación a la izquierda |
| `Ror` | Rotación a la derecha |

### Ejemplo: suma de los 20 primeros números naturales

> **Consigna:** desarrollar el diagrama de flujo que calcule la suma de los 20 primeros números naturales.

La lógica en pasos:

1. **Inicio**
2. Definir las variables `Suma` y `Num` como enteros.
3. Inicializar `Suma = 0`.
4. Inicializar `Num = 0`.
5. Incrementar `Num = Num + 1`.
6. Sumar: `Suma = Suma + Num`.
7. **Decisión:** ¿`Num <= 20`?
   - Si → volver al paso 5 (incrementar y seguir sumando).
   - No → pasar a Fin.
8. **Fin**

Representado con los símbolos:

```
        ( Inicio )
             |
             v
   [ Definir Suma, Num entero ]
             |
             v
        [ Suma = 0 ]
             |
             v
        [ Num = 0 ]
             |
             v
      [ Num = Num + 1 ]
             |
             v
   [ Suma = Suma + Num ]
             |
             v
       < Num <= 20 ? > -------- SI ------> (vuelve a Num = Num + 1)
             |
            NO
             |
             v
         ( Fin )
```

### Traducción a MicroPython

Esa misma lógica, cuando ya está claro el algoritmo, se codifica:

```python
suma = 0
num = 0
while num <= 20:
    num = num + 1
    suma = suma + num
print("La suma de los 20 primeros naturales es:", suma)
```

### Micro-desafío práctico

> Diseñá el diagrama de flujo (y luego el programa) que lea 10 números y muestre cuántos son positivos y cuántos negativos. Usá un bucle y un contador.

### Resumen

- Los operadores del diagrama cubren aritmética, comparación y lógica.
- `Mod`, `Low`, `High`, corrimientos y rotaciones son típicos de la programación de microcontroladores.
- El ejemplo de la suma de los 20 naturales combina inicialización, bucle y decisión.
- Una vez validado el diagrama, la traducción a código es directa.
