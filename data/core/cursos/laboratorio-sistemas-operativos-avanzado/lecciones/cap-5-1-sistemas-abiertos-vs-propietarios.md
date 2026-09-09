### Sistemas abiertos y cerrados

Los sistemas operativos se clasifican según el acceso a su **código fuente**. Esta elección define costos, control, seguridad y compatibilidad.

### Sistemas de código abierto

El **código fuente** está disponible para verlo, usarlo y modificarlo.

| Característica | Descripción |
| :--- | :--- |
| Transparencia | Cualquiera puede auditar el código |
| Costo | Generalmente gratuito |
| Comunidad | Desarrollado y revisado por muchas personas |
| Control | El usuario decide qué instalar y modificar |

Ejemplos: **Debian**, Ubuntu, Fedora, Arch, FreeBSD.

### Sistemas cerrados o propietarios

El código es **secreto** y controlado por una empresa.

| Característica | Descripción |
| :--- | :--- |
| Soporte comercial | La empresa se hace responsable |
| Uniformidad | Una sola versión oficial |
| Costo | Licencias pagas |
| Control | Solo la empresa modifica el producto |

Ejemplos: **Windows**, macOS.

### Comparación

| Aspecto | Abierto | Propietario |
| :--- | :--- | :--- |
| Código fuente | Visible | Secreto |
| Licencia | Libre | Paga |
| Modificaciones | Permitidas | Restringidas |
| Soporte | Comunidad / contratos | Empresa |
| Personalización | Alta | Baja |

### Instalación y compatibilidad

- En un sistema abierto se **adaptan** los programas al sistema.
- En un sistema propietario el sistema **debe** soportar los programas.
- La compatibilidad entre ambos se logra con estándares (SMB, HTTP, PDF, etc.) y emuladores.

### Debian como sistema abierto

Debian se rige por el **Contrato Social Debian** y las **Directrices de Software Libre (DFSG)**: garantizan que el sistema siga siendo libre.

```bash
# Ver la licencia de un paquete
apt show vim | grep -i license
```

### Micro-desafío práctico

> Elegí un programa que uses en el laboratorio (por ejemplo `htop` o `vim`) y consultá su licencia con `apt show`. Investigá en tu cuaderno dos sistemas operativos abiertos y dos propietarios, y comparalos según las características de la tabla.

### Resumen

- Los sistemas abiertos exponen su código y son libres.
- Los sistemas propietarios son secretos y comerciales.
- La elección afecta costos, control, soporte y personalización.
- Debian es un sistema abierto regido por su contrato social.
