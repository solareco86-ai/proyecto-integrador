# Auditoría UX/UI y propuesta de rediseño del portal

> **Estado:** Propuesta en revisión. No modifica el sitio en producción.
> **Alcance:** Portal institucional público y campus virtual.
> **Fecha:** Octubre de 2026.

Este documento reúne una auditoría de la interfaz actual y una propuesta de
dirección visual y de contenido. El prototipo navegable que la acompaña está en
[prototipo/](prototipo) y es HTML y CSS estáticos: no toca `templates/`, `src/`
ni `static/`, y no interviene en el pipeline de build.

## Cómo ver el prototipo

```bash
cd docs/rediseno/prototipo && python3 -m http.server 8012
```

Cuatro pantallas: `index.html` (portada), `carreras.html` (listado y comparador),
`carrera.html` (detalle de carrera) y `campus.html` (campus del estudiante).
El conmutador de tema claro/oscuro está arriba a la derecha.

Para comparar contra el sitio actual, levantar el proyecto en paralelo con
`python run.py` y abrir ambos puertos.

---

## 1. Hallazgos de la auditoría

La auditoría se hizo sobre el sitio corriendo en local (commit `f539217`),
recorriendo portada, listado de carreras, detalle de carrera, campus, formulario
de contacto, panel y página de error.

### 1.1 Conviven dos sistemas visuales distintos

`InstitucionalHome.css` —la identidad institucional nueva— lo cargan únicamente
tres plantillas: `index.html`, `carreras.html` y `contact.html`.

El resto del sitio cae al tema heredado de DataMaq: fondo azul oscuro, con el
encabezado sin estilar y los ítems del menú superpuestos. Afecta a:

- `templates/carrera_detail.html` — el detalle de cada tecnicatura
- `templates/404.html` y `templates/500.html`
- `templates/panel/` — el panel de autoridades

**Impacto:** quien entra a `/carreras` y hace clic en "Ver detalles" aterriza en
una página que parece de otro sitio. Es el recorrido principal de un aspirante.

**Causa:** el rediseño institucional se hizo plantilla por plantilla y las hojas
de estilo nuevas se sumaron solo donde se trabajó. No es un problema de build ni
de purga de Tailwind.

### 1.2 La página 404 ofrece contenido comercial de DataMaq

`templates/404.html` presenta accesos rápidos a "Factor de Potencia (cos φ)",
"Telemetría & Retrofit IoT", **"Precios y Financiamiento"** y "Cursos Gratuitos".

En el portal de una institución pública y gratuita, una página de error que
ofrece precios y financiamiento contradice la certeza **C-17** del
[roadmap](../todo.md) y la regla de gratuidad total de [AGENTS.md](../../AGENTS.md)
(sección 7.1). Conviene corregirlo con independencia de este rediseño.

### 1.3 El titular de la portada no comunica nada verificable

> "Formación técnica de excelencia para el futuro laboral y productivo de Tigre"

Es una frase aplicable a cualquier institución del país. Mientras tanto, los dos
datos que una persona viene a buscar están ausentes o escondidos:

| Dato | Dónde está hoy |
|---|---|
| La carrera es gratuita | Dentro de un acordeón de preguntas frecuentes, al final de la portada |
| Fechas de inscripción | No figura en ninguna parte del sitio |

### 1.4 Siete tarjetas idénticas para siete carreras que comparten casi todo

Las siete tecnicaturas tienen la misma duración (3 años), modalidad (presencial)
y turno (vespertino). La grilla de tarjetas obliga a leer siete veces los mismos
atributos para encontrar la única diferencia real, que es el campo de trabajo.
Además las tarjetas quedan con alturas desparejas y todas repiten el mismo ícono
de tilde, que no aporta información.

### 1.5 La interfaz tiene las marcas del diseño generado sin decisiones

Hero con degradado azul-verde, pastilla centrada en mayúsculas sobre cada título
de sección, títulos centrados con subtítulo gris, filas de tres tarjetas con
ícono circular, sombras suaves generalizadas, botón flotante de teléfono y un
ítem de menú con la leyenda "PRÓXIMAMENTE".

---

## 2. Dirección propuesta

La hipótesis: **un instituto público se parece más a un documento oficial bien
hecho que a un producto SaaS.** La jerarquía la construyen la tipografía y las
reglas, no las tarjetas y las sombras.

### 2.1 Decisiones del sistema

| Decisión | Fundamento |
|---|---|
| Base de papel cálido (`#F6F3EC`) en lugar de gris azulado | Separa la identidad del molde "producto tecnológico" |
| Sin degradados ni sombras; borde de 1px y radio de 2px | La jerarquía queda a cargo de la tipografía |
| **Archivo** para títulos e interfaz | Tipografía de Omnibus-Type, fundidora de Buenos Aires |
| **Source Serif 4** para texto extenso | Registro de documento académico |
| **IBM Plex Mono** para datos | Resoluciones, legajos, fechas y notas con cifras tabulares |
| Verde y oro del escudo, planos y escasos | Color institucional como señal, no como decoración |
| Marcadores de sección numerados sobre una regla | Reemplazan la pastilla centrada de color |
| Listas y tablas en lugar de grillas de tarjetas | Siete carreras con atributos comunes son una tabla |

Los tokens están en [prototipo/css/sistema.css](prototipo/css/sistema.css), con
tema claro y oscuro completos.

### 2.2 Decisiones de contenido

1. **La portada abre con el estado de admisión**, no con un eslogan: titular
   factual, días restantes para la preinscripción y la lista de documentación.
2. **La gratuidad sube a la primera pantalla.** Es el argumento más fuerte de la
   institución y hoy está escondido en un acordeón.
3. **Las carreras se comparan en una tabla**, porque el usuario está eligiendo
   entre siete opciones casi equivalentes.
4. **El campus no se parece al sitio público.** El sitio informa; el campus es
   una herramienta de gestión: mayor densidad, cifras tabulares, estado siempre
   visible y los vencimientos arriba de todo.
5. **No se inventa plan de estudios.** El detalle de carrera muestra los ejes de
   contenido cargados en `data/content/carreras.yaml` y aclara que el plan
   completo lo fija la resolución correspondiente, en cumplimiento de la regla de
   veracidad académica de [AGENTS.md](../../AGENTS.md) (sección 7.5).

---

## 3. Origen de los datos del prototipo

| Dato | Origen |
|---|---|
| Carreras, resoluciones, materias, perfiles y salida laboral | `data/content/carreras.yaml` |
| Domicilio, teléfono, correos y horarios | Sitio actual y `AGENTS.md` |
| Escudo institucional | `static/media/logo-isft199.webp` |
| Fechas de inscripción, días restantes, novedades y **todo el contenido del campus** | **Inventado para la maqueta** (ver señalización abajo) |

Ningún dato curricular del prototipo fue inventado. Los resúmenes por carrera son
versiones condensadas de `description_short` y los distintivos coinciden con
`badge` de `carreras.yaml`.

### Señalización de los datos de ejemplo

Cada pantalla abre con una banda «Prototipo de rediseño · no es el sitio
oficial». Además, el dato inventado lleva su propia etiqueta «ejemplo» al lado:
el estado de admisión y la fecha de cierre en la portada, la sección «Vida
institucional» y el pie del campus. La cuenta regresiva está escrita a mano y no
se actualiza.

**Regla de migración:** ninguna fecha, plazo, novedad ni cifra del prototipo se
copia a `templates/` o a código. En el sitio real esos datos viven en `data/` y
requieren una fuente oficial (`AGENTS.md`, secciones 3 y 7.5). Mientras no exista
esa fuente, el sitio no publica fechas de inscripción.

Dos tests lo hacen cumplir: `tests/test_prototipo_rediseno.py` comprueba la
banda y las etiquetas de ejemplo en las cuatro pantallas, y
`tests/test_resoluciones_consistentes.py` exige que los números de resolución
del prototipo, el README y los documentos públicos coincidan con `carreras.yaml`.
`tests/test_oferta_carreras_consistente.py` hace lo mismo con la lista de carreras
(README, `llms*.txt`, JSON-LD del home y el conteo del texto del home).

---

## 4. Trabajo pendiente

- [ ] Ajuste de la dirección visual. La estructura está aprobada; el acabado
      gráfico está en revisión.
- [ ] Migración del sistema a las plantillas Jinja y a Tailwind v4 con prefijo
      `tw:`, una vez cerrado el punto anterior.
- [ ] Unificación de las plantillas que quedaron con el tema heredado
      (hallazgo 1.1), en una rama propia.
- [ ] Corrección de los accesos comerciales de la página 404 (hallazgo 1.2), en
      una rama propia.
- [ ] Pruebas con lector de pantalla y verificación de contraste en ambos temas.
