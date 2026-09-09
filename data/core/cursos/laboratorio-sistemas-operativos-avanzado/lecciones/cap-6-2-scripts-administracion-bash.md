### Scripts de administración

Un **script** es un archivo de texto con comandos que se ejecutan de forma automática. En la administración del sistema, los scripts **automatizan tareas repetitivas** y reducen errores.

### Estructura de un script bash

```bash
#!/bin/bash
# Script: respaldo.sh
# Descripción: copia de respaldo de la carpeta del laboratorio

fecha=$(date +%Y%m%d)
origen="/home/agustin/laboratorio"
destino="/home/agustin/respaldos"

mkdir -p "$destino"
cp -r "$origen" "$destino/respaldo-$fecha"
echo "Respaldo completado en $destino/respaldo-$fecha"
```

La primera línea (`#!/bin/bash`) indica el intérprete. Los comentarios empiezan con `#`.

### Crear y ejecutar un script

```bash
# Crear el archivo
nano respaldo.sh

# Darle permiso de ejecución
chmod +x respaldo.sh

# Ejecutarlo
./respaldo.sh
```

### Variables y comandos comunes

```bash
#!/bin/bash
usuario=$(whoami)
fecha=$(date)
echo "Usuario: $usuario"
echo "Fecha: $fecha"
```

### Automatizar tareas

Los scripts se pueden programar para que corran solos:

**Con `cron`:**

```text
# crontab -e  ->  agenda de tareas
30 2 * * * /home/agustin/respaldo.sh
```

El ejemplo ejecuta el respaldo todos los días a las 2:30.

**Con `systemd` timers:**

```bash
# Crear un timer con systemctl (alternativa moderna a cron)
```

### Buenas prácticas

1. **Probar** el script paso a paso antes de automatizarlo.
2. Usar **variables** y rutas absolutas.
3. **Verificar** los comandos que requieren permisos (`sudo`).
4. **Registrar** la salida en un log.

```bash
# Redirigir la salida del script a un log
./respaldo.sh >> respaldo.log 2>&1
```

### Micro-desafío práctico

> Escribí un script `info.sh` que muestre el usuario, la fecha, el espacio libre (`df -h /`) y la memoria (`free -h`). Dale permiso de ejecución con `chmod +x` y ejecutalo. Luego agregalo a `cron` para que corra una vez al día y verificá que la salida quede en un archivo de log.

### Resumen

- Un script automatiza comandos en un archivo ejecutable.
- Los scripts se crean con texto, se marcan con `chmod +x` y se ejecutan.
- `cron` y los timers de systemd programan su ejecución.
- Probar, usar variables y registrar la salida son buenas prácticas.
