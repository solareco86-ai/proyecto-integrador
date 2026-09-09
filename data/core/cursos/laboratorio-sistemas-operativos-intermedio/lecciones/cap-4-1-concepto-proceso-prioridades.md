### El concepto de proceso

Un **proceso** es un programa en ejecución. Mientras un programa es el archivo en disco, el proceso es la instancia viva que usa memoria, CPU y archivos. El sistema operativo administra muchos procesos a la vez.

### Qué es un proceso

Cada proceso tiene:

| Dato | Descripción |
| :--- | :--- |
| PID | Identificador único del proceso |
| PPID | PID del proceso padre que lo creó |
| Usuario | Quién lo ejecuta |
| Prioridad | Importancia relativa en la CPU |
| Estado | En ejecución, dormido, detenido... |
| Recursos | Memoria, CPU y archivos que usa |

### Ver los procesos

```bash
ps                     # procesos de la sesión actual
ps -ef                 # todos los procesos del sistema
ps aux                 # con detalles de CPU y memoria
pstree                 # los procesos en forma de árbol
```

### Estados de un proceso

```text
Creado -> En ejecución (running) -> Dormido (sleeping)
                    |-> Detenido (stopped)
                    |-> Zombie (ha terminado, el padre no lo recogió)
```

### Recursos que utilizan los programas

Los procesos consumen:

- **CPU:** tiempo de procesamiento.
- **Memoria:** RAM y swap.
- **Archivos:** descriptores de archivos abiertos.
- **Red:** conexiones y puertos.

```bash
# Procesos que consumen más CPU y memoria
top

# Descriptores de archivos abiertos por un proceso
ls /proc/<PID>/fd
```

### Micro-desafío práctico

> Ejecutá `ps -ef` y anotá tres procesos con su PID y su usuario. Ejecutá `pstree` y explicá la relación padre-hijo entre procesos. Elegí un proceso (por ejemplo tu terminal) y listá sus archivos abiertos en `/proc/<PID>/fd`.

### Resumen

- Un proceso es un programa en ejecución con PID, prioridad y recursos.
- `ps`, `pstree` y `top` muestran los procesos del sistema.
- Los procesos consumen CPU, memoria, archivos y red.
- El sistema administra su creación, ejecución y terminación.
