### Parámetros de instalación

Una instalación no es única: se configuran **parámetros** según la máquina y el entorno de aplicaciones. Elegirlos bien marca la diferencia entre un sistema estable y uno con problemas.

### Parámetros principales de instalación

| Parámetro | Decisión |
| :--- | :--- |
| Arquitectura | amd64, i386, arm64 según el procesador |
| Particionado | Tamaño y layout de las particiones |
| Selección de software | Escritorio, servidor, utilidades |
| Nombre del equipo | Hostname según el rol |
| Zona horaria | Ajuste del reloj del sistema |
| Espejos (mirrors) | Servidores de paquetes a usar |
| Red | DHCP o IP fija |

### Configuración según el rol de la máquina

- **Equipo de escritorio:** escritorio XFCE, utilidades de usuario, bajo consumo.
- **Servidor:** sin escritorio, con servicios (SSH, web, bases de datos).
- **Equipo de laboratorio:** herramientas de diagnóstico y red.

Para un servidor mínimo se instala sin escritorio:

```bash
# Después de la instalación, quitar el escritorio si no se necesita
sudo apt remove task-xfce-desktop
```

### Kernel y parámetros de arranque

Los **parámetros del kernel** se pasan en el arranque por GRUB. Ejemplos:

```text
quiet splash          # arranque sin mensajes detallados
nomodeset             # desactiva el modo de video automático
```

Se editan en `/etc/default/grub`:

```bash
sudo nano /etc/default/grub
sudo update-grub
```

### Configuración según la máquina

- **Poca memoria:** agregar swap y evitar escritorios pesados.
- **Discos SSD:** activar `discard` (TRIM) en el montaje.
- **Máquinas virtuales:** instalar los "guest additions" correspondientes.

### Micro-desafío práctico

> Revisá los parámetros actuales con `cat /proc/cmdline` y anotá qué opciones se pasaron al núcleo. Consultá `/etc/default/grub` y explicá qué hacen `GRUB_DEFAULT` y `GRUB_TIMEOUT`. Determiná qué parámetros elegirías para una instalación de escritorio en un equipo con 2 GB de RAM.

### Resumen

- La instalación se configura con parámetros según la máquina.
- El rol define el software: escritorio, servidor o laboratorio.
- Los parámetros del kernel se ajustan en `/etc/default/grub`.
- La elección de particionado, swap y software afecta la estabilidad.
