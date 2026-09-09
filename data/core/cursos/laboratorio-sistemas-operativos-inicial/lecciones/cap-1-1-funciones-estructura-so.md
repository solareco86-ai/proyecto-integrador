### ¿Qué es un sistema operativo?

El **sistema operativo (SO)** es el software principal que administra los recursos de la computadora y actúa de intermediario entre el hardware (procesador, memoria, disco, pantalla) y las aplicaciones que usa el usuario. Sin un sistema operativo, cada programa tendría que "hablar" directamente con el hardware, algo imposible de mantener.

En este laboratorio trabajaremos con **Debian**, un sistema operativo basado en Linux, con el escritorio **XFCE**. Al final de la lección tendremos una idea clara de las funciones que cumple el sistema.

### Funciones fundamentales

| Función | ¿Qué hace? |
| :--- | :--- |
| Gestión de procesos | Decide qué programas se ejecutan y por cuánto tiempo |
| Gestión de memoria | Reparte la RAM entre los programas en ejecución |
| Gestión de archivos | Organiza el almacenamiento en archivos y carpetas |
| Gestión de dispositivos | Controla teclado, mouse, impresora, discos, red |
| Interface con el usuario | Brinda la pantalla, el escritorio y la terminal |

### Estructura del sistema operativo

```text
+-----------------------------------------------+
|  Aplicaciones (editor, navegador, terminal)   |
+-----------------------------------------------+
|  Entorno de escritorio (XFCE) y herramientas   |
+-----------------------------------------------+
|  Núcleo o kernel (Linux)                       |
+-----------------------------------------------+
|  Hardware (CPU, RAM, disco, dispositivos)      |
+-----------------------------------------------+
```

El **núcleo (kernel)** es el corazón del sistema: permanece cargado en memoria y administra los recursos. Sobre él se apoyan el escritorio y las aplicaciones, que se comunican con el kernel mediante *llamadas al sistema*.

### El rol del sistema como intermediario

Cuando un programa quiere guardar un archivo o mostrar algo en pantalla, no accede al hardware directamente: le pide al sistema operativo que lo haga por él. Esto trae tres beneficios:

1. **Orden:** los recursos se comparten sin que los programas colisionen.
2. **Seguridad:** un programa no puede dañar los datos de otro.
3. **Portabilidad:** un mismo programa puede correr en hardware distinto.

### Micro-desafío práctico

> Abrí la terminal en Debian y ejecutá el comando `uname -a`. Identificá el nombre del núcleo (kernel), la versión y el tipo de arquitectura del procesador. Anotá qué datos encontrás en cada parte de la salida.

### Resumen

- El sistema operativo administra los recursos y media entre hardware y aplicaciones.
- Sus funciones principales son procesos, memoria, archivos, dispositivos e interface.
- El kernel es el componente central que permanece siempre en memoria.
- Debian con XFCE es nuestro laboratorio para verlo funcionar.
