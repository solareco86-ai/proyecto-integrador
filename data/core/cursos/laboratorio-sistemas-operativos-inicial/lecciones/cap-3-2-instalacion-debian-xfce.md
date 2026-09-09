### Instalación de Debian con XFCE paso a paso

En esta lección recorremos las etapas del instalador de Debian. El objetivo es que la **primera instalación** se realice sin sorpresas y conociendo qué se está configurando en cada paso.

### Etapas del instalador

```text
Idioma -> Ubicación -> Teclado -> Red -> Usuarios -> Particionado -> Selección de software -> Instalación -> Grub
```

### Paso a paso

**1. Idioma, ubicación y teclado**

Se eligen los idiomas del sistema y del teclado. Para el laboratorio: *Español (Argentina)*.

**2. Configuración de red**

El instalador detecta la red. Si hay DHCP activo, tomará dirección automáticamente. Se asigna luego el nombre del equipo (*hostname*), por ejemplo `lab-so-01`.

**3. Cuentas de usuario**

- Se define la contraseña de **root** (administrador).
- Se crea un **usuario normal** para el trabajo diario, que usará `sudo` para tareas administrativas.

**4. Particionado**

Se elige *"Guiado - utilizar todo el disco"* y se confirma. El instalador crea las particiones automáticamente.

**5. Selección de software**

En esta pantalla se marcan los componentes a instalar:

| Opción | ¿Para qué sirve? |
| :--- | :--- |
| Escritorio XFCE | La interface gráfica del curso |
| Utilidades del sistema | Herramientas de administración |
| Servidor SSH | Acceso remoto al equipo |
| Entorno Debian estándar | Utilidades base del sistema |

> Para este curso marcá al menos **Escritorio XFCE** y **Utilidades del sistema**.

**6. Instalación y gestor de arranque**

El instalador copia los paquetes y, al final, instala **GRUB** en el disco. Sin esto el sistema no podría arrancar.

### Primer reinicio

Al finalizar, se quita el medio de instalación y se reinicia. Si todo salió bien, GRUB presentará el menú y luego aparecerá la pantalla de acceso al escritorio XFCE.

### Micro-desafío práctico

> Realizá la instalación de Debian con XFCE en tu equipo de laboratorio (o en una máquina virtual). Anotá en tu cuaderno las decisiones tomadas en cada paso: idioma, hostname, usuario, tipo de particionado y opciones de software elegidas.

### Resumen

- El instalador guía por etapas: idioma, red, usuarios, particiones y software.
- El usuario normal con `sudo` es la forma segura de administrar el sistema.
- La selección de software incluye el escritorio XFCE.
- GRUB se instala al final para permitir el arranque.
