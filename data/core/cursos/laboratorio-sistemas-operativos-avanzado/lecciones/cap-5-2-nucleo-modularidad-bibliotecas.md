### Núcleo, modularidad y bibliotecas

Dentro de la arquitectura de un sistema operativo hay conceptos clave que explican cómo se organiza: el **núcleo**, la **modularidad** y las **bibliotecas compartidas**.

### El núcleo (kernel)

El núcleo es el componente central del sistema. Su diseño define la arquitectura:

| Diseño | Descripción | Ejemplos |
| :--- | :--- | :--- |
| Monolítico | Todo el sistema en un solo programa | Linux |
| Microkernel | Solo lo esencial; el resto como servicios | Minix, QNX |
| Híbrido | Mezcla de ambos | Windows, macOS |

Linux es **monolítico y modular**: el núcleo es un todo, pero los controladores se agregan como módulos.

### La modularidad

La **modularidad** permite agregar o quitar componentes sin recompilar el núcleo:

```bash
# Módulos cargados
lsmod

# Cargar y descargar un módulo
sudo modprobe vfat
sudo modprobe -r vfat
```

Los módulos permiten un sistema **flexible y eficiente**: solo se carga lo que hace falta.

### Bibliotecas compartidas

Las **bibliotecas** son conjuntos de código reutilizable que los programas comparten.

| Sistema | Extensión | Nombre |
| :--- | :--- | :--- |
| Windows | `.dll` | Dynamic Link Library |
| Linux | `.so` | Shared Object |

```bash
# Bibliotecas que usa un programa
ldd /bin/ls

# Buscar dónde está una biblioteca
ldconfig -p | grep libc
```

### Compatibilidad entre sistemas

- Los programas de un sistema no se ejecutan en otro directamente.
- La compatibilidad se logra con **estándares** (POSIX), **bibliotecas portables** y **emuladores**.
- Un programa compilado para Linux (`.so`) no corre en Windows (`.dll`) sin recompilación o compatibilidad.

### Micro-desafío práctico

> Ejecutá `lsmod` y anotá tres módulos cargados. Con `ldd /bin/ls` listá las bibliotecas que usa el comando `ls`. Buscá en tu sistema alguna biblioteca `.so` con `find /usr/lib -name "*.so" | head`. Explicá qué papel juegan las bibliotecas en la compatibilidad.

### Resumen

- El núcleo puede ser monolítico, microkernel o híbrido.
- La modularidad permite cargar y descargar controladores.
- Las bibliotecas compartidas son `.dll` (Windows) y `.so` (Linux).
- `ldd` y `ldconfig` muestran las bibliotecas de un programa.
