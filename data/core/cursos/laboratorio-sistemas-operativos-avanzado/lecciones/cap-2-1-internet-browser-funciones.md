### Internet y el browser

**Internet** es la red mundial de redes que conecta miles de millones de computadoras. El **browser (navegador)** es el programa que interpreta las páginas web y muestra su contenido.

### ¿Qué es Internet?

Internet funciona gracias a:

| Componente | Función |
| :--- | :--- |
| Direcciones IP | Identifican cada equipo en la red |
| DNS | Traduce nombres (ej. debian.org) a direcciones IP |
| Protocolo TCP/IP | Reglas para transmitir los datos |
| Servidores web | Guardan y sirven las páginas |
| Navegador | Interpreta y muestra el contenido |

### El protocolo HTTP/HTTPS

El navegador se comunica con los servidores usando **HTTP** (o **HTTPS**, su versión segura):

```text
Cliente (browser)  --solicitud HTTP-->  Servidor web
Cliente (browser)  <--respuesta HTTP--  Servidor web
```

### El browser y sus funciones

| Función | Descripción |
| :--- | :--- |
| Navegación | Ir a una dirección o enlace |
| Pestañas | Abrir varias páginas a la vez |
| Historial | Recordar las páginas visitadas |
| Marcadores | Guardar sitios favoritos |
| Descargas | Bajar archivos al equipo |
| Extensiones | Agregar funciones extra |

### Navegadores en Debian

```bash
sudo apt install firefox-esr
```

También están disponibles `chromium` y navegadores livianos para XFCE como `epiphany` o `falkon`.

### Diagnóstico de la conexión desde la terminal

```bash
# Resolución de nombres (DNS)
getent hosts debian.org

# Cabeceras de un sitio (HTTP)
curl -I https://debian.org
```

### Micro-desafío práctico

> Abrí el navegador y navegá a un sitio de tu elección. Usá el menú del navegador para: abrir una pestaña nueva, guardar un marcador y consultar el historial. Desde la terminal, probá `getent hosts debian.org` y `curl -I https://debian.org` y anotá los datos que devuelven.

### Resumen

- Internet conecta equipos mediante IP, DNS y TCP/IP.
- El browser interpreta y muestra las páginas web.
- Las funciones del navegador incluyen pestañas, historial y marcadores.
- `getent` y `curl` diagnostican la conexión desde la terminal.
