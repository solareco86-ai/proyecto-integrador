### El gestor de paquetes

Debian usa **APT** para instalar, actualizar y quitar programas. Un **paquete** es un archivo que contiene el programa y sus metadatos. El gestor resuelve automáticamente las **dependencias** (bibliotecas que el programa necesita).

### Comandos fundamentales de apt

| Comando | Acción |
| :--- | :--- |
| `sudo apt update` | Actualiza la lista de paquetes disponibles |
| `sudo apt upgrade` | Actualiza los paquetes instalados |
| `sudo apt install <paquete>` | Instala un paquete y sus dependencias |
| `sudo apt remove <paquete>` | Quita un paquete |
| `sudo apt search <texto>` | Busca paquetes por nombre o descripción |
| `sudo apt show <paquete>` | Muestra información de un paquete |

### Elementos optativos del sistema

Además de los paquetes básicos, se pueden agregar **elementos optativos** que amplían las posibilidades del sistema:

```bash
# Escritorio y aplicaciones
sudo apt install firefox-esr libreoffice evince

# Herramientas de administración
sudo apt install htop neofetch nmap curl wget

# Multimedia y utilidades
sudo apt install vlc file-roller unzip
```

### Buscar antes de instalar

Una buena práctica es buscar el paquete antes de instalarlo:

```bash
apt search editor
apt show htop
```

Esto evita instalar paquetes equivocados o con nombres parecidos.

### Actualización del sistema

Mantener el sistema actualizado es parte del mantenimiento:

```bash
sudo apt update
sudo apt upgrade
```

Para limpiar paquetes que ya no se necesitan:

```bash
sudo apt autoremove
```

### Micro-desafío práctico

> Usá `apt search` para encontrar un reproductor multimedia y un editor de texto. Instalá `htop` (si no lo tenés) y ejecutalo. Luego verificá con `apt show htop` qué versión y dependencias tiene.

### Resumen

- APT instala, actualiza y quita paquetes resolviendo dependencias.
- `apt update` refresca la lista; `apt install` agrega programas.
- Los elementos optativos amplían el sistema según las necesidades.
- Mantener el sistema actualizado y limpio es parte del manejo.
