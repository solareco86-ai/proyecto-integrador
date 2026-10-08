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
| Sin degradados; escala de radio de 4, 8 y 14px | Lo justo para no parecer un formulario impreso, lo poco para no parecer una tarjeta de SaaS |
| Sombras teñidas de marrón, nunca de negro | Una sombra negra sobre base cálida la ensucia y la vuelve gris |
| **Source Serif 4** para titulares y texto extenso | Registro de documento académico; además, la sans es el molde de todo sitio generado |
| **Archivo** para interfaz, navegación y tablas | Refuerza la distinción entre el sitio que informa y la herramienta que gestiona |
| **IBM Plex Mono** solo para datos | Resoluciones, legajos, fechas y notas con cifras tabulares. Nunca para etiquetas |
| Verde y oro del escudo, planos y escasos | Color institucional como señal, no como decoración |
| Marcadores de sección numerados sobre una regla clara | Reemplazan la pastilla centrada de color |
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
6. **La sede aparece junto a cada carrera.** El instituto dicta en tres sedes y
   cada tecnicatura se cursa en una sola: es un dato que condiciona la decisión
   tanto como el plan de estudios, y hoy el sitio no lo dice en ninguna parte.

### 2.3 Sedes y distribución de la oferta

| Sede | Domicilio | Carreras que se dictan |
|---|---|---|
| **El Talar** | Maestra Celina Voena 1750, El Talar, Partido de Tigre | Logística · Higiene y Seguridad · Turismo · Hotelería |
| **Los Troncos** | Libertador Gral. San Martín 436, esquina Alte. Brown, Los Troncos del Talar, Partido de Tigre | Ciencia de Datos e IA · Administración de Recursos Humanos |
| **Virreyes** | *Pendiente de confirmación*, Virreyes, Partido de San Fernando | Mecatrónica |

Dato aportado por la cátedra en octubre de 2026. **Dos discrepancias con el
contenido publicado**, a resolver antes de migrar:

- El sitio actual publica Los Troncos en **Alte. Brown 739**; el dato aportado es
  **Libertador Gral. San Martín 436, esquina Alte. Brown**. El prototipo usa el
  segundo.
- El sitio actual publica un **Anexo Vicente López** (Cerrito 3966) que no figura
  en la distribución aportada. El prototipo no lo incluye.

Al tratarse de domicilios oficiales, ninguno de los dos puntos se lleva a
`data/` sin confirmación de Secretaría.

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

## 4. Guía de fotografía

El sitio no tiene una sola fotografía, y eso explica buena parte de por qué se
lee como un documento y no como el lugar donde se estudia. El prototipo reserva
cinco espacios con el encuadre y la proporción ya definidos: cuando lleguen las
fotos solo se reemplaza el contenido del marco.

### Reglas comunes a todas

- **Horizontal, salvo donde se indique.** Una foto vertical no entra en los
  marcos anchos y obliga a recortar lo importante.
- **Al anochecer, entre las 18:00 y las 20:00.** La cursada es vespertina: las
  ventanas iluminadas sobre cielo todavía azul son la imagen más honesta del
  instituto y la más favorecedora. Es la llamada «hora azul» y dura unos 25
  minutos, así que conviene llegar antes y esperar.
- **Luz disponible, sin flash directo.** El flash del teléfono aplana todo y
  produce el aspecto de foto de trámite.
- **Encuadrar más amplio de lo necesario.** Después se recorta; agregar no se
  puede. Mínimo 2400px de ancho.
- **Cuidado con las personas.** Si se ven caras identificables hace falta
  consentimiento por escrito. Lo más simple es fotografiar de espaldas, manos
  trabajando, o planos donde la gente aparezca de lejos o desenfocada.
- **Nada de posar.** Que la gente esté haciendo lo que hace. Una clase mirando a
  cámara se nota, y se nota mal.

### Las cinco tomas

| # | Dónde va | Proporción | Qué fotografiar |
|---|---|---|---|
| 1 | Portada, banda bajo el titular | 21:8 (muy apaisada) | **Fachada del instituto al anochecer.** Plano general con las aulas iluminadas y, si se puede, gente entrando. Es la primera imagen del sitio y la que más pesa. Pararse enfrente, cruzando la calle, para que entre el edificio completo. |
| 2 | Las sedes, columna 1 | 4:3 | **Frente de la sede El Talar**, con el cartel institucional visible. |
| 3 | Las sedes, columna 2 | 4:3 | **Frente de la sede Los Troncos.** Mismo encuadre y misma distancia que la anterior. |
| 4 | Las sedes, columna 3 | 4:3 | **Frente de la sede Virreyes.** Mismo encuadre que las otras dos. |
| 5 | Detalle de carrera, bajo el titular | 16:9 | **Un aula o laboratorio de esa carrera en uso.** Una foto distinta por tecnicatura: la sala de informática con las máquinas encendidas para Ciencia de Datos, el laboratorio con los PLC para Mecatrónica, y así. |

Las tres fotos de sede (2, 3 y 4) **tienen que estar tomadas igual**: misma
distancia, misma altura y a la misma hora del día. Van una al lado de la otra y
cualquier diferencia de encuadre o de luz se nota de inmediato y desprolija la
fila. Lo más práctico es hacer las tres el mismo día.

Formato: JPEG o WebP, el original sin recortar. El recorte a cada proporción se
hace después, en el proyecto.

---

## 5. Trabajo pendiente

- [x] Ajuste de la dirección visual sobre la estructura aprobada.
- [ ] **Fotografía institucional**: las cinco tomas de la sección 4. Los espacios
      ya están reservados en el prototipo.
- [ ] **Confirmar en Secretaría** el domicilio de Los Troncos, la dirección de
      Virreyes y la vigencia del anexo de Vicente López (sección 2.3).
- [x] **Migración de la portada** a las plantillas Jinja, con el sistema servido
      desde `static/css/sistema.css` y las tipografías autoalojadas en
      `static/fonts/`. La portada sale del shell heredado mediante los bloques
      `shell_class` / `main_class` de `base.html`.
- [ ] Migrar el resto de las páginas: listado y detalle de carreras, campus,
      páginas de error y panel. Hasta entonces conservan el sistema anterior y
      los partials `header.html` / `footer.html`.
- [ ] Unificar el partial de preguntas frecuentes: hoy el estilo nuevo se acota
      con `.capa-institucional` para no afectar a `pricing.html` ni `preview.html`.
- [ ] Unificación de las plantillas que quedaron con el tema heredado
      (hallazgo 1.1), en una rama propia.
- [ ] Corrección de los accesos comerciales de la página 404 (hallazgo 1.2), en
      una rama propia.
- [ ] Pruebas con lector de pantalla y verificación de contraste en ambos temas.
