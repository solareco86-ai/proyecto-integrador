### Seguridad de cuentas y privilegios

La **seguridad** de un sistema comienza por las cuentas de usuario y sus privilegios. La regla de oro es dar a cada uno **solo los permisos que necesita**.

### Principios de seguridad

1. **Menor privilegio:** trabajar como usuario normal; elevar solo lo necesario.
2. **Separación de cuentas:** una cuenta por persona, sin compartir.
3. **Contraseñas fuertes:** largas, únicas y renovadas.
4. **No usar root:** administrar con `sudo` puntual.

### Usuarios y grupos

```bash
# Listar usuarios y grupos
cat /etc/passwd
cat /etc/group

# Crear un usuario y agregarlo a un grupo
sudo adduser agustin
sudo usermod -aG sudo agustin
```

### Administrar contraseñas

```bash
# Cambiar la propia contraseña
passwd

# Cambiar la contraseña de otro usuario (requiere sudo)
sudo passwd agustin
```

### El sistema de `sudo`

`sudo` permite ejecutar un comando con privilegios de administrador sin ingresar como root:

```bash
sudo apt update
```

Los permisos se configuran en `/etc/sudoers` (siempre con `visudo`):

```text
agustin   ALL=(ALL:ALL) ALL
```

### Políticas de contraseña

Se pueden exigir contraseñas más fuertes con el módulo de políticas:

```bash
# Ver la política de contraseñas
chage -l agustin

# Exigir cambio cada 90 días
sudo chage -M 90 agustin
```

### Micro-desafío práctico

> Creá un usuario `practica` con `sudo adduser practica` y agregalo al grupo `sudo`. Verificá con `groups practica`. Probá cambiar su contraseña con `sudo passwd practica`. Consultá la política con `chage -l practica` y establecé la expiración a 90 días.

### Resumen

- La seguridad empieza por cuentas y privilegios bien administrados.
- Se trabaja como usuario normal y se eleva con `sudo`.
- `adduser`, `usermod`, `passwd` y `chage` administran cuentas.
- El menor privilegio reduce el impacto de errores y ataques.
