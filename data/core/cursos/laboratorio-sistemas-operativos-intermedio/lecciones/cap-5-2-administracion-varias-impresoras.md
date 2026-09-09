### Administrar varias impresoras

En un laboratorio puede haber **varias impresoras**: locales, de red o compartidas. CUPS permite administrarlas, enviar trabajos a cada una y preparar salidas para impresoras **no necesariamente conectadas**.

### Tipos de impresoras

| Tipo | Descripción |
| :--- | :--- |
| Local | Conectada por USB o cable al equipo |
| De red | Accesible por IP o nombre en la red |
| Compartida | Servida por otro equipo con CUPS |
| PDF virtual | Genera archivos PDF en lugar de papel |

### Listar y agregar impresoras

```bash
# Ver las impresoras configuradas
lpstat -p

# Ver impresoras disponibles y por defecto
lpstat -d
```

Agregar una impresora desde la web de CUPS:

```text
http://localhost:631 -> Administration -> Add Printer
```

### Enviar a una impresora específica

```bash
lp -d impresora_a documento.txt
lp -d impresora_b documento.txt
```

### Preparar salidas para impresoras no conectadas

Una impresora puede estar configurada aunque no esté conectada en este momento. Los trabajos quedan **encolados** y se imprimirán cuando la impresora esté disponible.

También se pueden preparar salidas a archivo (por ejemplo, a PDF) para imprimir luego:

```bash
# Enviar un documento a la impresora PDF virtual
lp -d impresora_pdf documento.txt
```

### Pausar, reordenar y cancelar

```bash
# Pausar una impresora
cupsdisable impresora_a

# Reanudar
cupsenable impresora_a

# Cancelar todos los trabajos de una impresora
lprm -P impresora_a -
```

### Micro-desafío práctico

> Listá las impresoras con `lpstat -p`. Configurá una impresora virtual PDF si no existe (CUPS suele incluirla). Enviá un documento a la impresora PDF y otro a la impresora principal, y verificá con `lpstat -t` a qué cola fue cada trabajo.

### Resumen

- CUPS administra varias impresoras locales, de red y virtuales.
- `lp -d <impresora>` envía trabajos a una impresora puntual.
- Las salidas pueden prepararse para impresoras no conectadas.
- `cupsdisable`, `cupsenable` y `lprm` administran el estado y la cola.
