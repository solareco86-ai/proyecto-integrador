### El panel de control y la configuración

El **panel de control** reúne las herramientas de configuración del sistema. En el nivel Inicial lo usamos de forma visual; ahora lo profundizamos desde la terminal y entendemos **cómo se guarda cada configuración**.

### Herramientas del panel

| Herramienta | Configuración |
| :--- | :--- |
| Administrador de usuarios | Crear y administrar cuentas |
| Impresoras | Agregar y configurar impresoras |
| Red | Interfaces y conexiones |
| Fecha y hora | Hora del sistema y zona horaria |
| Energía | Ahorro y suspensión |
| Apariencia | Temas, iconos y tipografías |

### Configuración desde la terminal

Muchas opciones del panel son la interfaz gráfica de archivos de configuración:

| Configuración | Archivo o comando |
| :--- | :--- |
| Usuarios | `/etc/passwd`, `passwd`, `useradd` |
| Impresoras | `lpadmin`, `lpstat` |
| Red | `ip`, `nmcli` |
| Fecha y hora | `timedatectl` |
| Servicios | `systemctl` |

```bash
# Fecha y hora
timedatectl

# Configuración de red
nmcli device status

# Administrar usuarios
sudo useradd laboratorio
```

### Cambiar configuraciones desde la terminal

```bash
# Agregar un usuario
sudo adduser laboratorio

# Darle permisos de administración
sudo usermod -aG sudo laboratorio

# Cambiar la zona horaria
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
```

### Verificar los cambios

```bash
# Ver los usuarios del sistema
cat /etc/passwd | cut -d: -f1

# Ver los grupos del usuario
groups laboratorio
```

### Micro-desafío práctico

> Creá un usuario `laboratorio` con `sudo adduser laboratorio` y agregalo al grupo `sudo`. Verificá con `groups laboratorio`. Consultá la hora del sistema con `timedatectl` y revisá el estado de las impresoras con `lpstat -t`. Anotá qué archivo y qué comando cambia cada configuración.

### Resumen

- El panel de control es la interface gráfica de la configuración.
- Cada ajuste del panel tiene su equivalente en la terminal.
- `timedatectl`, `nmcli`, `useradd` y `systemctl` configuran el sistema.
- Verificar con `groups` y `lpstat` confirma los cambios.
