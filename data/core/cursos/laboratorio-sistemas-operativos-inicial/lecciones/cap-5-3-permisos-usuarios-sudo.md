### Usuarios, grupos y permisos

El sistema operativo protege los archivos mediante **usuarios, grupos y permisos**. Cada archivo pertenece a un usuario y a un grupo, y define quién puede leerlo, escribirlo o ejecutarlo.

### Usuarios y grupos

- **Usuario:** identidad con la que ingresás al sistema.
- **Grupo:** conjunto de usuarios con permisos comunes.
- **root:** el superusuario con control total del sistema.

En Debian el usuario normal realiza las tareas administrativas con `sudo`, que eleva los privilegios puntualmente.

### Permisos de un archivo

Los permisos se representan con letras y con números:

```text
-rwxr-xr--  agustin  estudiantes  archivo.txt
```

| Posición | Significado |
| :--- | :--- |
| `-` | Tipo de archivo (archivo normal; `d` es carpeta) |
| `rwx` | Permisos del dueño (agustin) |
| `r-x` | Permisos del grupo (estudiantes) |
| `r--` | Permisos de los demás |

- `r` (4): lectura
- `w` (2): escritura
- `x` (1): ejecución

### Cambiar permisos con `chmod`

```bash
chmod +x script.sh        # agrega ejecución a todos
chmod 750 archivo.txt     # dueño rwx, grupo r-x, otros sin permisos
chmod u+w archivo.txt     # agrega escritura al dueño (u)
```

### Cambiar dueño con `chown`

```bash
sudo chown agustin archivo.txt       # cambia el dueño
sudo chown agustin:estudiantes a.txt # cambia dueño y grupo
```

### El comando `sudo`

```bash
sudo apt update
sudo systemctl restart networking
```

`sudo` pide la contraseña del usuario y ejecuta el comando con privilegios de root.

### Micro-desafío práctico

> Creá un archivo `datos.txt`, listalo con `ls -l` y anotá sus permisos. Con `chmod` quitá la escritura para el grupo y agregá ejecución. Luego consultá quién sos con `whoami` y a qué grupos perteneces con `groups`. Comprobá si podés escribir en `datos.txt` y explicá por qué.

### Resumen

- Los archivos pertenecen a un usuario y un grupo.
- Los permisos rwx se expresan con letras o números.
- `chmod` cambia permisos; `chown` cambia dueño y grupo.
- `sudo` permite ejecutar tareas administrativas con control.
