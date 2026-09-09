# Instrucciones y Reglas de Desarrollo para Agentes de IA (AGENTS.md)

Este archivo contiene los lineamientos de diseño, restricciones arquitectónicas y reglas de comportamiento que todo asistente de desarrollo de Inteligencia Artificial (como Antigravity, Kimi Code o Codex) debe obedecer al trabajar en el repositorio del **Portal Institucional y Campus Virtual del ISFT N° 199** (`isftn199.com.ar`).

---

## 1. Idioma de Interacción y Documentación
* **Idioma:** Toda comunicación con el usuario en el chat, logs de descubrimiento, explicaciones de commits y documentación técnica nueva (`*.md`) debe redactarse **exclusivamente en español**.

---

## 2. Restricciones de Arquitectura y Diseño de Software
* **Arquitectura Hexagonal / Limpia & DDD:** La aplicación en [src/](src) está organizada en capas con responsabilidades delimitadas que deben mantenerse:
  * **[domain/](src/domain)**: Define las entidades y value objects strictly usando la **librería estándar de Python (`@dataclass`, `@dataclass(frozen=True)`, `typing`, `abc`)**. Cero dependencias externas (prohibido Pydantic, FastAPI o bases de datos en dominio).
  * **[application/](src/application)**: Contiene los servicios de aplicación, casos de uso (ej. `DataService`, `SubmitLeadUseCase`), mappers y los **DTOs de validación y serialización con Pydantic** en `src/application/dtos/`.
  * **[adapters/](src/adapters)**: Presenters y adaptadores de interfaz agnósticos de frameworks web.
  * **[infrastructure/](src/infrastructure)**: Inicialización de FastAPI, configuración de rutas web, persistencia SQLAlchemy/MySQL y middleware.
* **Separación de Lógica:** No se permite escribir lógica de acceso a datos o de negocio directamente dentro de los endpoints de rutas en [infrastructure/fastapi/routes/](src/infrastructure/fastapi/routes). Estos deben limitarse a recibir peticiones, llamar al servicio correspondiente y retornar la plantilla o respuesta.

---

## 2b. Modificabilidad del Código Fuente (src/)
* **Permitido y esperado:** El código en [src/](src) puede y debe modificarse para implementar funcionalidad, corregir errores, y agregar rutas, servicios, mappers, presenters o utilidades (ej. lógica de SEO), respetando siempre la separación de capas de la sección 2.
* **Prohibido:**
  - Introducir datos de contenido (textos, catálogos, cursos, lecciones, cobertura) en código Python o plantillas HTML; esos datos viven exclusivamente en [data/](data).
  - Escribir lógica de acceso a datos o de negocio dentro de los endpoints de [infrastructure/fastapi/routes/](src/infrastructure/fastapi/routes); deben delegar en servicios.
  - Agregar dependencias externas (Pydantic, FastAPI, bases de datos) en la capa [domain/](src/domain).
  - Escribir expresiones Jinja (`{{ }}` / `{% %}`) dentro del valor de atributos `style="..."` que **no sean** CSS custom properties. La lógica de presentación condicional se resuelve con clases CSS (definidas en [critical.css](static/css/src/critical.css) o en los fuentes de [static/css/src/](static/css/src)). Se permite Jinja únicamente para interpolar un valor en una custom property: `style="--nombre: {{ dato }}"`. El validador [scripts/validate_templates.py](scripts/validate_templates.py) aplica esta regla (R1) en el pipeline.
  - Editar a mano el partial generado [templates/partials/critical_css.html](templates/partials/critical_css.html). El CSS crítico se edita en [static/css/src/critical.css](static/css/src/critical.css) y los tokens en [static/css/src/tokens.css](static/css/src/tokens.css); el partial se regenera con `python3 scripts/build_critical_css.py` (o `npm run build:css`).
  - "Corregir" los falsos positivos del parser CSS de VS Code: `css-semicolonexpected` en [static/css/src/input.css](static/css/src/input.css) (`@import "tailwindcss" prefix(tw);` es sintaxis Tailwind v4 válida) y `propertyIgnoredDueToDisplay` en [static/css/index.css](static/css/index.css) (regla `img,video,canvas,audio,iframe,embed,object{vertical-align:middle;display:block}` del preflight de Tailwind, artefacto de build). No editar esas líneas.

---

## 3. Gestión de Datos de Contenido (Servicios, Cobertura, Leads y Cursos)
* **Datos Desacoplados:** Toda la información referente a la propuesta de servicios técnicos, industrias asociadas, cobertura geográfica, leads capturados, cursos, lecciones, cuestionarios e instructores reside en archivos estáticos en la carpeta [data/](data).
* **Prohibido Hardcodear:** No debes escribir datos de contenido o textos descriptivos dentro del código Python o directamente en las plantillas HTML de [templates/](templates). Toda incorporación de información debe realizarse actualizando los archivos `.yaml` y agregando los archivos `.md` correspondientes.

---

## 4. Control de Calidad y Pruebas
* **Pruebas Automatizadas Obligatorias:** Tras realizar cualquier modificación al código fuente, debes ejecutar las pruebas unitarias y de integración para garantizar que no existan regresiones:
  ```bash
  pytest
  ```
* **Verificación Estática de Tipos Obligatoria en Todo el Repositorio:** Tras crear o modificar archivos en `src/`, `scripts/`, `static/js/` o `tests/`, debes verificar que existan 0 errores de tipado estricto con Pyright/Pylance y TypeScript LSP:
  ```bash
  npm run typecheck:js
  pyright
  ```
  *(o `pyright src/ scripts/ tests/`)*
* **Tipado Estricto Obligatorio:** Todo código Python y JavaScript nuevo o modificado debe incluir anotaciones de tipo completas y explícitas (JSDoc en JS, dataclasses/type hints en Python). Queda prohibida la inicialización de colecciones vacías sin anotación de tipo (ej: inicializar siempre `items: list[str] = []` o `mapping: dict[str, Any] = {}` en lugar de `items = []`), para evitar diagnósticos de tipo desconocido (`reportUnknownVariableType`, `reportUnknownMemberType`).
* **Verificación de Arquitectura Limpia:**
  ```bash
  python3 scripts/verify_architecture.py
  ```
* **Verificación de Cobertura:** Asegúrate de no reducir la cobertura de pruebas al añadir nueva lógica o rutas:
  ```bash
  pytest --cov=src --cov-fail-under=85 tests/
  ```

---

## 5. Control de Cambios y Despliegue
* **Despliegue Continuo (CI/CD Automático):** La publicación de cambios hacia el VPS de producción opera mediante **GitHub Actions (`.github/workflows/deploy.yml`)** en cada `git push` a `main` autorizado por el usuario. Una vez que el usuario aprueba el push, el pipeline de CD corre los tests y realiza el deploy automáticamente.
* **Prohibición de Deploy Manual Autónomo:** Queda terminantemente prohibido ejecutar el script local/VPS `./scripts/deploy-server.sh` de forma manual o autónoma sin la expresa aprobación previa del usuario.
* **Validación de Dependencias:** Al añadir librerías nuevas al archivo [requirements.txt](requirements.txt), valida primero localmente que no existan conflictos de versiones.

---

## 6. Operaciones en el VPS de Producción
* **Prohibido ejecutar git como `root` en el VPS:** Cualquier comando git (`git pull`, `git status`, `git fetch`) ejecutado como `root` sobre `/var/www/www-datamaq` deja `.git/index` y otros archivos con ownership `root`, rompiendo el despliegue (ver [docs/ops.md](docs/ops.md)).
* **Uso correcto en el VPS:** Ejecutar siempre git con el usuario dedicado:
  ```bash
  sudo -u datamaq git pull --ff-only
  sudo -u datamaq git status
  ```
  o a través del script [scripts/deploy-server.sh](scripts/deploy-server.sh).

---

## 7. Marco Institucional, Académico y Gobernanza del Portal ISFT N° 199

El portal institucional y campus virtual (`isftn199.com.ar`) opera como la plataforma digital oficial del **Instituto Superior de Formación Técnica N° 199 de Tigre**, institución educativa pública de nivel superior técnico provincial.

### 7.1 Identidad Institucional y Propuesta Educativa Pública
* **Dependencia Oficial:** Dirección General de Cultura y Educación (DGCyE) de la Provincia de Buenos Aires, Región 6.
* **Sede Operativa:** Maestra Celina Voena 1750, El Talar (Partido de Tigre, Pcia. de Buenos Aires).
* **Horario de Cursada:** Turno vespertino oficial (18:00 a 22:30 hs).
* **Principio de Gratuidad Total:** La educación es **100% pública y gratuita**. Queda estrictamente prohibido tarifar, cobrar matrículas, mensualidades o inventar precios en el portal. Las redirecciones permanentes (301) desde antiguas rutas comerciales (`/pricing`, `/planes`) conducen directamente al catálogo académico oficial (`/carreras`).

### 7.2 Oferta Académica Oficial (Tecnicaturas Superiores de 3 Años)
El instituto ofrece 6 tecnicaturas superiores con títulos oficiales de validez nacional y articulación socio-productiva con Tigre y Zona Norte del GBA:
1. **Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial:** Machine Learning, analítica avanzada, Python, pipelines de datos y modelos predictivos.
2. **Tecnicatura Superior en Mecatrónica:** Automatización industrial, robótica, electrónica aplicada, PLC y mantenimiento electromecánico.
3. **Tecnicatura Superior en Logística:** Gestión de cadena de suministro, distribución física, centros de almacenamiento y comercio internacional.
4. **Tecnicatura Superior en Higiene y Seguridad en el Trabajo:** Prevención de riesgos laborales, ergonomía, auditoría ambiental y normativa SRT.
5. **Tecnicatura Superior en Administración de Recursos Humanos:** Gestión del talento, relaciones laborales, legislación del trabajo y clima organizacional.
6. **Tecnicatura Superior en Servicios Gastronómicos y Turismo:** Planificación de servicios turísticos, gestión gastronómica, hospitalidad y desarrollo regional.

### 7.3 Campus Virtual y Aulas Técnicas (`/cursos`)
* **LMS Integrado:** El campus virtual en `/cursos` sirve como aula técnica extendida con talleres prácticos, lecciones interactivas, código abierto y recursos de cátedra para estudiantes y docentes del instituto.
* **Formatos de Contenido:** El contenido de clases y laboratorios reside desacoplado en `data/core/cursos/` en formato Markdown estructurado con soporte de sintaxis de programación.

### 7.4 Requisitos de Ingreso y Orientación al Aspirante
* **Requisito Fundamental:** Título secundario completo o constancia de título en trámite (otorgado por instituciones reconocidas por el Ministerio de Educación).
* **Documentación de Legajo:** Fotocopia de DNI, analítico secundario, partida de nacimiento, 2 fotos 4x4 y certificado de aptitud psicofísica.
* **Canales de Orientación:** Formulario de consulta multi-paso (`#ingreso`, `/contact`), atención directa por secretaría y canal de WhatsApp institucional.

### 7.5 Reglas de Veracidad Académica y Antialucinación
1. **Veracidad Curricular:** Prohibido inventar o asumir títulos, correlatividades, resoluciones ministeriales o materias no especificadas en `data/content/carreras.yaml`.
2. **Desacoplamiento de Contenido:** Ningún dato curricular o administrativo debe escribirse en código Python o templates HTML. Toda actualización opera sobre archivos en `data/`.
3. **Canales Oficiales:**
   - Sitio Web Oficial: `https://isftn199.com.ar`
   - Correo Institucional: `isft199@gmail.com`
   - Teléfono / WhatsApp de Secretaría: `+54 11 5629 7160`

