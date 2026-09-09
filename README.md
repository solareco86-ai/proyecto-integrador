# isftn199-web (`isftn199.com.ar`)

Sitio web institucional oficial y campus virtual del **Instituto Superior de Formación Técnica N° 199** (El Talar, Tigre, Provincia de Buenos Aires). Aplicación web Server-Side Rendered (SSR) construida con **FastAPI** y Python bajo Arquitectura Hexagonal / DDD. Gestiona la presencia institucional, catálogo oficial de carreras técnicas superiores (`/carreras`), requisitos de ingreso e inscripción (`/carreras#requisitos`), campus virtual y LMS de cátedras técnicas (`/cursos`), y recepción de consultas de aspirantes con notificaciones automáticas.

## 1. Identidad y Misión Institucional

* **Institución:** Instituto Superior de Formación Técnica N° 199.
* **Dependencia:** Dirección General de Cultura y Educación (DGCyE) de la Provincia de Buenos Aires · Dirección de Educación Técnico Profesional (DETP).
* **Nivel:** Educación Superior Técnica Terciaria (Pública y 100% Gratuita). Títulos oficiales con validez nacional.
* **Sede Principal:** Maestra Celina Voena 1750, El Talar, Partido de Tigre, Pcia. de Buenos Aires (CP 1618).
* **Dominio Oficial:** [https://isftn199.com.ar](https://isftn199.com.ar)
* **Oferta Académica Principal (Tecnicaturas Superiores de 3 Años):**
  1. *Ciencia de Datos e Inteligencia Artificial* (Resolución DGCyE N° 273/22)
  2. *Mecatrónica* (Resolución DGCyE N° 5885/10)
  3. *Logística* (Resolución DGCyE N° 1243/19)
  4. *Higiene y Seguridad en el Trabajo* (Resolución DGCyE N° 320/13)
  5. *Administración de Recursos Humanos* (Resolución DGCyE N° 276/03)
  6. *Servicios Gastronómicos y Turismo* (Resolución DGCyE N° 148/18)

---

## 2. Estructura del Proyecto

* **[docs/](docs)**: Suite canónica de documentación viva (SSOT):
  * **[srs.md](docs/srs.md)**: Especificación de requerimientos, catálogo oficial de tecnicaturas, requisitos de admisión, campus virtual y modelo educativo 100% público y gratuito.
  * **[specs.md](docs/specs.md)**: Arquitectura Hexagonal/DDD, catálogo de carreras, campus virtual LMS, Critical CSS, observabilidad (`X-Request-ID`) y testing.
  * **[ops.md](docs/ops.md)**: Manual de operaciones en VPS, Systemd, Nginx, despliegues seguros y gestión de incidentes.
  * **[todo.md](docs/todo.md)**: Registro de Certezas vigentes (C-01 a C-20) y roadmap de desarrollo.
  * **[CHANGELOG.md](docs/CHANGELOG.md)**: Historial cronológico de hitos, refactorizaciones y migraciones.
* **[src/](src)**: Código fuente organizado en capas limpias (`domain`, `application`, `adapters`, `infrastructure`).
* **[data/](data)**: Archivos YAML y Markdown de contenido estático (carreras, cursos, lecciones, configuración institucional y SEO).
* **[templates/](templates)**: Plantillas Jinja2 para la interfaz de usuario.
* **[static/](static)**: Hojas de estilo CSS (Critical CSS + Tailwind v4), JavaScript tipado con JSDoc y assets.
* **[tests/](tests)**: Suite automatizada de pruebas unitarias y de integración.

---

## 3. Inicio Rápido Local

### Requisitos Previos
* **Python 3.12** o superior instalado en el sistema.
* Entorno Windows, Linux o macOS.

### Configuración y Puesta en Marcha
1. Crear el archivo de entorno local a partir del ejemplo:
   ```bash
   cp .env.example .env
   ```
2. Iniciar el servidor local (crea automáticamente el entorno virtual `.venv`, instala dependencias y arranca Uvicorn con recarga en vivo):
   - **Multiplataforma / Python:**
     ```bash
     python run.py
     ```
   - **Windows:**
     ```cmd
     run.bat
     ```
   - **Linux / macOS:**
     ```bash
     ./run.sh
     ```
   Acceder a: `http://localhost:8001` (o puerto configurado).

---

## 4. Control de Calidad y Pruebas

```bash
# 1. Verificación estricta de tipos JavaScript (0 errores LSP)
npm run typecheck:js

# 2. Ejecutar pruebas unitarias y de integración
pytest

# 3. Ejecutar pruebas con reporte de cobertura (mínimo 85%)
pytest --cov=src --cov-fail-under=85 tests/

# 4. Verificación estricta de tipos Python con Pyright (0 errores)
pyright

# 5. Verificación de reglas de Arquitectura Limpia
python3 scripts/verify_architecture.py
```

---

## 5. Orientación a Aspirantes y Gestión de Consultas Institucionales

La plataforma implementa un pipeline desacoplado y resiliente para la recepción de consultas académicas y orientación al aspirante:

1. **Formularios de Consulta y Preinscripción (`/contact`, `#ingreso`):**
   - **Gestión Unificada:** Las consultas se consolidan con **deduplicación** por email y teléfono: si el aspirante ya realizó una consulta previa, se preserva el historial cronológico de orientación académica.
   - **Registro de Auditoría:** Cada consulta se almacena íntegra en la base de datos con metadatos completos (carrera de interés, situación de estudios secundarios, timestamps).
   - **Notificación por Correo Electrónico:** Despacho vía SMTP a la Secretaría del instituto (`isft199@gmail.com`) para su seguimiento administrativo.
   - **Alerta Instantánea en Telegram:** Notificación en tiempo real con datos de contacto y enlace directo a chat de WhatsApp institucional.

2. **Canales Directos de Orientación (WhatsApp, Teléfono y Correo):**
   - **Atención Inmediata:** Acceso directo a los canales oficiales de Secretaría y Preceptoría.
   - **Privacidad y Resguardo:** Protección estricta de la información personal de aspirantes y alumnos conforme a normativas de protección de datos.

---

## 6. Suite de Servidores FastMCP para Agentes de IA

Los servidores FastMCP para analítica y auditoría presupuestaria en tiempo real fueron migrados al repositorio **`datamaq-hub`** para unificar las herramientas de uso interno de la organización.

Ver detalles de gobernanza y configuración en **[`docs/certezas_y_dudas_datamaq_hub.md`](docs/certezas_y_dudas_datamaq_hub.md)**.

