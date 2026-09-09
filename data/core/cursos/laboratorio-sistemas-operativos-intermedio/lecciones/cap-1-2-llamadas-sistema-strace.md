### Las llamadas al sistema

Las aplicaciones no acceden al hardware directamente: piden servicios al núcleo mediante **llamadas al sistema (syscalls)**. Son la interface entre el modo usuario y el modo núcleo.

### Qué es una syscall

Una syscall es una función del núcleo que un programa invoca para realizar una operación privilegiada: abrir un archivo, crear un proceso, asignar memoria o enviar datos por la red.

```text
Aplicación  ->  syscall (open, read, write, fork, exec)  ->  núcleo  ->  hardware
```

### Ejemplos comunes de syscalls

| Syscall | Función |
| :--- | :--- |
| `open` | Abre un archivo |
| `read` | Lee datos de un archivo |
| `write` | Escribe datos |
| `close` | Cierra un archivo |
| `fork` | Crea un proceso hijo |
| `exec` | Reemplaza el programa de un proceso |

### Observar syscalls con `strace`

`strace` rastrea las llamadas al sistema que hace un programa. Es una herramienta de diagnóstico muy valiosa.

```bash
# Instalación
sudo apt install strace

# Ver las syscalls de un comando simple
strace ls
```

La salida muestra, por ejemplo:

```text
openat(AT_FDCWD, "/etc/ld.so.cache", O_RDONLY) = 3
write(1, "apuntes  practicas  respaldos\n", 30) = 30
```

Cada línea indica la syscall, sus argumentos y el valor de retorno.

### Usar strace para diagnosticar

```bash
# Seguir todas las operaciones de un comando
strace -f cp origen.txt destino.txt

# Ver solo las syscalls de un tipo
strace -e trace=open cp origen.txt destino.txt
```

Si un programa falla, strace ayuda a ver la última syscall antes del error.

### Micro-desafío práctico

> Instalá `strace`. Ejecutá `strace ls` y anotá tres syscalls distintas que aparezcan. Luego usá `strace -e trace=open,write ls` y explicá para qué sirve limitar el rastreo a ciertas syscalls.

### Resumen

- Las syscalls son la interface de los programas con el núcleo.
- `open`, `read`, `write`, `fork` y `exec` son syscalls básicas.
- `strace` rastrea las syscalls de un programa y ayuda a diagnosticar.
- Cada syscall tiene argumentos y un valor de retorno.
