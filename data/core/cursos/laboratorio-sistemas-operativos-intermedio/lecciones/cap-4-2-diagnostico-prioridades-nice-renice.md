### Prioridades de ejecución

No todos los procesos son igual de importantes: el sistema asigna una **prioridad** que determina cuánta CPU recibe cada uno. En esta lección vemos cómo **recabar información** y **alterar** esas prioridades.

### El valor nice

En Linux, la prioridad se expresa con el **nice value**, que va de -20 (máxima prioridad) a 19 (mínima). Los valores **negativos** requieren permisos de administrador.

```text
nice -20                  nice 0                nice 19
alta prioridad         prioridad normal       baja prioridad
```

### Ver las prioridades

```bash
# Columnas NI (nice) y PR (prioridad)
ps -el
top
htop
```

En `top`, la columna `NI` muestra el nice value de cada proceso.

### Establecer prioridad al lanzar: `nice`

```bash
nice -n 10 ./programa        # ejecutar con prioridad baja
nice -n -5 ./programa        # ejecutar con prioridad alta (requiere sudo)
```

### Cambiar prioridad en ejecución: `renice`

```bash
renice 10 <PID>              # bajar la prioridad de un proceso
sudo renice -5 <PID>         # subir la prioridad de un proceso
```

### Efectos de alterar prioridades

- Un proceso con **prioridad alta** recibe más CPU y termina antes, pero puede **frenar** al resto.
- Un proceso con **prioridad baja** cede CPU a los demás; ideal para tareas en segundo plano.

> Subir demasiado la prioridad de varios procesos degrada la respuesta del sistema. Es una herramienta para equilibrar, no para abusar.

### Terminar procesos

Para finalizar un proceso problemático:

```bash
kill <PID>          # pedir terminación normal
kill -9 <PID>       # terminación forzosa (último recurso)
pkill <nombre>      # terminar por nombre
```

### Micro-desafío práctico

> Ejecutá `sleep 300 &` y anotá su PID. Listá los procesos con `ps -el` y observá su columna `NI`. Con `renice 15 <PID>` bajá su prioridad y verificá el cambio. Luego terminá el proceso con `kill <PID>`.

### Resumen

- La prioridad (nice) va de -20 a 19.
- `nice` define la prioridad al lanzar; `renice` la cambia en ejecución.
- Alterar prioridades afecta el reparto de CPU entre procesos.
- `ps`, `top` y `htop` recaban la información de prioridades.
