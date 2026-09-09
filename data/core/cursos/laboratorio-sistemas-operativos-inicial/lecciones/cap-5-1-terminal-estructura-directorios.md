### La terminal

La **terminal** (o línea de comandos) permite operar el sistema escribiendo comandos. Es rápida, reproducible y esencial para administrar Debian. En el laboratorio convivirá con el escritorio gráfico XFCE.

### La estructura de directorios

En GNU/Linux todo cuelga de la raíz `/`. Los directorios principales son:

| Directorio | Contenido |
| :--- | :--- |
| `/home` | Las carpetas de los usuarios |
| `/etc` | Archivos de configuración del sistema |
| `/var` | Datos variables (logs, colas de impresión) |
| `/tmp` | Archivos temporales |
| `/usr` | Programas y bibliotecas del sistema |
| `/bin` y `/sbin` | Comandos esenciales del sistema |

### Primeros comandos

| Comando | Acción |
| :--- | :--- |
| `pwd` | Muestra el directorio actual |
| `whoami` | Muestra el usuario actual |
| `ls` | Lista el contenido del directorio |
| `cd <directorio>` | Cambia de directorio |
| `man <comando>` | Muestra la ayuda de un comando |

### La estructura de rutas

```text
/home/agustin  ->  ruta absoluta (desde la raíz)
./documentos   ->  relativa al directorio actual
../            ->  el directorio padre
~              ->  la carpeta personal del usuario
```

### La ayuda del sistema

Casi todo comando tiene documentación:

```bash
man ls
```

Se navega con las flechas y se sale con `q`. La ayuda en línea es una de las **herramientas de diagnóstico y aprendizaje** que brinda el sistema.

### Micro-desafío práctico

> Abrí la terminal y explorá: ejecutá `pwd`, `whoami` y `ls`. Movete a `/etc` con `cd /etc`, listá su contenido y volvé a tu carpeta con `cd ~`. Consultá la ayuda de `ls` con `man ls` y anotá tres opciones que no conocías.

### Resumen

- La terminal opera el sistema escribiendo comandos.
- La estructura de directorios cuelga de la raíz `/`.
- Comandos básicos: `pwd`, `ls`, `cd`, `whoami`.
- `man` brinda la documentación de cada comando.
