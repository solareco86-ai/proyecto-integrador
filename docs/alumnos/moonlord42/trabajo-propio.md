# Trabajo propio

Registro de lo que hice en el Proyecto Integrador y en el generador de actas, con la evidencia de cada
parte (PRs, issues y commits). Es el documento de N3.

## Cómo trabajé

- **Con un asistente de IA.** Programé con Claude Code, como permite `AGENTS.md`. Los commits hechos así
  llevan la línea `Co-Authored-By: Claude`, así que se distinguen en el historial.
- **Lo que hice yo:** definir qué hacer y para quién, decidir entre alternativas, revisar el resultado
  en el navegador, pedir cambios y llevar cada parte hasta un PR.
- **Probar antes de dar algo por hecho.** Cada PR pasa la puerta de control (`scripts/pre-push.sh`)
  y además lo reviso en el navegador, en claro, en oscuro y a ancho de celular.

## 1. Generador de actas de examen (proyecto propio)

[isft199datos.vercel.app](https://isft199datos.vercel.app) ·
repo [MoonLord42/isft199datos](https://github.com/MoonLord42/isft199datos)

**Problema.** Antes de cada turno de mesas, Secretaría armaba a mano más de 200 actas volantes,
copiando alumnos del Forms de inscripción a la plantilla.

**Qué hice.**

| Fecha | Qué | Evidencia |
|---|---|---|
| 5-nov-2026 | Primera versión: lee el Forms, la planilla de Materias y el acta volante, y devuelve un ZIP con un acta por materia, sección y llamado. Todo corre en el navegador: los datos de los alumnos no se suben a ningún servidor. | Commits iniciales del repo |
| 17-nov-2026 | 38 tests automáticos (5 de texto, 14 de reglas, 17 de punta a punta y 2 de arquitectura), con cobertura mínima del 85 % (hoy 99,5 % de líneas) y GitHub Actions en cada PR. Los Excel de prueba se arman con datos inventados. | Issue #1 · PR #2 |
| 17-nov-2026 | Arquitectura en capas: reglas del negocio puras (`js/dominio/`), lectura y escritura de Excel (`js/excel/`) y coordinación (`js/actas.js`). Un test falla si el dominio importa una librería de Excel o del navegador. | Issue #3 · PR #4 |

**Resultado.** Secretaría ya la usa. Con las inscripciones de agosto de 2026 procesó 304 respuestas
y 864 inscripciones, y armó 213 actas en unos 40 segundos.

**Cómo verifiqué el cambio a capas.** Comparé celda por celda las actas del código viejo contra las del
nuevo con los mismos archivos: salieron iguales. También introduje errores a propósito para confirmar
que los tests los detectan.

**Documentación.** [SRS](srs-actas.md), [Canvas](canvas.md) y [caminos de ingreso](caminos-de-ingreso.md).

## 2. Rediseño del portal institucional (este repo)

| PR | Estado | Qué hice |
|---|---|---|
| #16 | Fusionado | Auditoría UX/UI del sitio y prototipo navegable de 4 pantallas en `docs/rediseno/`. Detecté, entre otras cosas, que la página 404 ofrecía servicios comerciales de DataMaq y que la gratuidad no aparecía en la primera pantalla. |
| #30 | Fusionado | Ajuste visual del prototipo después de la devolución («muy cuadrado, genérico»): escala de radios y sombras, serif en los titulares y mono solo para datos. |
| #31 | Fusionado | Primera migración real: la portada pasa al sistema de diseño nuevo (`sistema.css`, tipografías autoalojadas sin tocar la CSP). Saqué de la plantilla el catálogo de carreras y los domicilios, que estaban escritos a mano, y los pasé a `data/`, con un test que lo controla. |
| #33 | Cerrado | Las otras tres pantallas, una paleta nueva y datos de sedes. Quedó demasiado grande (40 archivos) y se cruzó con lo que fusionaron después #54 y #55. Lo dividí en #92 a #96. |
| #62 | Fusionado | A pedido del instituto, «preinscripción» pasa a «consultas» y el correo a isft199consultas@gmail.com en todo el sitio. |
| #92 | Abierto | Pantalla `/campus` con datos de muestra, solo en modo desarrollo. |
| #93 | Abierto | Comparador de las carreras dentro del listado que rehicieron #54 y #55. |
| #94 | Abierto | Rediseño del detalle de carrera, que seguía con el diseño viejo. |
| #95 | Abierto | Cuenta regresiva del cierre de inscripción, calculada en vivo con la hora argentina. |
| #96 | Abierto | «Cursos» pasa a «materias» en los rótulos, sin cambiar las rutas. |

### Decisiones al dividir el #33

- **Colores:** usé los de `develop` (#55), porque los directivos no aprobaron la versión toda azul.
  Descarté mi paleta.
- **Datos de sedes y carreras:** quedan los de `develop` (#54) hasta confirmarlos con Secretaría.
- **Listado de carreras:** sumé solo el comparador para no pisar el trabajo de mis compañeros.
- **Espacios de fotos:** no los subí, porque en producción se verían como recuadros vacíos.
- **Arreglos que encontré al probar:**
  - los estilos del campus estaban copiados tres veces;
  - el campus se desbordaba en el celular;
  - la cuenta regresiva restaba un día de 21 a 24 h porque usaba la hora UTC;
  - la barra lateral del detalle mostraba la misma sede para todas las carreras.

## 3. Lo que sigue

- Que se revisen y fusionen los PRs #91 a #96.
- Confirmar con Secretaría las sedes y qué carreras se dictan en cada una, y proponerlo en un PR aparte.
- Para 2027, sumar al generador la inscripción a materias, con su propio SRS (ver [SRS, sección 8](srs-actas.md#8-próximos-pasos)).
