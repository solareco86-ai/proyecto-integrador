### Seguridad en la red

La red es una puerta de entrada al sistema. La seguridad en red combina el **firewall**, la **gestión de actualizaciones** y el **monitoreo** de servicios expuestos.

### ¿Qué es un firewall?

Un **firewall** filtra el tráfico de red entrante y saliente según **reglas**. Permite o bloquea conexiones para proteger el sistema.

### nftables: el firewall de Linux

```bash
# Ver las reglas actuales
sudo nft list ruleset

# Ejemplo: permitir tráfico local y rechazar lo demás
sudo nft add table inet filtro
sudo nft add chain inet filtro entrada { type filter hook input priority 0\; }
sudo nft add rule inet filtro entrada iif lo accept
sudo nft add rule inet filtro entrada ct state established,related accept
sudo nft add rule inet filtro entrada drop
```

### ufw: firewall simple

Para simplificar, `ufw` ofrece reglas en lenguaje humano:

```bash
sudo apt install ufw

# Reglas básicas
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable

# Ver el estado
sudo ufw status verbose
```

### Servicios y puertos expuestos

```bash
# ¿Qué servicios están escuchando en la red?
ss -tulpn
```

Cada puerto abierto es una puerta potencial. Los más comunes:

| Puerto | Servicio |
| :--- | :--- |
| 22 | SSH |
| 80 / 443 | Web (HTTP/HTTPS) |
| 631 | Impresión (CUPS) |

### Actualizaciones de seguridad

Mantener el sistema al día es esencial:

```bash
sudo apt update
sudo apt upgrade

# Instalar actualizaciones de seguridad automáticamente
sudo apt install unattended-upgrades
```

### Micro-desafío práctico

> Ejecutá `ss -tulpn` y anotá los servicios que están escuchando. Instalá `ufw`, configurá las reglas básicas (deny incoming, allow ssh) y activalo con `sudo ufw enable`. Verificá con `sudo ufw status verbose` y explicá qué puertos quedaron abiertos y por qué.

### Resumen

- El firewall filtra el tráfico según reglas de seguridad.
- `nftables` y `ufw` administran el firewall en Debian.
- `ss -tulpn` muestra los servicios expuestos a la red.
- Actualizar el sistema y aplicar parches de seguridad es obligatorio.
