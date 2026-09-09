### Gestión de archivos desde la terminal

Manejar archivos es una de las tareas centrales del sistema operativo. En esta lección vemos los comandos esenciales de **navegación y gestión de archivos**.

### Comandos de navegación y listado

| Comando | Acción |
| :--- | :--- |
| `ls` | Lista archivos y carpetas |
| `ls -l` | Lista con detalles (permisos, dueño, tamaño, fecha) |
| `ls -a` | Lista también los archivos ocultos |
| `cd <carpeta>` | Cambia de directorio |
| `pwd` | Muestra la ruta actual |

### Gestión de archivos y carpetas

| Comando | Acción |
| :--- | :--- |
| `mkdir <nombre>` | Crea una carpeta |
| `touch <archivo>` | Crea un archivo vacío o actualiza su fecha |
| `cp <origen> <destino>` | Copia archivos o carpetas |
| `mv <origen> <destino>` | Mueve o renombra |
| `rm <archivo>` | Elimina un archivo |
| `rmdir <carpeta>` | Elimina una carpeta vacía |
| `rm -r <carpeta>` | Elimina una carpeta y su contenido |
| `find <carpeta> -name <patrón>` | Busca archivos por nombre |

> Cuidado con `rm`: elimina sin pasar por la papelera. Revisá siempre la ruta antes de confirmar.

### Ejemplo de sesión

```bash
mkdir laboratorio
cd laboratorio
touch notas.txt
cp notas.txt copia-notas.txt
mv copia-notas.txt respaldo.txt
ls -l
find . -name "*.txt"
rm respaldo.txt
cd ..
```

### Buscar archivos con `find`

`find` es muy útil para localizar archivos:

```bash
find /home -name "*.conf"
find . -type d   # solo carpetas
find . -type f   # solo archivos
```

### Micro-desafío práctico

> Creá una estructura de carpetas para organizar tu laboratorio: `laboratorio/apuntes`, `laboratorio/practicas` y `laboratorio/respaldos`. Dentro de `practicas` creá un archivo `reporte.txt`, copialo a `respaldos` y renombralo como `reporte-01.txt`. Verificá el resultado con `ls -R laboratorio`.

### Resumen

- `ls`, `cd` y `pwd` navegan y listan el sistema de archivos.
- `mkdir`, `touch`, `cp`, `mv` y `rm` administran archivos y carpetas.
- `find` busca archivos por nombre, tipo o ruta.
- La gestión de archivos es una tarea central del SO.
