### La impresión en diferido

Imprimir es una tarea lenta comparada con el procesamiento. Para no frenar los programas, el sistema usa la **impresión en diferido**: el documento se envía a una **cola de impresión** y el programa sigue trabajando.

### El spool y la cola de impresión

```text
Aplicación -> spool (cola) -> impresora
```

El **spool** es el área donde se guardan los trabajos que esperan su turno. El programa que lo administra en Debian es **CUPS** (Common Unix Printing System).

### El programa administrador: CUPS

```bash
# Ver el estado del servicio
systemctl status cups

# Instalarlo si no está presente
sudo apt install cups
```

La configuración gráfica se accede desde el navegador:

```text
http://localhost:631
```

### Comandos que gobiernan la impresión

| Comando | Función |
| :--- | :--- |
| `lp <archivo>` | Envía un trabajo a la cola |
| `lpq` | Muestra la cola de impresión |
| `lprm <id>` | Cancela un trabajo de la cola |
| `lpstat -p` | Estado de las impresoras |
| `lpstat -t` | Información completa del sistema de impresión |

### Enviar un trabajo

```bash
# Imprimir un archivo de texto
lp documento.txt

# Elegir impresora y número de copias
lp -d impresora_1 -n 2 documento.txt

# Ver la cola
lpq
```

### Utilidad práctica de administrar la impresión

- Los usuarios pueden **encolar** trabajos y seguir trabajando.
- El administrador puede **pausar, reordenar o cancelar** trabajos.
- Se puede **diagnosticar** errores de impresora sin detener los programas.

### Micro-desafío práctico

> Instalá CUPS con `sudo apt install cups` y verificá el servicio con `systemctl status cups`. Creá un archivo de texto, enviá dos trabajos con `lp` y observá la cola con `lpq`. Cancelá uno de ellos con `lprm` y verificá la cola nuevamente.

### Resumen

- La impresión en diferido usa un spool que no detiene a los programas.
- CUPS es el administrador de impresión de Debian.
- `lp`, `lpq`, `lprm` y `lpstat` gobiernan la impresión.
- Administrar la cola permite pausar, reordenar y cancelar trabajos.
