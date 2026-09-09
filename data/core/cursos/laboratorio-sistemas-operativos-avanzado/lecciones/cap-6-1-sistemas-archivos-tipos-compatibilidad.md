### Sistemas de archivos: tipos y compatibilidad

El **sistema de archivos** define cómo se guardan y organizan los datos en un dispositivo. La elección afecta el rendimiento, la fiabilidad y la compatibilidad entre sistemas operativos.

### Tipos de sistemas de archivos

| Tipo | Sistema | Características |
| :--- | :--- | :--- |
| `ext4` | Linux | Estándar, fiable, con journaling |
| `xfs` | Linux | Muy bueno para archivos y volúmenes grandes |
| `btrfs` | Linux | Snapshots y compresión integrados |
| `fat32` | Todos | Compatible pero sin journaling y con límites |
| `exfat` | Windows/Linux | Para pendrives grandes |
| `ntfs` | Windows | Sistema nativo de Windows |

### El journaling

El **journaling** (bitácora) registra las operaciones antes de realizarlas. Si el sistema se corta, el journaling permite **recuperar** el sistema de archivos más rápido y con menos pérdida de datos.

```bash
# Ver el tipo de sistema de archivos de cada partición
df -T
lsblk -f
```

### Compatibilidad entre sistemas

- **Linux** lee la mayoría de los sistemas de archivos, incluidos los de Windows (`ntfs`, `fat32`, `exfat`).
- **Windows** no lee nativamente `ext4`.
- Para intercambiar datos se usan formatos neutros (`fat32`, `exfat`) o herramientas especiales.

```bash
# Instalar soporte NTFS en Debian
sudo apt install ntfs-3g
```

### Verificar y reparar

```bash
# Revisar el estado de un sistema de archivos
sudo fsck /dev/sda1

# Información detallada de discos
sudo fdisk -l
```

### Micro-desafío práctico

> Ejecutá `lsblk -f` y `df -T` y anotá qué sistemas de archivos usa cada partición de tu equipo. Explicá qué sistema de archivos usarías para un pendrive que vas a compartir con equipos Windows y por qué. Verificá si `ntfs-3g` está instalado.

### Resumen

- Los sistemas de archivos difieren en fiabilidad, rendimiento y compatibilidad.
- El journaling protege los datos ante cortes de energía.
- Linux soporta muchos sistemas de archivos; Windows no lee `ext4`.
- `df`, `lsblk` y `fsck` diagnostican y reparan los sistemas de archivos.
