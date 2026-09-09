### Grupos y recursos compartidos

El sistema operativo extiende los límites de una máquina al **grupo de trabajo**: varios equipos comparten **archivos e impresoras**. En esta lección vemos el concepto de grupo y cómo acceder a recursos compartidos con Samba y NFS.

### El concepto de grupo

Un **grupo de trabajo** es un conjunto de equipos en una red local que comparten recursos. No dependen de un servidor central: cada equipo puede compartir y consumir recursos.

### Recursos que se comparten

- **Archivos:** documentos, imágenes y carpetas.
- **Impresoras:** un equipo comparte su impresora con los demás.
- **Discos:** carpetas completas montadas en otros equipos.

### Compartir con Samba

**Samba** implementa el protocolo SMB/CIFS y permite compartir recursos con equipos **Windows** y Linux.

```bash
# Instalar el servidor Samba
sudo apt install samba

# Compartir una carpeta: editar /etc/samba/smb.conf y agregar
```

```text
[compartido]
   path = /srv/compartido
   read only = no
   guest ok = no
```

```bash
# Verificar la configuración y reiniciar
sudo testparm
sudo systemctl restart smbd
```

### Acceder a un recurso compartido

```bash
# Listar los recursos compartidos de un equipo
smbclient -L //servidor

# Montar una carpeta compartida por Samba
sudo mkdir -p /mnt/compartido
sudo mount -t cifs //servidor/compartido /mnt/compartido -o username=usuario
```

### Compartir con NFS

**NFS** es el protocolo nativo de Linux para compartir sistemas de archivos.

```bash
sudo apt install nfs-kernel-server
```

```text
# En /etc/exports
/srv/compartido  192.168.1.0/24(rw,sync)
```

```bash
sudo exportfs -a
```

### Micro-desafío práctico

> Creá la carpeta `/srv/compartido`, dale permisos y configurá una compartición con Samba. Verificá con `testparm` y `smbclient -L localhost`. Si tenés otro equipo en la red, probá acceder al recurso desde él.

### Resumen

- Un grupo de trabajo comparte archivos e impresoras en red local.
- Samba (SMB/CIFS) permite compartir con Windows y Linux.
- NFS es el protocolo nativo de Linux para compartir sistemas de archivos.
- `smbclient`, `mount -t cifs` y `exportfs` administran el acceso.
