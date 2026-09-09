### Las tipografías (fonts)

Las **tipografías** son los conjuntos de caracteres que las aplicaciones usan para dibujar el texto. El sistema operativo las administra de forma centralizada para que todos los programas puedan usarlas.

### Formatos de tipografía

| Formato | Extensión | Características |
| :--- | :--- | :--- |
| TrueType | `.ttf` | Muy difundido, escalable |
| OpenType | `.otf` | Extiende TrueType con más funciones |
| PostScript | `.pfb` / `.pfa` | Usado históricamente en impresión |

### Dónde se guardan las tipografías

```text
/usr/share/fonts/     # tipografías del sistema
~/.local/share/fonts/ # tipografías del usuario
```

```bash
# Listar tipografías instaladas
fc-list

# Ver las tipografías de un formato
fc-list | grep -i ttf

# Buscar una tipografía
fc-match "DejaVu Sans"
```

### Instalar una tipografía

**Para el usuario actual** (no requiere sudo):

```bash
mkdir -p ~/.local/share/fonts
cp MiTipografia.ttf ~/.local/share/fonts/
fc-cache -f -v
```

**Para todo el sistema:**

```bash
sudo cp MiTipografia.ttf /usr/share/fonts/truetype/
sudo fc-cache -f -v
```

### Cómo funcionan las tipografías

- El sistema mantiene un **índice de tipografías** (`fc-cache`).
- Las aplicaciones piden una tipografía por nombre con `fontconfig`.
- Al imprimir, las tipografías se **incrustan o se sustituyen** según el documento.

### Micro-desafío práctico

> Descargá o copiá una tipografía `.ttf` en tu equipo. Instalala para tu usuario en `~/.local/share/fonts/`, actualizá el índice con `fc-cache -f` y verificá con `fc-list | grep <nombre>` que quedó disponible. Abrí un editor y aplicá esa tipografía.

### Resumen

- Las tipografías son conjuntos de caracteres escalables (ttf, otf).
- Se instalan a nivel de usuario o de sistema.
- `fc-list` y `fc-match` consultan las tipografías instaladas.
- `fc-cache` actualiza el índice que usan las aplicaciones.
