# Business Model Canvas: Sistema de asignación de aulas

Este Canvas describe cómo el sistema podría aportar valor a instituciones educativas y convertirse en un servicio profesional. El MVP actual trabaja con datos sintéticos y archivos CSV; Excel, PDF e interfaz quedan como etapas posteriores.

## Canvas de nueve bloques

| Bloque | Definición para el proyecto |
|---|---|
| **Socios clave** | Instituciones educativas; equipos de secretaría y coordinación académica; proveedores de alojamiento; eventualmente proveedores de conversión XLSX/PDF. |
| **Actividades clave** | Cargar y validar datos; detectar conflictos de capacidad, recursos y horarios; generar asignaciones reproducibles; exportar resultados y grafos; mantener reglas configurables. |
| **Recursos clave** | Algoritmo de matching; contrato de datos; código Python; reglas de negocio; datos sintéticos o institucionales autorizados; documentación y pruebas automatizadas. |
| **Propuesta de valor** | Reducir errores de asignación manual y mostrar una propuesta explicable de aulas, indicando también las sesiones que no pudieron asignarse y el motivo. |
| **Relación con clientes** | Inicialmente acompañamiento y revisión humana: el sistema propone, pero la institución valida la decisión. En una etapa posterior podría ofrecerse autoservicio con historial de ejecuciones. |
| **Canales** | Repositorio GitHub, demostración académica, contacto directo con instituciones y, en una futura etapa, una API o interfaz web para cargar archivos. |
| **Segmentos de clientes** | Institutos terciarios, colegios y universidades con varias comisiones, aulas limitadas, laboratorios o bibliotecas y planificación vespertina. El usuario operativo sería la secretaría o coordinación académica. |
| **Estructura de costos** | Desarrollo y mantenimiento; alojamiento; soporte y configuración inicial; adaptación del contrato de datos; capacitación; almacenamiento de archivos si se agrega una plataforma web. |
| **Fuentes de ingresos** | Servicio de implementación y configuración; suscripción institucional; soporte y mantenimiento; o relación laboral como desarrolladora/analista de sistemas académicos. Para la evolución comercial se prioriza comenzar con un servicio de implementación, no con un SaaS multiinstitución. |

## Problema y propuesta de valor

La planificación manual puede reutilizar un aula en una misma franja, ignorar la capacidad disponible o no detectar que dos materias compiten por el único laboratorio. El sistema procesa los datos institucionales, explica los errores, propone una asignación y deja la decisión final en manos de la institución.

## Usuarios, comprador y decisión humana

- **Usuario operativo:** secretaría, coordinación académica o responsable de horarios.
- **Comprador o decisor:** dirección, rectorado o administración de la institución.
- **Beneficiario indirecto:** docentes y estudiantes, porque reciben una planificación con menos cambios y conflictos.
- **Supervisión humana:** la salida es una propuesta; una persona debe revisarla antes de publicarla.

## Modelo de ingresos elegido para el MVP

El MVP no cobra ni procesa pagos. Como proyección profesional, la alternativa más realista es ofrecer **implementación y configuración del sistema para cada institución**, con soporte posterior. Esto permite adaptar días, horarios, tipos de aula y requerimientos sin afirmar todavía que existe un producto SaaS terminado.

La alternativa laboral también es válida: el proyecto demuestra competencias aplicables a puestos de desarrollo backend, análisis de datos y optimización de procesos institucionales.

## Página complementaria: caminos de ingreso

La experiencia del proyecto puede convertirse en un ingreso por dos caminos. Se elige como principal el camino comercial, porque permite ofrecer una solución concreta a varias instituciones sin afirmar que todavía existe un producto SaaS terminado.

| Camino | Puesto o servicio | A quién | Qué se ofrecería |
|---|---|---|---|
| **Relación laboral** | Desarrolladora backend, analista de datos o analista de sistemas académicos | Institutos, universidades, colegios, empresas EdTech o áreas de sistemas | Diseñar, mantener y mejorar sistemas de planificación, validación y análisis de datos educativos. |
| **Comercial — camino elegido** | Servicio de implementación y configuración de asignación de espacios | Institutos terciarios, colegios y universidades con aulas limitadas o recursos especiales | Adaptar el contrato de datos, configurar reglas institucionales, ejecutar el análisis, entregar la propuesta de asignación y brindar soporte. |

### Justificación del camino elegido

Se elige inicialmente el servicio comercial de implementación porque el problema cambia según cada institución: pueden variar los días, horarios, tipos de aula, equipamiento y formato de los archivos. Un servicio de configuración permite validar esas diferencias antes de convertir el proyecto en una plataforma general o en un SaaS multiinstitución.

La primera oferta no incluiría cobro automático ni prometería una asignación óptima. Incluiría diagnóstico de datos, configuración, ejecución, informe de conflictos y acompañamiento de una persona responsable de la institución.

## Hipótesis a validar

1. La institución dispone de archivos de aulas y comisiones con información suficiente para aplicar el contrato.
2. La propuesta explicable resulta más útil que una asignación manual sin trazabilidad.
3. El tiempo de revisión disminuye sin quitar la decisión final al personal académico.
4. Las reglas de cada institución pueden configurarse sin modificar la lógica central.

## Fuera de alcance actual

- Cobro, suscripciones o comercialización real.
- Procesamiento de datos personales reales sin autorización.
- Generación automática de horarios.
- Integración con sistemas administrativos.
- Excel/XLSX, PDF e interfaz web; se consideran futuras etapas.

