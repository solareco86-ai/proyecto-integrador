### Sistemas de archivos y montaje

Un **sistema de archivos (filesystem)** es la forma en que el sistema operativo organiza y guarda los datos en un dispositivo. En Linux, los sistemas de archivos se **montan** en el árbol de directorios para poder usarlos.

### Tipos de sistemas de archivos

| Tipo | Uso típico |
| :--- | :--- |
| `ext4` | Sistema de archivos nativo de Linux (raíz `/`) |
| `xfs` | Sistemas de archivos grandes y robustos |
| `btrfs` | Copias y snapshots avanzados |
| `fat32` / `exfat` | Pendrives y compatibilidad con Windows |
| `ntfs` | Discos usados con Windows |

Para ver qué tipo de sistema de archivos usa cada partición:

```bash
df -T
```

### Qué es montar

**Montar** es vincular un dispositivo (o partición) a un directorio del árbol. Por ejemplo, montar un pendrive en `/media/usb` hace que su contenido sea visible en esa carpeta.

```bash
# Ver los montajes actuales
mount

# Montar un pendrive (ejemplo)
sudo mount /dev/sdb1 /media/usb

# Desmontar
sudo umount /media/usb
```

### El archivo de configuración `/etc/fstab`

El archivo `/etc/fstab` define qué sistemas de archivos se montan al arrancar.

```text
# dispositivo  punto de montaje  tipo  opciones  dump  pass
UUID=abc123     /                 ext4   errors=remount-ro  0  1
UUID=def456     /home             ext4   defaults           0  2
```

- Las particiones se identifican por su **UUID**, que no cambia.
- `pass` con `1` o `2` activa la verificación del sistema de archivos al arrancar.

### Verificar sistemas de archivos

```bash
# Verificar un sistema de archivos (desmontado o en modo seguro)
sudo fsck /dev/sdb1

# Ver la información de las particiones
lsblk -f
```

### Micro-desafío práctico

> Ejecutá `lsblk -f` y anotá las particiones de tu disco con su tipo de sistema de archivos, tamaño y punto de montaje. Revisá `df -T` y explicá qué partición corresponde a la raíz `/`. Luego consultá `/etc/fstab` y anotá las entradas que aparecen.

### Resumen

- El sistema de archivos organiza los datos en el dispositivo.
- `ext4` es el sistema de archivos habitual de la raíz en Linux.
- Montar vincula un dispositivo a un directorio del árbol.
- `/etc/fstab` define los montajes al arrancar.
