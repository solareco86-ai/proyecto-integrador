### Preparación antes de instalar

Antes de instalar Debian con XFCE hay que verificar **requisitos de hardware** y preparar el **medio de instalación**. Una buena preparación evita errores durante el proceso.

### Requisitos mínimos recomendados

| Componente | Mínimo recomendado |
| :--- | :--- |
| Procesador | 64 bits (amd64) |
| Memoria RAM | 2 GB |
| Disco | 20 GB libres |
| Medio de instalación | Pendrive USB o DVD |
| Conectividad | Conexión a Internet (opcional pero recomendada) |

### BIOS/UEFI y arranque desde el medio

La BIOS o UEFI es el primer software que corre al encender. Para arrancar desde el pendrive:

1. Reiniciar la máquina y entrar a la configuración (tecla `F2`, `Del` o `F10` según el equipo).
2. Ubicar la opción de **orden de arranque (Boot Order)**.
3. Poner el medio USB como primer dispositivo.
4. Si el sistema usa UEFI, puede requerirse **Secure Boot** desactivado.

### Particionado básico

El disco se divide en **particiones** que el sistema usa para organizar los datos. En una instalación sencilla alcanza con:

| Partición | Tamaño sugerido | Punto de montaje |
| :--- | :--- | :--- |
| Raíz (`/`) | Resto del disco | `/` |
| Intercambio (swap) | 2-4 GB | `swap` |

> El instalador de Debian ofrece la opción *"Guiado - utilizar todo el disco"* que crea las particiones automáticamente, ideal para comenzar.

### Obtención de la imagen ISO

La imagen de instalación se descarga desde el sitio oficial de Debian. Para este curso conviene elegir una imagen que incluya el escritorio XFCE o la edición en vivo, y grabarla en el pendrive.

```bash
# Ejemplo: grabar la ISO en un pendrive (reemplazar /dev/sdX por el dispositivo correcto)
sudo dd if=debian-xfce.iso of=/dev/sdX bs=4M status=progress
```

### Micro-desafío práctico

> En tu equipo de laboratorio, verificá los requisitos: anotá la cantidad de RAM (con `free -h`), el espacio libre del disco (con `df -h`) y la arquitectura del procesador (con `uname -m`). Determiná si cumple los mínimos para instalar Debian con XFCE.

### Resumen

- Verificá requisitos de hardware antes de instalar.
- La BIOS/UEFI controla el arranque desde el medio de instalación.
- El particionado guiado simplifica la instalación inicial.
- La ISO oficial de Debian incluye la opción de escritorio XFCE.
