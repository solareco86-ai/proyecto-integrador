# Tareas Pendientes - Proyecto Integrador

## Estado General
Documentación de tareas por completar en el proyecto ISFT N° 199.

---

## Equipo y roles (BORRADOR — pendiente de confirmar)

> La asignación de Lucas, Lautaro y Verónica a sus funcionalidades es tentativa:
> conviene revisarla según la experiencia de cada uno (Asistencias es la tarea más grande).

| Persona | Rol principal | Responsabilidad adicional |
|---|---|---|
| Sol | Coordinación general | QA y documentación (este archivo, seguimiento, demo) |
| Mati | Accesos, roles y permisos (tarea 2) | Revisión técnica de PRs |
| Milagros | SEO, GEO y SEM | Frontend/UX (header, imágenes, paneles por rol) |
| Lucas | Campus: validar y agregar cursos (tarea 1) | — |
| Lautaro | Notificaciones (tarea 3) | — |
| Verónica | Asistencias (tarea 4) | — |

Agustín es el profesor de la materia; no forma parte del equipo de desarrollo.

### Orden de trabajo sugerido
1. **Primero:** Mati define roles y permisos (primera versión). Las tareas 1, 3 y 4 dependen de saber quién es profesor, alumno, preceptor o directivo.
2. **En paralelo:** Lucas, Lautaro y Verónica diseñan sus modelos de datos; Milagros arma maquetas de las pantallas.
3. **Después:** cada uno trabaja en su rama `feat/...` y abre PR hacia `main`.

---

## Certezas (estado actual del código)

- Stack: FastAPI + Jinja/Tailwind + MySQL (SQLAlchemy) + migraciones con Alembic + tests con pytest.
- Ya existe login (`src/infrastructure/fastapi/routes/auth_routes.py`) con bcrypt y CSRF.
- La entidad `Usuario` tiene campo `rol`, pero hoy existe un único rol: `"autoridad"` (`src/domain/auth/entities.py`).
- Tablas existentes: `leads`, `usuarios`, `noticias`, `eventos`, `comunicados`. No existen tablas de alumnos, materias ni asistencias.
- Ya hay gateways de notificación por email y Telegram (`src/infrastructure/gateways/`).

## Decisiones tomadas

1. **Plazos:** 10-11.
2. **Validar cursos:** el curso que carga un docente lo valida un **docente especialista**. En el MVP se implementa con archivos YAML en el repositorio y aprobación vía Pull Request (opción B); luego evolucionará a base de datos (ver "Preguntas para Lucas").
3. **Roles:** "directivo" es el rol `"autoridad"` que ya existe. **Un usuario puede tener 2 roles** → el campo `rol` (texto único) de `Usuario` debe pasar a soportar varios roles (tarea de Mati).
4. **Alumnos:** se registran solos en la **preinscripción**. La **inscripción** es un circuito distinto.
5. **Asistencias:** las toma el **profesor**.
6. **Notificaciones:** por **todos los canales** (en el sitio, email y Telegram).

## Dudas abiertas

1. **Plazos:** ¿"10-11" significa octubre-noviembre o el 10 de noviembre? ¿Hay entregas parciales antes?
2. **Docente especialista:** ¿es un rol más (además de profesor, alumno, preceptor y directivo) o un atributo del profesor (ej. especialista por área o carrera)?
3. **Inscripción:** ¿cómo es el "otro camino"? ¿Quién pasa a un preinscripto a alumno inscripto (preceptor, directivo)? ¿Entra en el alcance de este proyecto?
4. **Asistencias:** ¿se registran por materia/clase o por día? ¿Hay justificaciones o porcentaje mínimo? ¿Qué puede ver/hacer el preceptor?
5. **Notificaciones:** ¿quién recibe cada tipo (preinscriptos, comunicados, eventos, noticias)? ¿El usuario puede elegir canales?
6. **Cambio del header (sección 5):** confirmar qué imagen se cambia y cuál es el texto/enlace correcto ("Requisitos de ingreso" vs. "Preinscripción").

## Preguntas para Lucas (campus y cursos)

### ¿Dónde se guardan los cursos?
Hoy los cursos **no están en la base de datos**: son archivos versionados en el repositorio
(`data/core/cursos/<curso>/curso.yaml` + lecciones en Markdown), leídos por `DataService.get_cursos_container()`
en `src/application/data_service.py`. Agregar un curso hoy = hacer un commit.

Esto choca con la decisión de que un **docente cargue su curso y un docente especialista lo valide** desde el sitio. Opciones:

- **A. Pasar los cursos a la base de datos:** nuevas tablas (curso, lección, estado de aprobación) y migración de los cursos existentes. Permite cargar y aprobar desde el panel. Es la opción más trabajosa.
- **B. Mantener archivos y aprobar vía Pull Request:** el docente propone el curso como PR y el especialista lo aprueba en GitHub. Casi no requiere código, pero exige que docentes y especialistas usen GitHub.
- **C. Híbrida:** los datos del curso y su estado de aprobación en la base de datos; el contenido de las lecciones sigue en Markdown.

### ✅ Decisión: opción B — archivos en el repo + aprobación vía Pull Request

**Para el MVP los cursos quedan en YAML** (opción B). **Más adelante evolucionarán a base de datos** (opción A), con carga y aprobación desde el panel del sitio.

Para que esa migración futura sea sencilla:
- Definir y validar en CI un esquema estable de `curso.yaml`: los mismos campos serán después las columnas de la tabla de cursos.
- Seguir leyendo los cursos solo a través de `DataService` (no leer los YAML desde otros lugares). Así, al pasar a base de datos, se cambia una sola capa.

El circuito de un curso en el MVP queda así:

| Estado del curso | Equivalente en GitHub |
|---|---|
| Borrador | PR en modo *draft* |
| Enviado a revisión | PR listo para revisar (*Ready for review*) |
| Rechazado / con cambios | Review con *Request changes* |
| Aprobado | Review con *Approve* del docente especialista |
| Publicado | PR mergeado a `main` (y deploy) |
| Edición de un curso aprobado | Nuevo PR → vuelve a revisión automáticamente |

**Alcance de la tarea 1 (Lucas) con esta decisión:**
- [ ] Plantilla de curso nuevo (carpeta modelo con `curso.yaml` y una lección de ejemplo).
- [ ] Validación automática en CI: que cada `curso.yaml` tenga los campos obligatorios y las lecciones referenciadas existan (hoy `.github/workflows/` solo tiene `deploy.yml`).
- [ ] `CODEOWNERS` para que los PR sobre `data/core/cursos/` pidan review al docente especialista, y protección de rama en `main` que exija esa aprobación.
- [ ] Guía paso a paso para docentes: cómo proponer un curso por PR (puede ir en `CONTRIBUTING.md`).

**Impacto en Mati:** la aprobación de cursos ocurre en GitHub, no en el sitio. El "docente especialista" podría **no** necesitar ser un rol dentro de la aplicación (ver pregunta 2 para Mati).

Preguntas que quedan:
1. ¿Docentes y especialistas ya tienen cuenta de GitHub y saben usarla? Si no, ¿quién los capacita?
2. ¿Quiénes son los docentes especialistas y de qué áreas? (necesario para armar `CODEOWNERS`).
3. ¿Hace falta aprobación de un especialista por área/carrera, o alcanza con uno para todos los cursos?

> Nota de entorno: en desarrollo la base es SQLite (`data/leads.db`) y en producción MySQL (ver `.env.example`).
> Las migraciones nuevas deben probarse en ambas.

## Preguntas para Mati (accesos, roles y permisos)

### Urgentes — desbloquean a Lucas, Lautaro y Verónica
1. **Roles múltiples:** una persona puede tener 2 roles, pero hoy `Usuario.rol` guarda uno solo. ¿Tabla aparte usuario-rol o lista en el mismo campo? ¿Hay que migrar los usuarios `"autoridad"` existentes?
2. **Docente especialista:** como la aprobación de cursos se hace por Pull Request en GitHub (opción B), ¿hace falta que exista como rol dentro de la aplicación, o alcanza con que sea revisor en GitHub (`CODEOWNERS`)?
3. **Fecha:** ¿cuándo puede estar una primera versión de roles que el resto pueda usar, aunque sea básica?

### Diseño de permisos
4. ¿Permisos solo **por rol** (un profesor carga asistencias) o también **por recurso** (un profesor carga asistencias solo de *sus* materias)? Impacta en Asistencias (Verónica).
5. ¿Qué ve y qué puede hacer cada rol? Armar una matriz rol × acción (crear/editar cursos, aprobar cursos, cargar asistencias, publicar comunicados, ver preinscriptos) como guía para todo el equipo.
6. ¿Cómo se aplica desde el código? Por ejemplo, una dependencia de FastAPI tipo `requiere_rol("profesor")` que los demás usen en sus rutas.

### Alta y ciclo de vida de usuarios
7. ¿Quién crea las cuentas de profesores, preceptores y especialistas: un directivo desde el panel, o se registran solos y alguien las aprueba?
8. ¿Un preinscripto tiene cuenta con acceso, o la obtiene recién al inscribirse?
9. Si un profesor deja el instituto, ¿se desactiva con `is_active` o se le quitan los roles?

---

## 1. Campus: Validar y Agregar Cursos
**Estado:** Pendiente

### Descripción
Implementar validación y sistema de gestión de cursos en el campus virtual.

### Requisitos
- [ ] Validar datos de cursos antes de agregar
- [ ] Interfaz para agregar nuevos cursos
- [ ] Almacenamiento persistente de cursos
- [ ] Manejo de errores y validaciones

---

## 2. Niveles de Acceso
**Estado:** Pendiente

### Descripción
Implementar sistema de control de acceso por rol de usuario.

### Roles Requeridos
- [ ] Profesores
- [ ] Alumnos
- [ ] Preceptores
- [ ] Directivos

### Requisitos
- [ ] Definir permisos por rol
- [ ] Autenticación y autorización
- [ ] Interfaz de gestión de roles
- [ ] Auditoría de accesos

---

## 3. Notificaciones
**Estado:** Pendiente

### Descripción
Sistema de notificaciones para diferentes eventos del sistema.

### Tipos de Notificaciones
- [ ] Preinscriptos
- [ ] Comunicados
- [ ] Eventos
- [ ] Noticias

### Requisitos
- [ ] Panel de notificaciones
- [ ] Sistema de suscripción
- [ ] Entrega de notificaciones (email, in-app)
- [ ] Historial de notificaciones

---

## 4. Sistema de Asistencias
**Estado:** Pendiente

### Descripción
Registro y control de asistencias de estudiantes.

### Requisitos
- [ ] Registro de asistencia
- [ ] Reportes de asistencia
- [ ] Integración con cursos
- [ ] Visualización por estudiante/clase

---

## 5. Cambios UI/UX - Header y Preinscripción
**Estado:** Pendiente — el alcance está sin confirmar (ver duda 7). Lo que sigue es una interpretación inicial.

### Cambios en Header
**Archivos Afectados:** `templates/partials/components/header.html`

- [ ] **Cambiar imagen de logo** (línea 16)
  - Ruta actual: `/static/media/logo-isft199.webp`
  - Nueva ruta: _(pendiente especificar)_

- [ ] **Cambiar texto de botón y ruta de "Inscripciones" a "Preinscripción"** (línea 52)
  - Texto actual: "Requisitos de ingreso"
  - Href actual: `/inscripciones`
  - Texto nuevo: _(pendiente especificar)_
  - Href nuevo: `/preinscripcion`

### Cambios en Rutas
**Archivos Afectados:** `src/infrastructure/fastapi/routes/carreras_routes.py`

- [ ] **Renombrar ruta `/inscripciones` a `/preinscripcion`** (líneas 82-84)
  - Ruta actual: `/inscripciones` → `/carreras#requisitos`
  - Nueva ruta: `/preinscripcion` → _(pendiente especificar destino)_

---

## Notas
- Todos los cambios deben mantenerse en control de versiones
- Implementar tests para cada nueva funcionalidad
- Seguir patrones de código existentes en el proyecto
- Documentar cambios en commits descriptivos

---

**Última actualización:** 2026-09-30
**Responsable del documento:** Sol (coordinación general)
