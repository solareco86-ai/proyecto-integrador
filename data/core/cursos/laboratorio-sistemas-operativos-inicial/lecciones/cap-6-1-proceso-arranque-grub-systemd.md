### El proceso de arranque

El **arranque** es la secuencia que lleva al sistema desde el encendido hasta que aparece el escritorio. Conocerla ayuda a entender y diagnosticar fallas al iniciar.

### Etapas del arranque

```text
Encendido -> BIOS/UEFI -> GRUB -> Kernel -> systemd -> Escritorio XFCE
```

### 1. BIOS/UEFI

La BIOS o UEFI verifica el hardware (POST) y busca el gestor de arranque en el disco.

### 2. GRUB

**GRUB** es el gestor de arranque. Presenta el menú con las opciones:

- El sistema operativo Debian.
- Otras versiones del kernel instaladas.
- Entradas de recuperación (*recovery mode*).

Con GRUB se puede elegir con qué kernel arrancar, útil ante problemas.

### 3. El kernel

El kernel se carga en memoria, detecta los dispositivos y monta la raíz `/`. Los mensajes de esta etapa se revisan con:

```bash
dmesg
```

### 4. systemd

**systemd** es el sistema de inicio que lanza los servicios y procesos del sistema. Comandos de diagnóstico:

```bash
systemd-analyze             # tiempo de arranque por etapas
systemctl list-units --failed   # servicios que fallaron
```

### 5. El escritorio

El administrador de sesión arranca XFCE y presenta la pantalla de acceso.

### Micro-desafío práctico

> Reiniciá (o prendé) tu equipo y observá el menú de GRUB. Una vez en el sistema, ejecutá `systemd-analyze` y `systemctl list-units --failed`. Anotá cuánto tardó el arranque y si algún servicio falló. Si tenés varios kernels instalados, listalos con `ls /boot`.

### Resumen

- El arranque pasa por BIOS/UEFI, GRUB, kernel, systemd y el escritorio.
- GRUB permite elegir el sistema o kernel a cargar.
- `dmesg` muestra los mensajes del kernel.
- `systemd-analyze` y `systemctl` diagnostican el inicio.
