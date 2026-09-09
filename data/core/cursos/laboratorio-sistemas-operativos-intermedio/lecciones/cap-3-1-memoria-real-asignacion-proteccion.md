### La memoria real

La **memoria real (RAM)** es el espacio donde se cargan los programas y sus datos mientras se ejecutan. El sistema operativo la **asigna, administra y protege** para que los programas no interfieran entre sí.

### Organización de la memoria

```text
+------------------------+
|  Programa A            |
+------------------------+
|  Programa B            |
+------------------------+
|  Núcleo y sistema      |
+------------------------+
```

Cada programa recibe un espacio propio; el núcleo reserva el suyo y protege ambos.

### Funciones de la administración de memoria

| Función | Qué hace |
| :--- | :--- |
| Asignación | Reparte la RAM entre los programas |
| Reasignación | Libera memoria cuando un programa termina |
| Protección | Evita que un programa lea o escriba en la memoria de otro |
| Compartición | Permite compartir código entre programas cuando es seguro |

### Herramientas de diagnóstico de memoria

| Comando | Qué muestra |
| :--- | :--- |
| `free -h` | Memoria total, usada, libre y disponible |
| `vmstat` | Estadísticas de memoria y CPU |
| `top` / `htop` | Consumo de memoria por proceso |
| `cat /proc/meminfo` | Detalle completo de la memoria |

### Ver el consumo por proceso

```bash
top
```

La columna `%MEM` indica cuánta RAM usa cada proceso. Con `M` en `top` se ordena por uso de memoria.

### Programas residentes

Algunos programas quedan **residentes** en memoria, es decir, se cargan y permanecen disponibles. En Debian se llaman *daemons* o servicios y los gestiona systemd.

```bash
systemctl list-units --type=service
```

### Micro-desafío práctico

> Ejecutá `free -h` y anotá los valores de memoria total, usada y disponible. Luego `vmstat 2 5` para ver 5 muestras cada 2 segundos y observá la columna de memoria libre. Usá `top` y ordená por consumo de memoria con `M`. Identificá el proceso que más RAM usa.

### Resumen

- La RAM se asigna, administra y protege por el sistema operativo.
- Cada programa tiene su espacio; el núcleo protege el propio.
- `free`, `vmstat`, `top` y `/proc/meminfo` diagnostican la memoria.
- Los servicios residentes quedan disponibles en memoria.
