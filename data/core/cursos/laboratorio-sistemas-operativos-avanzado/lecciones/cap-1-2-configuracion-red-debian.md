### Configuración de red en Debian

La red es lo que conecta la máquina con el grupo y el mundo. En esta lección vemos cómo **consultar** y **configurar** las interfaces de red en Debian.

### Ver las interfaces de red

```bash
# Interfaces y direcciones IP
ip addr

# Estado de los enlaces
ip link

# Ruta por defecto (por dónde sale a Internet)
ip route
```

### Herramientas de red

| Herramienta | Uso |
| :--- | :--- |
| `ip` | Consulta y configura interfaces y rutas |
| `ping` | Prueba de conectividad con otro equipo |
| `traceroute` | Traza el camino hasta un destino |
| `ss` | Puertos y conexiones abiertos |
| `nmtui` | Configuración de red con interfaz de texto |

### Configurar la red con `nmtui`

**nmtui** ofrece un menú en la terminal para configurar la red:

```bash
sudo nmtui
```

Dentro del menú se pueden **activar o desactivar** conexiones, **editar** su configuración (IP fija o DHCP) y **establecer el hostname**.

### Archivos de configuración

| Archivo | Contenido |
| :--- | :--- |
| `/etc/network/interfaces` | Configuración de red clásica |
| `/etc/hostname` | El nombre del equipo |
| `/etc/resolv.conf` | Servidores de nombres (DNS) |
| `/etc/hosts` | Asociación local de nombres e IPs |

### Pruebas de conectividad

```bash
# ¿Hay conexión con un servidor?
ping -c 4 8.8.8.8

# ¿Resuelve nombres (DNS)?
ping -c 4 debian.org

# ¿Qué puertos están escuchando?
ss -tulpn
```

### Micro-desafío práctico

> Ejecutá `ip addr` y anotá la dirección IP de tu equipo, la máscara y la interface. Probá conectividad con `ping -c 4` hacia la IP de un compañero, hacia una IP pública y hacia `debian.org`. Compará los tres resultados y explicá qué diferencia hay entre fallar por red o por DNS.

### Resumen

- `ip addr`, `ip link` y `ip route` consultan la red.
- `nmtui` permite configurar la red con una interface de texto.
- Los archivos `/etc/network/interfaces` y `/etc/hosts` guardan la configuración.
- `ping` y `ss` prueban la conectividad y los servicios.
