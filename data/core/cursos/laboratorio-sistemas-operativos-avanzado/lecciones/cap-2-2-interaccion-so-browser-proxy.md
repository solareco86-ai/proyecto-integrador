### El browser y el sistema operativo

El navegador no trabaja aislado: depende del sistema operativo para la red, los certificados, el proxy y las tipografías. Cuando algo "no anda" en el browser, muchas veces el problema está **en el sistema**.

### Cómo interactúa el browser con el SO

```text
Browser -> bibliotecas del sistema (TLS, DNS, red) -> kernel -> tarjeta de red
```

- La **resolución de nombres** usa los DNS del sistema (`/etc/resolv.conf`).
- Los **certificados** de seguridad se guardan a nivel de sistema.
- El **proxy** puede estar configurado en el sistema o en el browser.
- Las **tipografías** y fuentes que muestra el browser son las del sistema.

### Configurar el proxy

Un proxy es un servidor intermediario que muchas redes usan para salir a Internet.

**A nivel de sistema (variables de entorno):**

```bash
export http_proxy="http://proxy.ejemplo.com:3128"
export https_proxy="http://proxy.ejemplo.com:3128"
```

**En el browser:** se configura en sus preferencias de red.

### Problemas de ajuste y compatibilidad

| Problema | Causa habitual | Solución |
| :--- | :--- | :--- |
| El sitio no carga | DNS o proxy mal configurados | Revisar `/etc/resolv.conf` y el proxy |
| Página con "certificado inválido" | Certificados del sistema desactualizados | `sudo apt install ca-certificates` |
| Tipografías raras o rotas | Faltan fuentes | Instalar tipografías del sistema |
| Aplicaciones web lentas | Swapping excesivo | Revisar la memoria con `free` |

### Herramientas de diagnóstico

```bash
# ¿Resuelve el DNS del sistema?
getent hosts debian.org

# ¿Funciona la red?
curl -I https://debian.org

# ¿El proxy responde?
curl -I -x http://proxy.ejemplo.com:3128 https://debian.org
```

### Micro-desafío práctico

> Ejecutá `getent hosts debian.org` y `curl -I https://debian.org` y verificá que respondan. Consultá el archivo `/etc/resolv.conf` y anotá los DNS configurados. Si tu red usa proxy, configuralo como variable de entorno y verificá que `curl` lo use.

### Resumen

- El browser depende del sistema para DNS, certificados, proxy y fuentes.
- El proxy se configura en el sistema o en el browser.
- Los certificados se actualizan con el paquete `ca-certificates`.
- `getent` y `curl` aíslan el origen de los problemas de navegación.
