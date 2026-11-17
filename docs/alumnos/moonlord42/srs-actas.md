# SRS · Generador de actas de examen

Especificación de requisitos del generador de actas del ISFT N° 199.

- Sitio: [isft199datos.vercel.app](https://isft199datos.vercel.app)
- Código: [MoonLord42/isft199datos](https://github.com/MoonLord42/isft199datos)

## 1. Propósito y alcance

Antes de cada turno de mesas, Secretaría arma a mano un acta volante por cada final: copia de las
respuestas del formulario de inscripción a la plantilla los alumnos de cada materia, sección y llamado.
Con más de 200 actas por turno, es mucho trabajo y es fácil equivocarse.

La herramienta recibe tres archivos Excel y devuelve un ZIP con todas las actas listas para imprimir.

**Queda fuera del alcance:**
- cargar notas;
- firmar las actas;
- guardar datos en un servidor;
- inscribir alumnos (eso sigue haciéndose con el Forms).

## 2. Usuarios

| Usuario | Qué hace |
|---|---|
| Personal de Secretaría | Sube los archivos, revisa los avisos e imprime las actas. No necesita saber de informática. |
| Preceptoría y docentes | Reciben el acta impresa de su mesa. No usan la herramienta. |

## 3. Entradas

| Archivo | Contenido | Datos que necesita |
|---|---|---|
| Inscripciones del Forms | Una fila por respuesta y una columna por materia con sección (ej. `S01A - Programación I`). La celda dice el llamado y la condición (ej. `1er llamado - REGULAR`). | DNI, apellido y nombre. Si están, también legajo, correo, carrera y marca temporal. |
| Materias | Una fila por unidad curricular. | Unidad curricular. Si están, también carrera, año, curso, profesor, fecha y fecha del 2º llamado. |
| Acta volante | La plantilla en blanco del instituto, de una o más páginas. | Rótulos «Carrera:», «Curso:», «Espacio Curricular:», «Presidente», «Fecha» y una tabla que empieza con «N°». |

## 4. Requisitos funcionales

| ID | Requisito |
|---|---|
| RF-01 | Leer los tres archivos `.xlsx` desde la computadora, eligiéndolos o arrastrándolos juntos. |
| RF-02 | Reconocer las columnas por su título, sin importar tildes, mayúsculas ni el orden. |
| RF-03 | Emparejar cada columna del Forms con su fila de Materias: primero por código y nombre, y si no coincide, solo por código. Esto hace falta porque el mismo código se repite entre planes (por ejemplo, L01A en el plan viejo y en el nuevo de Logística). |
| RF-04 | Armar un acta por materia, sección y llamado. Regular y libre salen en actas separadas, porque la plantilla tiene un solo campo de condición. |
| RF-05 | Completar la cabecera (carrera, curso, materia, condición, presidente y fecha) y la tabla de alumnos ordenada por apellido. |
| RF-06 | Usar la fecha del 2º llamado cuando el llamado es el segundo. |
| RF-07 | Si un alumno se inscribió dos veces en la misma materia y llamado, dejar la última respuesta. |
| RF-08 | Si un final tiene más alumnos que filas, dividirlo en varias actas («parte 1 de 2»). |
| RF-09 | Ocultar las páginas sobrantes de la plantilla y dejar el área de impresión solo sobre las páginas usadas. |
| RF-10 | Avisar qué revisar: inscripciones repetidas, alumnos sin DNI, materias que no están en Materias y actas sin presidente. |
| RF-11 | Entregar un ZIP con una carpeta por carrera y un `00 - Resumen.xlsx` con todas las actas y los avisos. |
| RF-12 | Si un archivo no es el correcto, mostrar un error que diga qué falta y en qué archivo. |

## 5. Requisitos no funcionales

| ID | Requisito |
|---|---|
| RNF-01 | **Privacidad:** los archivos se procesan en el navegador. No se suben a internet ni quedan guardados. |
| RNF-02 | **Rendimiento:** un turno completo (unas 900 inscripciones) se procesa en menos de un minuto en una computadora común. |
| RNF-03 | **Facilidad de uso:** una sola pantalla, en español, sin registro ni instalación. |
| RNF-04 | **Costo:** la página es estática, así que el alojamiento es gratuito y no hay servidor que mantener. |
| RNF-05 | **Calidad:** tests automáticos con cobertura de al menos 85 % de la lógica, que corren en cada PR. |
| RNF-06 | **Datos de prueba:** en el repo no se guardan Excel con datos reales de alumnos. |

## 6. Casos de uso

### CU-01 · Generar las actas de un turno

- **Actor:** personal de Secretaría.
- **Antes:** tiene las inscripciones del Forms, la planilla de Materias y el acta volante en `.xlsx`.

**Flujo principal**
1. Abre la página y elige o arrastra los tres archivos.
2. Toca «Generar actas».
3. La página muestra el avance y, al terminar, cuántas actas, inscripciones y respuestas leyó.
4. Descarga el ZIP.

**Flujos alternativos**
- **2a.** Un archivo no es `.xlsx`: la página pide descargarlo de Google Sheets como Excel.
- **2b.** Falta una columna o la tabla del acta: la página dice cuál falta y en qué archivo. No se genera nada.

**Después:** tiene una carpeta por carrera con las actas y el resumen.

### CU-02 · Revisar antes de imprimir

- **Actor:** personal de Secretaría.

**Flujo principal**
1. Lee los avisos: repetidas, sin DNI, materias que no están y actas sin presidente.
2. Abre el `00 - Resumen.xlsx` para ver todas las actas en una lista.
3. Corrige a mano las actas marcadas o corrige la planilla de origen y vuelve a generarlas.

### CU-03 · Imprimir un acta

- **Actor:** personal de Secretaría.

**Flujo principal**
1. Abre el acta en Excel o LibreOffice e imprime.

**Resultado:** salen solo las páginas con alumnos y cada página empieza en hoja nueva.

## 7. Criterios de aceptación

Cada criterio tiene un test automático en
[`tests/actas.test.js`](https://github.com/MoonLord42/isft199datos/blob/main/tests/actas.test.js).

| Requisito | Criterio | Test |
|---|---|---|
| RF-04, RF-05 | Con 2 alumnos en el 1er llamado regular de una materia, sale 1 acta con la cabecera completa y los alumnos ordenados por apellido. | «arma un acta por materia y llamado…» |
| RF-04 | Un alumno regular y otro libre en la misma materia generan 2 actas. | «regular y libre salen en actas separadas» |
| RF-06 | En el 2º llamado, la fecha del acta es la del 2º llamado. | «el 2º llamado usa la fecha…» |
| RF-03 | Con L01A en dos planes, el acta toma el profesor de la materia con el mismo nombre. | «si el código se repite entre planes…» |
| RF-03 | Con el nombre mal escrito en el Forms, empareja por código y usa el nombre oficial. | «con el nombre mal escrito…» |
| RF-07, RF-10 | Dos respuestas del mismo DNI quedan en 1 alumno con los datos de la última, y se avisa. | «una inscripción repetida…» |
| RF-08 | Con 7 alumnos y lugar para 6, salen 2 actas («parte 1 de 2» y «parte 2 de 2»). | «con más alumnos que filas…» |
| RF-09 | Con 1 alumno, la página 2 queda oculta y el área de impresión termina en la firma de la página 1. | «si sobra la página 2…» |
| RF-10 | Se avisan las materias sin profesor, las que no están en Materias y los alumnos sin DNI. | «avisa cuando la materia no tiene profesor…» |
| RF-11 | El ZIP trae `00 - Resumen.xlsx` con una fila por acta y la hoja de avisos. | «el ZIP trae el resumen…» |
| RF-12 | Con un archivo equivocado, el error dice qué columna o tabla falta. | 5 tests «error claro si…» |
| RNF-05 | La cobertura de `js/actas.js` es de al menos 85 %. Hoy está en 98,7 % de líneas. | `npm test` en GitHub Actions |
