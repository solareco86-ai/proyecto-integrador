### Operadores aritméticos

Se usan para realizar cálculos:

| Operador | Operación | Ejemplo | Resultado |
| :--- | :--- | :--- | :--- |
| `+` | Suma | `3 + 2` | `5` |
| `-` | Resta | `3 - 2` | `1` |
| `*` | Multiplicación | `3 * 2` | `6` |
| `/` | División | `7 / 2` | `3.5` |
| `//` | División entera | `7 // 2` | `3` |
| `%` | Módulo (resto) | `7 % 2` | `1` |
| `**` | Potencia | `2 ** 3` | `8` |

### Operadores relacionales

Comparan valores y devuelven `True` o `False`:

| Operador | Significado | Ejemplo |
| :--- | :--- | :--- |
| `==` | Igual a | `3 == 3` → True |
| `!=` | Distinto de | `3 != 4` → True |
| `>` | Mayor que | `5 > 3` → True |
| `<` | Menor que | `5 < 3` → False |
| `>=` | Mayor o igual | `5 >= 5` → True |
| `<=` | Menor o igual | `4 <= 3` → False |

> ¡Ojo! `==` compara y `=` asigna. Son operadores distintos.

### Operadores lógicos

Combinan condiciones booleanas:

| Operador | Lógica | Ejemplo |
| :--- | :--- | :--- |
| `and` | Ambas verdaderas | `True and False` → False |
| `or` | Al menos una verdadera | `True or False` → True |
| `not` | Negación | `not True` → False |

```python
tiene_bolitas = True
esta_apaciguado = False

if tiene_bolitas and not esta_apaciguado:
    print("Pac-Man puede seguir comiendo")
```

### Prioridad de operadores

1. `**` (potencia)
2. `*`, `/`, `//`, `%`
3. `+`, `-`
4. Relacionales (`==`, `!=`, `<`, `>`, ...)
5. Lógicos: `not`, luego `and`, luego `or`

Se pueden usar paréntesis para aclarar y forzar el orden:

```python
resultado = (3 + 2) * 4   # 20
```

### Micro-desafío práctico

> Escribí un programa que pida un número y muestre si es par (usando `%`), si es mayor a 10 y si es positivo, combinando operadores relacionales y lógicos.

### Resumen

- Los operadores aritméticos cubren sumar, restar, multiplicar, dividir, módulo y potencia.
- Los relacionales comparan y devuelven True/False.
- Los lógicos `and`, `or`, `not` combinan condiciones.
- `==` compara, `=` asigna.
- Respeta la prioridad de operadores; usá paréntesis para aclarar.
