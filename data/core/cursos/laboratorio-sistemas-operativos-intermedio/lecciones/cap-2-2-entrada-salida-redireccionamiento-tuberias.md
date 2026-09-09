### Entrada/salida, redireccionamiento y tuberías

Cada programa recibe datos por su **entrada estándar** y entrega resultados por su **salida estándar**. En la terminal podemos **redirigir** esos flujos y **encadenar** comandos con tuberías.

### Los flujos estándar

| Flujo | Descripción | Número |
| :--- | :--- | :--- |
| Entrada estándar (stdin) | Datos que el programa lee | 0 |
| Salida estándar (stdout) | Resultados normales | 1 |
| Error estándar (stderr) | Mensajes de error | 2 |

### Redireccionamiento

```bash
# Guardar la salida en un archivo (sobrescribe)
ls > lista.txt

# Agregar la salida al final del archivo
ls >> lista.txt

# Redirigir errores a un archivo
ls /no-existe 2> errores.txt

# Enviar el contenido de un archivo como entrada
wc -l < texto.txt
```

### Tuberías (pipes)

La tubería `|` envía la salida de un comando como entrada del siguiente:

```bash
ls -l | wc -l          # cuántos elementos hay
ps aux | grep bash     # buscar procesos que contengan "bash"
ls | sort              # ordenar la lista
ls | head -5           # ver solo las primeras 5 líneas
```

### Combinar redireccionamiento y tuberías

```bash
# Guardar en un archivo el resultado de una cadena
ps aux | grep bash > procesos_bash.txt

# Ver y guardar a la vez
ls | tee salida.txt
```

`tee` muestra la salida y también la escribe en un archivo.

### Ejemplo práctico: diagnóstico

```bash
# Contar cuántos procesos tiene el usuario actual
ps aux | grep $(whoami) | wc -l
```

### Micro-desafío práctico

> Ejecutá `ls -l` y redirigí su salida a `lista.txt`. Luego contá las líneas con `wc -l < lista.txt`. Usá una tubería para contar cuántos procesos de `systemd` hay con `ps aux | grep systemd | wc -l`. Guardá ese resultado en un archivo.

### Resumen

- Los programas usan stdin, stdout y stderr.
- `>` y `>>` redirigen la salida; `2>` redirige los errores.
- La tubería `|` conecta la salida de un comando con la entrada del siguiente.
- `tee` muestra y guarda la salida a la vez.
