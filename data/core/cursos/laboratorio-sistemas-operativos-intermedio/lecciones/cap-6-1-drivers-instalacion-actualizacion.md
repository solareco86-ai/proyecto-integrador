### Los controladores (drivers)

Un **controlador (driver)** es el software que permite que el sistema operativo se comunique con un dispositivo de hardware. Sin el driver correcto, la impresora, la placa de red o la tarjeta gráfica no funcionan.

### ¿Qué es un driver?

```text
Aplicación -> sistema operativo -> driver -> dispositivo
```

El driver traduce las órdenes generales del sistema al **lenguaje específico del dispositivo**.

### Drivers en Debian

Muchos drivers ya vienen en el núcleo (módulos). Otros se instalan como paquetes:

```bash
# Instalar el driver de una impresora (ejemplo HP)
sudo apt install hplip

# Drivers de impresoras varias
sudo apt install printer-driver-gutenprint
```

### Drivers instalados

```bash
# Módulos del núcleo cargados (drivers activos)
lsmod

# Dispositivos USB conectados
lsusb

# Dispositivos PCI conectados
lspci
```

### Instalación y actualización de drivers

```bash
# Actualizar todos los paquetes (incluye drivers)
sudo apt update
sudo apt upgrade
```

Para dispositivos propietarios (por ejemplo algunas tarjetas gráficas o de WiFi), Debian ofrece los paquetes `firmware-*`:

```bash
sudo apt install firmware-linux
```

### Cómo el driver se comunica con el dispositivo

CUPS usa un sistema de **filtros** que convierten el documento al lenguaje de la impresora (PostScript, PCL, etc.). Cada impresora tiene su propia descripción (PPD).

```bash
# Listar los controladores y filtros disponibles
lpinfo -m
```

### Micro-desafío práctico

> Ejecutá `lsusb` y `lspci` y anotá qué dispositivos detecta tu equipo. Consultá `lpinfo -m` y anotá tres controladores de impresora disponibles. Verificá si `hplip` está instalado con `dpkg -l | grep hplip`.

### Resumen

- El driver es el software que comunica al sistema con el hardware.
- En Debian muchos drivers son módulos del núcleo o paquetes.
- `lsmod`, `lsusb` y `lspci` muestran los dispositivos y drivers.
- Los drivers se actualizan junto con el sistema con `apt upgrade`.
