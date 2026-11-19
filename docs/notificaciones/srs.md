# Especificación de Requerimientos de Software (SRS)
## Sistema de notificaciones del campus — ISFT N.º 199

**Autor:** Lautaro Amengual (`amengual-ln`)  
**Versión:** 1.0 — 17/11/2026  
**Ámbito:** Módulo de notificaciones personales del campus, con bandeja, suscripciones e historial.  
**Estado:** Reconstrucción documental de una propuesta discontinuada.

Este documento se elaboró el 17/11/2026 a partir de las issues de planificación creadas el 16/10/2026. Describe el alcance que se había propuesto; no acredita una especificación aprobada en esa fecha ni una implementación terminada. El campus fue discontinuado y las issues #44–#49 se cerraron como no planificadas. Se conserva esta especificación como evidencia del análisis de requisitos y del cambio de alcance.

## 1. Contexto y propósito

El módulo propuesto buscaba comunicar a los destinatarios pertinentes las publicaciones de noticias, eventos y comunicados, y los eventos de una preinscripción válida. Las notificaciones iban a vivir en el campus y podían complementarse con email y Telegram. El objetivo era permitir consultar avisos personales, configurar suscripciones y conocer los resultados de entrega.

Según el relevamiento registrado en las issues, ya existían adaptadores de email y Telegram para alertas internas de leads/contactos a destinatarios fijos. Ese flujo no equivalía a un sistema de notificaciones personales. Tampoco se había definido un flujo propio de preinscripción: un contacto o lead no debía tratarse automáticamente como preinscripto.

Se toma como referencia la organización del [SRS general del portal](https://github.com/solareco86-ai/proyecto-integrador/blob/main/docs/srs.md), pero esta especificación se limita al módulo de notificaciones. No reemplaza ni valida los datos académicos del documento general.

## 2. Actores, alcance y dependencias

| Actor o parte interesada | Participación prevista |
|---|---|
| Destinatario autenticado del campus | Consultar su bandeja, marcar avisos como leídos y gestionar las preferencias autorizadas. |
| Responsable de publicar contenido | Publicar noticias, eventos o comunicados mediante los circuitos existentes. |
| Aspirante/preinscripto | Posible destinatario de avisos de preinscripción; reglas pendientes de definición. |
| Personal autorizado | Consultar el historial administrativo, si se aprobaba ese panel. |
| Coordinación y referente institucional | Definir destinatarios, obligatoriedad, permisos y consentimiento. |
| Responsable técnico propuesto | Lautaro Amengual: analizar e implementar el alcance una vez aprobado. |
| Servicios externos de email y Telegram | Transportar mensajes y devolver resultados de entrega. |

### 2.1 Alcance propuesto

- Definición funcional de eventos, destinatarios y canales.
- Persistencia de notificaciones personales, lectura e intentos de entrega.
- Disparadores de primera publicación y de preinscripción válida.
- Suscripciones y entrega por email y Telegram.
- Bandeja in-app y, sujeto a aprobación, panel administrativo de historial.

### 2.2 Fuera de alcance

Push móvil, SMS, WhatsApp saliente, métricas avanzadas de apertura/clic, actualización por WebSocket y un nuevo broker de mensajes. También quedaban fuera la implementación autónoma de un circuito de preinscripción y la conversión automática de leads en suscriptores.

### 2.3 Decisiones previas pendientes — #44

Antes de implementar se debía aprobar una especificación con:

1. Matriz de evento × destinatario y permisos.
2. Destinatarios de la preinscripción: Secretaría, aspirante o ambos.
3. Regla ante actualizaciones de contenido ya publicado.
4. Notificaciones obligatorias y opcionales; valores iniciales de preferencias.
5. Admisión o exclusión de suscriptores públicos sin cuenta de campus.
6. Mecanismo seguro para vincular y desvincular Telegram.
7. Consentimiento, baja y conservación de datos de contacto.
8. Confirmación del alcance de la bandeja personal y del panel administrativo.

La identidad de alumnos y los roles/permisos eran dependencias del campus; la issue #34 era una referencia relacionada. Los actores posibles de esta sección no constituyen una matriz de destinatarios aprobada.

## 3. Requerimientos funcionales (RF)

Los criterios siguientes expresan el comportamiento esperado de la propuesta. Su cumplimiento no fue verificado mediante una implementación de este módulo.

### RF-N01 — Aplicar reglas de destinatarios y permisos (#44)

El sistema deberá resolver destinatarios, canales permitidos y obligatoriedad conforme a la matriz funcional aprobada.

- **CA-01:** Dada una matriz aprobada, cuando ocurra un evento contemplado, entonces solo se seleccionarán los destinatarios y canales autorizados para ese evento.
- **CA-02:** Dada una notificación opcional y un canal deshabilitado por el destinatario, cuando se resuelva la entrega, entonces ese canal quedará excluido.
- **CA-03:** Dada una consulta o modificación sobre avisos ajenos, cuando el solicitante carezca del permiso correspondiente, entonces el backend rechazará la operación sin exponer esos datos.

### RF-N02 — Persistir notificaciones y entregas (#46)

El sistema deberá distinguir la notificación lógica de sus intentos/resultados de entrega y conservar el estado de lectura.

- **CA-01:** Dado un aviso generado, cuando se registre, entonces se conservarán destinatario, referencia al origen y estado de lectura; cada entrega conservará al menos fecha, canal y estado.
- **CA-02:** Dado un evento ya procesado, cuando se procese nuevamente para el mismo destinatario y canal, entonces la regla de idempotencia impedirá duplicados.
- **CA-03:** Dada una falla de transporte, cuando se registre el resultado, entonces el aviso permanecerá consultable y el fallo quedará asociado al canal correspondiente.

### RF-N03 — Generar avisos desde eventos válidos (#48)

El sistema deberá generar avisos al producirse una preinscripción válida y en la primera publicación de noticias, eventos y comunicados.

- **CA-01:** Dado contenido en borrador, cuando se cree sin publicar, entonces no generará avisos; cuando se publique por primera vez, generará como máximo un aviso por destinatario y canal.
- **CA-02:** Dado contenido publicado, cuando se edite o despublique, entonces no se generará otro envío, salvo una regla de actualización expresamente aprobada en #44.
- **CA-03:** Dado un lead/contacto genérico, cuando se registre, entonces no activará un aviso de preinscripción; el disparador requerirá el evento del circuito específico de preinscripción.

### RF-N04 — Gestionar suscripciones y canales externos (#47)

El sistema deberá permitir consultar, modificar y dar de baja las suscripciones habilitadas, y entregar avisos por email y Telegram según las preferencias aprobadas.

- **CA-01:** Dada una suscripción opcional activa, cuando el titular solicite la baja, entonces se guardará el cambio y no habrá nuevos envíos de esa suscripción.
- **CA-02:** Dada una entrega multicanal, cuando falle email o Telegram, entonces el otro canal podrá conservar su resultado y cada fallo quedará registrado independientemente.
- **CA-03:** Dada una vinculación de Telegram, cuando se solicite asociar una cuenta, entonces se aplicará el mecanismo aprobado y no se aceptará arbitrariamente el identificador de otra persona.

### RF-N05 — Consultar y gestionar la bandeja personal (#49)

El sistema deberá mostrar al usuario autenticado sus notificaciones recientes y permitir marcar las propias como leídas.

- **CA-01:** Dado un usuario autenticado, cuando abra su bandeja, entonces verá únicamente sus avisos en orden reciente y con un listado paginado o acotado.
- **CA-02:** Dado un aviso propio no leído, cuando se marque como leído y se inicie una nueva sesión, entonces el estado persistirá y el contador de no leídos será consistente.
- **CA-03:** Dado un enlace de un aviso, cuando se abra, entonces se comprobará el permiso sobre el contenido de origen; no se expondrán borradores ni recursos restringidos.

### RF-N06 — Consultar el historial administrativo, si se aprobaba (#49)

El sistema deberá ofrecer un historial paginado de entregas y fallas solo si coordinación confirma esa necesidad y define el rol autorizado.

- **CA-01:** Dado un rol autorizado por la definición funcional, cuando consulte el historial, entonces verá los resultados de entrega y fallas dentro de su alcance.
- **CA-02:** Dado un usuario sin ese permiso, cuando intente acceder, entonces el backend denegará la consulta.
- **CA-03:** Dado el historial habilitado, cuando se muestre una página, entonces incluirá información suficiente para revisar la entrega sin exponer cuerpos completos ni datos personales innecesarios.

## 4. Requerimientos no funcionales (RNF)

| ID | Requerimiento propuesto | Forma prevista de verificación |
|---|---|---|
| RNF-N01 | Mantener dominio sin dependencias de FastAPI, Pydantic, SQLAlchemy ni transportes externos; rutas limitadas a delegar en casos de uso. | Revisión de dependencias y `python3 scripts/verify_architecture.py`. |
| RNF-N02 | Una falla externa no deberá revertir la publicación ni la preinscripción que originó el aviso. | Pruebas de fallas parciales y persistencia de la operación principal. |
| RNF-N03 | Aplicar permisos en backend y minimizar los datos expuestos en historial. Consentimiento y conservación debían definirse antes del desarrollo. | Pruebas de aislamiento y revisión contra la definición funcional aprobada. |
| RNF-N04 | Ofrecer controles operables con teclado, foco visible y estados comprensibles sin depender solo del color. | Recorrido manual con teclado y revisión de estados vacíos, leído/no leído y error. |
| RNF-N05 | Mantener migraciones compatibles con SQLite y MySQL, con subida y reversión verificables. | Pruebas de migración en ambos motores antes de liberar. |
| RNF-N06 | Mantener los contenidos institucionales configurables en `data/` y documentar nuevas variables sin secretos. | Revisión de cambios y de `.env.example`. |
| RNF-N07 | Cumplir las validaciones de tipos, arquitectura y pruebas definidas en la épica, con cobertura de `src` de al menos 85 %. | `pytest`, cobertura, `npm run typecheck:js` y `pyright`. |

No se habían fijado metas de latencia, volumen ni disponibilidad para el módulo. Debían acordarse antes de comprometer un nivel de servicio.

## 5. Casos de uso principales

### CU-N01 — Publicar contenido y generar avisos

**Actor principal:** Responsable autorizado de contenido.  
**Precondiciones:** Definición funcional aprobada, destinatarios resolubles y contenido válido.  
**Disparador:** Primera publicación de una noticia, evento o comunicado.

1. El responsable crea contenido publicado o publica un borrador.
2. El caso de uso registra la publicación.
3. El sistema resuelve destinatarios y canales habilitados.
4. Registra el aviso aplicando la regla de idempotencia.
5. Ejecuta las entregas previstas y registra sus resultados.

**Alternativas:** Un borrador no notifica. Un reprocesamiento no duplica avisos. Si falla un canal, se registra la falla y se conserva la publicación y el resultado de los demás canales.  
**Postcondición:** Contenido publicado y resultados de notificación consultables.  
**Trazabilidad:** RF-N01, RF-N02, RF-N03 y RF-N04.

### CU-N02 — Consultar y leer un aviso personal

**Actor principal:** Destinatario autenticado del campus.  
**Precondición:** Identidad y permisos resueltos por el campus.  
**Disparador:** El usuario abre la bandeja.

1. El sistema identifica al usuario y consulta sus avisos recientes.
2. Muestra el listado y diferencia leídos de no leídos.
3. El usuario marca un aviso propio como leído.
4. El sistema guarda ese estado y actualiza el contador.
5. Si abre el enlace al origen, se valida su permiso sobre ese recurso.

**Alternativas:** Sin avisos se muestra un estado vacío. Si se intenta leer/modificar un aviso ajeno, se rechaza la operación. Si el contenido ya no está disponible o no es accesible, se informa sin revelar datos restringidos.  
**Postcondición:** Estado de lectura persistido y acceso limitado a recursos autorizados.  
**Trazabilidad:** RF-N01, RF-N02 y RF-N05.

### CU-N03 — Cambiar preferencias o dar de baja una suscripción

**Actor principal:** Titular de la suscripción.  
**Precondiciones:** Mecanismo de identificación aprobado y reglas que distingan avisos opcionales de obligatorios.  
**Disparador:** El titular abre la gestión de preferencias.

1. El sistema muestra las suscripciones y canales que el titular puede configurar.
2. El titular deshabilita un canal opcional o solicita la baja.
3. El sistema valida la titularidad y guarda el cambio.
4. Confirma la preferencia vigente.
5. Los eventos posteriores respetan la nueva configuración.

**Alternativas:** Una notificación obligatoria sigue la regla institucional aprobada. La vinculación/desvinculación de Telegram exige el mecanismo seguro definido en #44. Un intento de cambiar preferencias ajenas se rechaza.  
**Postcondición:** Preferencias persistidas y aplicables a futuros envíos.  
**Trazabilidad:** RF-N01 y RF-N04.

## 6. Trazabilidad y plan de validación

| Issue | Entregable previsto | Requisitos relacionados | Situación al cierre |
|---|---|---|---|
| #44 | Definición funcional de destinatarios, preferencias y consentimiento | RF-N01; dependencias de los demás RF | Definiciones pendientes; no planificada. |
| #45 | Coordinación del sistema multicanal | Todos los RF y RNF | Épica discontinuada. |
| #46 | Modelo y persistencia | RF-N02, RF-N05 | No planificada. |
| #47 | Suscripciones, email y Telegram | RF-N04 | No planificada. |
| #48 | Disparadores de publicación y preinscripción | RF-N03 | No planificada. |
| #49 | Bandeja e historial | RF-N05 y RF-N06 | No planificada. |

La secuencia prevista era aprobar #44, implementar la base de #46 y luego integrar disparadores, canales y pantallas. La aceptación debía incluir pruebas de dominio, casos de uso, persistencia, permisos y rutas; además de deduplicación, baja, fallas parciales y compatibilidad con las alertas existentes. Este documento no informa resultados de esas pruebas: constituye su especificación prevista.

## 7. Cambio de alcance y aprendizaje

El 17/11/2026 se dejó asentado en las seis issues que el campus se discontinuó y que el módulo dependía de ese entorno. Por ese motivo se cerraron como **no planificadas**, sin marcar sus criterios como cumplidos.

El análisis muestra la necesidad de resolver primero las dependencias funcionales: definir un canal técnico no alcanza si todavía no se sabe quién recibe cada aviso, con qué permiso y bajo qué preferencias. El cierre conserva la trazabilidad de lo propuesto y explica por qué no se continuó su desarrollo.

## 8. Fuentes

- [SRS general del portal, utilizado como referencia de estructura](https://github.com/solareco86-ai/proyecto-integrador/blob/main/docs/srs.md).
- [#44 — Destinatarios, preferencias y consentimiento](https://github.com/solareco86-ai/proyecto-integrador/issues/44).
- [#45 — Épica del sistema multicanal](https://github.com/solareco86-ai/proyecto-integrador/issues/45).
- [#46 — Modelo y persistencia](https://github.com/solareco86-ai/proyecto-integrador/issues/46).
- [#47 — Suscripciones y canales externos](https://github.com/solareco86-ai/proyecto-integrador/issues/47).
- [#48 — Disparadores](https://github.com/solareco86-ai/proyecto-integrador/issues/48).
- [#49 — Bandeja e historial](https://github.com/solareco86-ai/proyecto-integrador/issues/49).
- [Guía de la materia: criterios de aceptación y casos de uso](https://github.com/solareco86-ai/proyecto-integrador/blob/main/data/core/cursos/practicas-profesionales-proyecto-integrador/lecciones/unidad-2-3-criterios-casos-uso.md).
