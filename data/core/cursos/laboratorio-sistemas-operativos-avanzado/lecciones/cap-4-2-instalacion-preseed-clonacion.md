### Instalación no interactiva (preseed)

Cuando hay que instalar muchas máquinas iguales, la instalación manual no es práctica. La **instalación preseed** automatiza el proceso: un archivo responde las preguntas del instalador sin intervención.

### ¿Qué es preseed?

El **archivo preseed** es un texto que define las respuestas a las preguntas del instalador: idioma, teclado, particiones, usuarios y software. Permite instalaciones **repetibles y estandarizadas**.

### Estructura de un archivo preseed

```text
d-i debian-installer/locale string es_AR.UTF-8
d-i keyboard-configuration/xkb-keymap select es
d-i netcfg/choose_interface select auto
d-i netcfg/hostname string lab-so-01

d-i passwd/root-password password Secreto123!
d-i passwd/root-password-again password Secreto123!

d-i partman-auto/method string regular
d-i partman-auto/choose_recipe select atomic

tasksel tasksel/first multiselect standard, xfce-desktop
d-i grub-installer/only_debian boolean true
```

### Usar el archivo preseed

```bash
# Cargar el preseed desde un servidor web
linux /install.amd/vmlinuz auto url=http://192.168.1.10/preseed.cfg
```

O desde un pendrive: se agrega la opción en el menú de GRUB del instalador.

### Beneficios

| Beneficio | Descripción |
| :--- | :--- |
| Repetibilidad | Todas las máquinas quedan iguales |
| Ahorro de tiempo | Sin responder preguntas a mano |
| Menos errores | Sin variaciones por distracción |
| Escalabilidad | Instalación en muchos equipos a la vez |

### Clonación

Otra técnica para muchas máquinas es **clonar** un disco ya configurado:

```bash
# Copiar un disco entero a otro (ejemplo)
sudo dd if=/dev/sda of=/dev/sdb bs=4M status=progress
```

> La clonación es útil pero hereda el hostname y los datos del equipo original; hay que reconfigurarlos luego.

### Micro-desafío práctico

> Escribí un archivo preseed mínimo para un equipo de laboratorio: hostname `lab-so-XX`, un usuario con sudo, particionado automático y el escritorio XFCE. Explicá qué línea responde cada etapa del instalador y en qué situaciones conviene preseed frente a instalación manual.

### Resumen

- Preseed automatiza la instalación respondiendo las preguntas por adelantado.
- El archivo define idioma, red, particiones, usuarios y software.
- Permite instalaciones repetibles y a escala.
- La clonación con `dd` duplica discos ya configurados.
