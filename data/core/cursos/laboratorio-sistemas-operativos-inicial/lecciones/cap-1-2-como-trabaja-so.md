### Cómo trabaja el sistema operativo

En la lección anterior vimos qué hace el sistema operativo. Ahora veamos **cómo lo hace**: el ciclo de arranque, los componentes que intervienen y la relación entre el kernel, los servicios y las aplicaciones.

### El ciclo de vida del sistema

```text
Encendido  ->  BIOS/UEFI  ->  Gestor de arranque (GRUB)  ->  Kernel  ->  Servicios (systemd)  ->  Escritorio XFCE
```

1. Al encender, la **BIOS o UEFI** revisa el hardware y busca el disco de arranque.
2. El **gestor de arranque (GRUB)** ofrece el menú para elegir el sistema o núcleo.
3. El **kernel** se carga y detecta los dispositivos.
4. **systemd** inicia los servicios y procesos del sistema.
5. El **escritorio XFCE** presenta la interface al usuario.

### El kernel: el administrador central

El kernel organiza el trabajo en dos modos:

| Modo | Quién lo usa | Qué puede hacer |
| :--- | :--- | :--- |
| Modo núcleo | El propio kernel | Acceso total al hardware y a la memoria |
| Modo usuario | Aplicaciones | Solo servicios que el kernel le permite |

Por eso una aplicación "no puede romper" al sistema: si falla, se termina el programa, pero el kernel sigue funcionando.

### Los servicios (daemons)

Muchas tareas ocurren "en segundo plano" mientras usamos la computadora. Estos programas se llaman **servicios** o *daemons* y los gestiona **systemd**:

| Comando | Para qué sirve |
| :--- | :--- |
| `systemctl status` | Ver el estado de los servicios |
| `systemctl start <servicio>` | Iniciar un servicio |
| `systemctl stop <servicio>` | Detener un servicio |
| `systemctl enable <servicio>` | Que se inicie al arrancar |

### Las aplicaciones y el escritorio

Sobre el kernel y los servicios se apoyan las aplicaciones. El **entorno de escritorio** (XFCE) no es parte del kernel: es un conjunto de programas (panel, ventanas, menú) que dan la interface gráfica.

### Micro-desafío práctico

> Ejecutá `systemctl status` y observá la lista de servicios activos. Luego probá `systemctl status ssh` (o `systemctl status networking` si ssh no está instalado) y anotá el estado del servicio: *active*, *inactive* o *failed*.

### Resumen

- El sistema arranca en etapas: BIOS/UEFI, GRUB, kernel, systemd y escritorio.
- El kernel trabaja en modo núcleo; las aplicaciones, en modo usuario.
- Los servicios en segundo plano los administra systemd.
- El escritorio XFCE es la interface gráfica sobre el sistema.
