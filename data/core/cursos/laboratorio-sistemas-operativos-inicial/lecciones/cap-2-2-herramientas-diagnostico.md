### Herramientas de diagnóstico del sistema

El sistema operativo ofrece herramientas para **diagnosticar** su estado: espacio en disco, memoria, procesos y servicios. Conocerlas ayuda a detectar problemas antes de que se vuelvan críticos.

### Diagnóstico del almacenamiento: `df`

`df` muestra el espacio de los sistemas de archivos montados.

```bash
df -h
```

La opción `-h` muestra los valores en formato legible (GB, MB).

### Diagnóstico de la memoria: `free`

`free` informa el uso de la memoria RAM y del espacio de intercambio (swap).

```bash
free -h
```

| Columna | Significado |
| :--- | :--- |
| total | Memoria total disponible |
| used | Memoria en uso |
| free | Memoria libre |
| available | Memoria disponible para nuevas aplicaciones |

### Diagnóstico de procesos: `top`

`top` muestra en tiempo real los procesos que más consumen CPU y memoria.

```bash
top
```

Dentro de `top` podés presionar `q` para salir. Las columnas principales son:

- **PID:** identificador del proceso.
- **%CPU:** porcentaje de CPU que usa.
- **%MEM:** porcentaje de memoria que usa.

### Diagnóstico de servicios: `systemctl`

Para conocer el estado de los servicios gestionados por systemd:

```bash
systemctl list-units --type=service
systemctl status <servicio>
```

### Comparación rápida

| Herramienta | ¿Qué diagnostica? |
| :--- | :--- |
| `df` | Espacio en disco |
| `free` | Memoria RAM y swap |
| `top` | Procesos y consumo en vivo |
| `systemctl` | Estado de los servicios |

### Micro-desafío práctico

> Ejecutá `df -h`, `free -h` y `top` en tu Debian. Anotá: cuánto espacio libre hay en la partición raíz, cuánta memoria libre y disponible tenés, y cuál es el proceso que más CPU consume en ese momento.

### Resumen

- `df` diagnostica el espacio en disco.
- `free` muestra el uso de la memoria RAM.
- `top` lista los procesos que más recursos consumen.
- `systemctl` permite revisar el estado de los servicios.
