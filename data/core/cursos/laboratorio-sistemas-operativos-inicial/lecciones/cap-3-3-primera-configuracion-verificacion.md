### Primera configuración y verificación

Una vez instalado Debian con XFCE, conviene hacer una **primera configuración** y **verificar** que el sistema quedó sano. Esto incluye actualizar los paquetes, comprobar la conexión y revisar los datos básicos del sistema.

### Actualización inicial

Lo primero es actualizar la lista de paquetes y aplicar las mejoras de seguridad:

```bash
sudo apt update
sudo apt upgrade
```

- `apt update`: actualiza la lista de paquetes disponibles.
- `apt upgrade`: actualiza los paquetes instalados a sus versiones nuevas.

### Verificación básica del sistema

```bash
# Nombre del sistema, kernel y arquitectura
uname -a

# Distribución instalada
cat /etc/os-release

# Espacio en disco
df -h

# Memoria RAM
free -h
```

### Verificación de la red

```bash
# Direcciones IP de las interfaces
ip addr

# Prueba de conectividad a un servidor de nombres
ping -c 4 debian.org
```

### Configuración de idioma y teclado (si hace falta)

Si el teclado no responde correctamente:

```bash
sudo dpkg-reconfigure keyboard-configuration
```

### Herramientas útiles para el laboratorio

Conviene instalar algunos paquetes que usaremos en el curso:

```bash
sudo apt install htop neofetch tree git curl
```

- `htop`: monitor interactivo de procesos.
- `neofetch`: resume el sistema con un vistazo.
- `tree`: muestra directorios en forma de árbol.
- `curl`: descarga y prueba conexiones web.

### Micro-desafío práctico

> Tras la instalación: actualizá el sistema con `apt update` y `apt upgrade`, instalá los paquetes del laboratorio y ejecutá `neofetch`. Copiá la salida en tu cuaderno y comparala con la de `uname -a`.

### Resumen

- Actualizá siempre el sistema tras instalarlo.
- Verificá sistema, disco, memoria y red con los comandos básicos.
- El idioma y teclado se reconfiguran con `dpkg-reconfigure`.
- Los paquetes del laboratorio facilitan el trabajo del curso.
