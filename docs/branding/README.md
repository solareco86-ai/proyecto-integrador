# Manual de marca — ISFT N° 199

> **Alcance:** portal institucional y campus virtual (`isftn199.com.ar`).
> **Implementación:** [static/css/sistema.css](../../static/css/sistema.css) para
> las páginas migradas, [static/css/src/tokens.css](../../static/css/src/tokens.css)
> para las que todavía conservan el sistema anterior.
> **Estado:** vigente desde octubre de 2026.

Este documento define cómo se ve el portal y, sobre todo, **por qué**. Cada regla
tiene un motivo: si el motivo deja de valer, la regla se discute.

---

## 1. Qué queremos que transmita

El ISFT N° 199 es una institución **pública, gratuita y oficial**. Eso define el
registro visual antes que cualquier preferencia estética:

| Debe leerse como | No debe leerse como |
|---|---|
| Un organismo público que se toma en serio a sí mismo | Una landing comercial que vende un curso |
| Claro y verificable | Aspiracional o publicitario |
| Ordenado y legible a las 22:30, después de una jornada laboral | Denso o decorativo |

De ahí salen las tres decisiones de fondo:

1. **La jerarquía la hace la tipografía, no el color.** Un sitio que necesita
   siete colores para que se entienda su estructura está mal maquetado.
2. **Nada decorativo.** Si un elemento no aporta información o no guía una
   acción, no va. Sin degradados, sin íconos que repiten lo que dice el título,
   sin tarjetas que solo sirven para dibujar un rectángulo.
3. **Ningún dato sin fuente.** La marca incluye no publicar fechas, plazos ni
   cifras que no estén confirmados. Es parte de la credibilidad institucional,
   no solo una regla de contenido.

---

## 2. Color

### 2.1 La escala

Blanco como base y una sola familia de azules. El azul es el color del portal
institucional desde su primera versión y el que la comunidad ya asocia al
instituto.

| Token | Valor | Para qué |
|---|---|---|
| `--azul-50` | `#F3F7FB` | Fondo de sección alterna, superficies hundidas |
| `--azul-100` | `#E2EDF7` | Rellenos suaves, estados de reposo |
| `--azul-200` | `#C6DCEF` | Bordes de énfasis |
| `--azul-300` | `#93BEDE` | Marcas secundarias |
| `--azul-500` | `#2176B5` | Acento, numeración de secciones, enlaces en tema oscuro |
| `--azul-600` | `#1A5A91` | **Color primario**: botones sólidos, enlaces, foco |
| `--azul-700` | `#134670` | Hover del primario |
| `--azul-900` | `#0B2A4A` | **Tinta**: todo el texto principal |

### 2.2 Por qué la tinta es azul y no negra

El cuerpo de texto usa `#0B2A4A`, no `#000000` ni un gris neutro. Un negro puro
sobre blanco produce un contraste duro que cansa en lecturas largas, y un gris
neutro ensucia una paleta fría. El azul muy oscuro mantiene el contraste
necesario y hace que el texto pertenezca a la misma familia que el resto.

### 2.3 Semántica

| Token | Valor | Significado |
|---|---|---|
| `--ok` | `#1E7A52` | Resuelto, regular, vigente |
| `--alerta` | `#B4452F` | Vencimiento próximo, condición en riesgo, error |
| `--aviso` | `#B5761A` | En trámite, pendiente de confirmación |

**Son las únicas excepciones al azul.** Si un estado se pintara de azul, se
confundiría con un enlace. Los tres pasan contraste AA sobre blanco.

### 2.4 Reglas de uso

- **El color nunca comunica solo.** Todo estado lleva además texto, ícono o
  posición. Un chip rojo dice «En riesgo»; no es rojo a secas.
- **Sin degradados.** Ni en fondos, ni en botones, ni en encabezados.
- **Las sombras se tiñen de azul** (`rgba(11,42,74,…)`), nunca de negro: una
  sombra neutra sobre blanco agrisa y ensucia.
- **Las superficies se distinguen por tono, no por borde grueso.** Un borde de
  1px en `--linea` y, cuando hace falta elevación, `--sombra-sutil`.

### 2.5 Tema oscuro

El sitio tiene tema claro y oscuro, conmutables desde la cabecera. **El claro es
la apariencia canónica**: es la que se usa en capturas, material impreso y
presentaciones. El oscuro invierte las superficies a navy (`#091A2D`) y aclara
el azul de marca a `#5BA3DC` para sostener el contraste. No es una paleta
distinta, es la misma rotada.

---

## 3. Tipografía

Tres familias, cada una con un trabajo. Están **autoalojadas** en
`static/fonts/` (116 KB en total): la CSP solo admite `'self'` en `font-src` y,
además, un portal público no debería derivar una petición por visita a un
tercero. Las tres son de licencia SIL Open Font License 1.1.

| Familia | Token | Dónde se usa |
|---|---|---|
| **Source Serif 4** | `--lectura` | Titulares y todo texto de lectura extensa |
| **Archivo** | `--display` | Interfaz: navegación, botones, tablas, etiquetas, campus |
| **IBM Plex Mono** | `--dato` | **Solo datos**: resoluciones, legajos, fechas, notas, códigos de mesa |

### 3.1 Por qué serif en los titulares

Es la decisión más visible y la más deliberada. Una grotesca pesada en tamaños
grandes produce un titular de cartel; la serif produce un titular de documento,
que es lo que corresponde a una institución educativa. Además, el molde por
defecto de cualquier sitio generado automáticamente es sans en todo: la serif es
lo que hace que este portal no se parezca a esos.

### 3.2 La monoespaciada va a dieta

`--dato` se reserva para valores que alguien podría copiar, comparar o citar:
una resolución, un legajo, una nota, una fecha. **Nunca para etiquetas.** Poner
«CIERRE DE PREINSCRIPCIÓN» en monoespaciada mayúscula con tracking ancho es
estética de terminal de los noventa, y fue exactamente el error que hubo que
corregir en la primera versión del rediseño.

### 3.3 Escala

| Clase | Tamaño | Uso |
|---|---|---|
| `.titular-mayor` | `clamp(2.5rem, 5.6vw, 4.6rem)` | Un solo `h1` por página |
| `.titular` | `clamp(1.7rem, 3vw, 2.4rem)` | Encabezado de sección |
| `.titular-menor` | `1.2rem` | Subsección |
| `.prosa` | `1.125rem` / interlínea 1.62 | Texto largo, máximo 62 caracteres por línea |
| `.dato` | `0.78rem` | Valores, con cifras tabulares |

---

## 4. Forma y espacio

- **Radio:** `--radio-xs` 4px (controles chicos), `--radio` 8px (botones,
  tarjetas), `--radio-lg` 14px (paneles). Lo justo para no parecer un formulario
  impreso, lo poco para no parecer una tarjeta de SaaS.
- **Ritmo vertical de 4px:** `--e1` a `--e9` (4, 8, 12, 16, 24, 32, 48, 72,
  112px). Todo margen y relleno sale de esa escala; no se escriben valores
  sueltos.
- **Ancho máximo:** 1280px, con 24px de aire lateral (16px en teléfono).
- **Grilla de 12 columnas.** Composición asimétrica: el contenido suele ocupar
  las columnas 1 a 8 y los datos auxiliares las 9 a 12. Nada se centra por
  defecto.

### 4.1 Alineación en tarjetas

Las tarjetas alinean su contenido **a la izquierda**, no al centro. El centrado
solo se usa dentro de un marco de fotografía pendiente, donde el rótulo es el
único contenido. Una tarjeta con título, texto y enlace centrados obliga al ojo
a buscar el inicio de cada línea.

Cada tarjeta mantiene **un único ritmo vertical**: `--e4` entre bloques grandes
(imagen y cuerpo) y `--e2` entre líneas del mismo bloque. Las tarjetas de una
misma fila se alinean al tope y empujan su acción al pie con `margin-top: auto`,
de modo que los enlaces queden a la misma altura aunque los textos midan
distinto.

---

## 5. Componentes con regla propia

### 5.1 Marcador de sección

Número + nombre sobre una regla fina (`.marcador`). **Reemplaza a la pastilla de
color centrada** que usa cualquier plantilla genérica. El número va en
`--azul-500` y da al visitante una noción de avance dentro de la página.

### 5.2 Botones

Un primario sólido por pantalla y el resto con borde. El sólido usa `--verde`
—que en esta paleta apunta a `--azul-600`— con sombra sutil, y se eleva 1px al
pasar el mouse. **No hay un tercer nivel de botón:** si hacen falta tres
jerarquías en una misma vista, el problema es la vista.

### 5.3 Marca de sede

Punto de color + nombre (`.sede-marca`). Cada sede tiene su tono dentro de la
escala azul, salvo Vicente López que usa `--aviso` por ser anexo. Permite
reconocer dónde se cursa una carrera sin leer el texto completo.

### 5.4 Interruptor de tema

Los dos símbolos —sol y luna— quedan **siempre visibles** y el carro se desplaza
al activo. El estado se lee por posición, no solo por color, que es lo que
necesita alguien con dificultad para distinguir tonos. Lleva `role="switch"` y
`aria-checked`.

### 5.5 Nombres heredados en el código

Los tokens `--verde` y `--oro` vienen de una etapa anterior del rediseño y hoy
apuntan al azul de marca y al de acento. Se conservan para no reescribir cada
regla del sistema. **Al escribir CSS nuevo conviene usar `--azul-600` y
`--azul-500` directamente**; los alias quedan por compatibilidad y se retirarán
cuando no queden usos.

---

## 6. Dos sistemas conviviendo

Durante la migración hay dos hojas de estilo:

| Sistema | Archivo | Lo usan |
|---|---|---|
| **Institucional** | `static/css/sistema.css` | Portada, carreras, detalle de carrera, campus |
| **Heredado** | `static/css/src/tokens.css` → `index.css` | El resto de las páginas |

Los tokens `--dm-*` del sistema heredado **fueron retiñidos a esta misma
paleta**. Así, una página todavía sin migrar adopta los colores de marca sin
tocar su marcado, y la unificación visual no queda esperando a que se reescriba
cada plantilla. La migración completa sigue siendo el objetivo; el retiñido es
el puente.

---

## 7. Accesibilidad

- **Contraste:** texto principal y enlaces cumplen AA. Los tres colores
  semánticos están elegidos para cumplirlo sobre blanco y sobre navy.
- **Foco visible:** contorno de 2px en `--verde` con 2px de separación. No se
  elimina nunca.
- **El color no es el único canal:** todo estado lleva texto además de color.
- **Movimiento:** cada transición se desactiva bajo
  `prefers-reduced-motion: reduce`.
- **Enlaces externos:** los direccionales a Google Maps llevan
  `rel="noopener noreferrer"` y un texto para lector de pantalla que aclara que
  se abre en otro sitio.

---

## 8. Qué está pendiente

- **Fotografía institucional.** Los espacios están reservados con sus
  proporciones definitivas; la guía de toma está en
  [docs/rediseno/README.md](../rediseno/README.md), sección 4.
- **Migrar las páginas restantes** al sistema institucional: contacto,
  novedades, materias, páginas de error y panel.
- **Retirar los alias `--verde` / `--oro`** cuando no queden usos.
- **Verificación de contraste con herramienta** sobre las dos variantes de tema.
