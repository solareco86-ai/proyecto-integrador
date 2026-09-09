# Oportunidades de Mejora y Hoja de Ruta — `isftn199-web`

> **Proyecto:** Instituto Superior de Formación Técnica N° 199 (`isftn199.com.ar`)  
> **Estado:** Documento Vivo de Estrategia Técnica, UX Académica & SEO  
> **Ámbito:** Portal institucional, catálogo de tecnicaturas, campus virtual (LMS), admisión y accesibilidad.

---

## 🎓 1. Experiencia del Aspirante y Difusión Académica

### A. Herramientas de Orientación Vocacional y Curricular
- **Orientador de Carrera Interactivo:** Módulo ágil de autoevaluación para aspirantes indecisos entre tecnicaturas afines (ej. *Ciencia de Datos e IA* vs *Mecatrónica*), guiándolos según intereses en programación, robótica, gestión o logística.
- **Descarga Directa de Resoluciones y Planes de Estudio:** Integración de enlaces de descarga directa de los PDFs oficiales de resoluciones DGCyE (Res. 273/22, Res. 5885/10, etc.) en cada ficha de `/carreras/{slug}`.
- **Visualizador de Malla Curricular y Correlatividades:** Diagrama interactivo de correlatividades por año (1°, 2° y 3°) para facilitar la planificación de cursada a los estudiantes regulares.

### B. Proceso de Inscripción Ágil
- Preinscripción en línea con subida opcional de documentación digital (DNI, analítico) para revisión preliminar por Secretaría.
- Canales de asistencia directa por WhatsApp institucional con mensajes predefinidos por tecnicatura.

---

## 🔍 2. Posicionamiento Orgánico (SEO Educativo) y Datos Estructurados

### A. Schema.org Especializado en Educación Superior
Consolidar el marcado enriquecido en formato JSON-LD para posicionar las tecnicaturas en Google for Education y búsquedas locales:
- **`CollegeOrUniversity` / `EducationalOrganization`**:
  - Nombre: *Instituto Superior de Formación Técnica N° 199*.
  - Sede operativa: *Maestra Celina Voena 1750, El Talar, Tigre*.
  - Horario de cursada oficial: *Lunes a Viernes de 18:00 a 22:30 hs*.
- **`EducationalOccupationalProgram`**:
  - Fichas individuales por tecnicatura superior: titulación oficial, validez nacional, duración de 3 años y requisitos de titulación.
- **`Course`**:
  - Estructuración de las materias técnicas del campus virtual (`/cursos`).
- **`FAQPage`**:
  - Preguntas frecuentes sobre homologaciones, equivalencias de materias, documentación para egresados del secundario y cursada vespertina.

---

## 💻 3. Campus Virtual y Aulas Técnicas (LMS)

### A. Plataforma Práctica para Cátedras de Software e IA
- **Visualizador de Notebooks Jupyter:** Integración para renderizar notebooks de cátedra directamente en el navegador dentro de las lecciones de Ciencia de Datos e IA.
- **Repositorio de Código Abierto:** Enlace a repositorios institucionales de GitHub para prácticas de cátedra y proyectos integradores.
- **Calendario Académico Centralizado:** Módulo con cronograma de fechas clave: inicio de cuatrimestre, mesas de exámenes finales, receso invernal y períodos de preinscripción.

---

## ⚡ 4. Rendimiento, Resiliencia y Accesibilidad (a11y)

### A. Accesibilidad Web (WCAG 2.1 AA)
- Auditoría continua de contraste cromático, navegación completa por teclado, etiquetas `aria-*` y compatibilidad con lectores de pantalla para garantizar inclusión total en un portal público provincial.

### B. Core Web Vitals y Rendimiento Móvil
- Mantener el **Largest Contentful Paint (LCP)** por debajo de 1.2 segundos y **CLS = 0** mediante la inyección de Critical CSS inline (<14KB) y optimización de imágenes WebP.
- Cero dependencias pesadas en el bundle JavaScript de cliente.

