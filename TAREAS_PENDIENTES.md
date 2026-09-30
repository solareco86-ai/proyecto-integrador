# Tareas Pendientes - Proyecto Integrador

## Estado General
Documentación de tareas por completar en el proyecto ISFT N° 199.

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
**Estado:** Pendiente

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
**Responsable:** Sol (solangeareco36@gmail.com)
