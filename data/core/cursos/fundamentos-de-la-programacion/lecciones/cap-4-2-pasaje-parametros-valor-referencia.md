### 4.2 Pasaje de Parámetros por valor y referencia

Los parámetros permiten enviar información entre el programa principal y los subprocesos.

#### Modos de pasaje de parámetros:
1. **Por Valor:**
   - Se envía una **copia** del dato almacenado en la variable.
   - Cualquier modificación realizada dentro del subproceso **no altera** la variable original del llamador.
   - Es el comportamiento por defecto para tipos simples en la mayoría de los entornos.

2. **Por Referencia:**
   - Se envía la **dirección de memoria** o referencia a la variable original.
   - Cualquier modificación efectuada dentro del subproceso **afecta directamente** a la variable externa.
   - Se utiliza cuando un procedimiento debe retornar múltiples valores o actualizar el estado de una estructura.

#### Sintaxis en PSeInt:
```text
SubProceso Intercambiar(a Por Referencia, b Por Referencia)
    Definir aux Como Entero;
    aux <- a;
    a <- b;
    b <- aux;
FinSubProceso
```
