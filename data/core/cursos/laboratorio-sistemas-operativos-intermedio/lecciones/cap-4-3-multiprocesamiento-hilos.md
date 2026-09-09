### Multiprocesamiento y líneas de ejecución paralelas

Las computadoras modernas tienen **múltiples procesadores o núcleos**. Para aprovecharlos, los sistemas ejecutan **líneas de ejecución paralelas** (hilos), lo que acelera el trabajo pero también plantea problemas de comportamiento.

### Núcleos y procesadores

```bash
# Cantidad de procesadores lógicos
nproc

# Información de la CPU
lscpu
```

Si `nproc` devuelve 4, el sistema puede ejecutar hasta 4 tareas de forma simultánea.

### Procesos e hilos

- Un **proceso** puede tener varias **líneas de ejecución (threads)**.
- Cada hilo corre dentro del mismo proceso y comparte su memoria.
- El sistema operativo reparte los hilos entre los núcleos disponibles.

```bash
# Ver hilos de los procesos
ps -eLf
htop          # la columna TID muestra cada hilo
```

### Problemas de comportamiento

Las ejecuciones paralelas tienen desafíos:

| Problema | Descripción |
| :--- | :--- |
| Condiciones de carrera | Dos hilos modifican el mismo dato a la vez |
| Sincronización | Los hilos deben coordinar su avance |
| Consumo de recursos | Demasiados hilos saturan la CPU y la memoria |

### Herramientas de diagnóstico

```bash
# Carga del sistema: el primer número es el promedio de 1 minuto
uptime

# Uso por núcleo
top            # presionar "1" muestra cada núcleo
htop           # cada barra es un núcleo

# Estadísticas de procesos y CPU
vmstat
```

### La carga del sistema

`uptime` muestra la **carga promedio (load average)**. Si los tres números superan la cantidad de núcleos (`nproc`), el sistema está saturado.

### Micro-desafío práctico

> Ejecutá `nproc` y `lscpu` y anotá cuántos núcleos lógicos tenés. Corré `uptime` y compará la carga promedio con la cantidad de núcleos. En `top`, presioná `1` y observá cómo se reparte el trabajo entre los núcleos.

### Resumen

- Los múltiples núcleos permiten ejecución paralela de hilos.
- `nproc` y `lscpu` muestran la capacidad de la CPU.
- Los hilos comparten memoria dentro de un proceso.
- La carga promedio y `top` ayudan a diagnosticar la saturación.
