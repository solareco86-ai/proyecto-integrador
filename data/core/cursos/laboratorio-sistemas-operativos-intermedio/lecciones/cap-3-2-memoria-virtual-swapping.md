### Memoria virtual y swapping

Cuando la RAM se agota, el sistema operativo usa la **memoria virtual** y el **espacio de intercambio (swap)** para seguir trabajando. Entender el **swapping** es clave para diagnosticar lentitud.

### Memoria virtual

La **memoria virtual** es la técnica que permite usar espacio del disco como si fuera RAM. Cada programa cree tener mucha memoria disponible; el sistema traslada páginas de memoria entre la RAM y el disco según hace falta.

### ¿Qué es el swapping?

El **swapping** es el movimiento de páginas de memoria entre la RAM y el área de intercambio:

```text
RAM  <--->  swap (disco)
```

Cuando falta RAM, el sistema "envía" páginas al swap y las recupera cuando vuelven a necesitarse. Como el disco es mucho más lento que la RAM, un **swap excesivo frena la ejecución**.

### Ver el swap

| Comando | Qué muestra |
| :--- | :--- |
| `free -h` | Tamaño y uso del swap |
| `swapon --show` | Áreas de swap activas |
| `vmstat` | Páginas intercambiadas por segundo |

### Diagnóstico del swapping

```bash
free -h
vmstat 2 5
```

En `vmstat`, las columnas `si` (swap in) y `so` (swap out) muestran el tráfico de intercambio. Valores altos indican que el sistema está "golpeando" el disco y puede estar lento.

### Crear y activar un archivo de swap

```bash
# Crear un archivo de 2 GB
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile

# Formatearlo como swap y activarlo
sudo mkswap /swapfile
sudo swapon /swapfile

# Verificar
swapon --show
```

### Micro-desafío práctico

> Ejecutá `free -h` y anotá el tamaño y uso del swap. Corré `vmstat 2 10` y observá las columnas `si` y `so`. Si tu sistema no tiene swap, creá un archivo de 1 GB, activalo y verificá con `swapon --show`.

### Resumen

- La memoria virtual extiende la RAM usando espacio del disco.
- El swapping mueve páginas entre RAM y swap.
- Un swap excesivo frena la ejecución de los programas.
- `free`, `vmstat` y `swapon` diagnostican el intercambio.
