# SRS-SPECS — Proyecto Web Institucional ISFT N.º 199

| Campo | Detalle |
|---|---|
| **Documento** | SRS — Especificación de Requisitos del Software |
| **Versión** | 0.1 — Consolidado para revisión |
| **Estado** | Borrador consolidado |
| **Fecha** | 22 de noviembre de 2026 |
| **Autores** | Solange Areco — SRS individual (N1), elaborado sobre el Proyecto Integrador grupal ISFT N.º 199. |
| **Repositorio** | `solareco86-ai/proyecto-integrador` |
| **Dominio** | https://isftn199.com.ar |

> Documento de trabajo basado en la plantilla SRS-SPECS. Se distinguen requisitos, objetivos, funcionalidades verificadas y propuestas futuras.

## SRS-SPECS: Single Source of Truth (SSOT) & Especificación del Sistema

Este documento consolida el contexto estratégico, los requisitos, la arquitectura, las convenciones y la gobernanza del Proyecto Web Institucional del ISFT N.º 199. Es una referencia para el desarrollo, revisión, mantenimiento y evolución del sistema.

> **Acompañamiento pedagógico:** analizar necesidades, casos de borde, restricciones y decisiones de diseño, evitando la sobreingeniería y documentando las soluciones adoptadas.

---

## 1. Contexto Estratégico & Propuesta de Valor

### 1.1. Foco Estratégico & Alcance

| Aspecto | Definición |
|---|---|
| Mercado objetivo | Institución educativa superior y comunidad vinculada al ISFT N.º 199; portal institucional, no producto comercial. |
| Buyer Persona | Autoridades y referentes que necesitan difundir información oficial, mantener el portal y mejorar su presencia digital. |
| User Persona | Aspirantes, estudiantes, docentes, personal institucional y comunidad. |
| Alcance geográfico/modalidad | Alcance local/regional y acceso público por Internet; despliegue en infraestructura VPS. |
| Fuera de alcance | Gestión académica integral, inscripción/legajos, pagos, LMS, DataMaq, IA autónoma en runtime y campañas SEM ejecutadas no documentadas. |

El proyecto busca centralizar información sobre la institución, propuestas educativas, noticias, eventos, comunicados y contacto. También contempla posicionamiento SEO y GEO, y evaluación de posibles acciones SEM.

### 1.2. Pilares de Valor de la Solución

| Pilar | Enfoque | Implementación |
|---|---|---|
| 1. Activos & Entorno Operativo | Infraestructura y fuentes | Portal web, VPS, dominio, base de datos y contenidos institucionales. |
| 2. Software & Lógica de Negocio | Captura, procesamiento, persistencia e interfaz | Python/FastAPI, arquitectura por capas, casos de uso, persistencia y vistas web. |
| 3. Impacto Económico & ROI | Eficiencia y alcance | Centralización, facilidad de actualización, visibilidad y comunicación. ROI no cuantificado. |

### 1.3. Coordinación Operativa, Roles & Seguridad

| Aspecto | Definición |
|---|---|
| Liderazgo técnico | Docente Agustín Bustos orienta criterios y revisiones; equipo desarrolla y mantiene. |
| Disponibilidad | Depende del VPS y mantenimiento/deploy. No hay SLA formal documentado. |
| Seguridad | Acceso administrativo autenticado, secretos en entorno, HTTPS y controles de validación/autorización. |

### 1.4. Objetivos

- Centralizar y organizar información institucional y educativa.
- Facilitar consulta de carreras, cursos, noticias, eventos y comunicados.
- Proporcionar medios de contacto accesibles.
- Permitir administrar contenidos.
- Mejorar visibilidad mediante SEO/GEO.
- Evaluar SEM de forma planificada, sin afirmar campañas realizadas.
- Facilitar mantenimiento y evolución mediante arquitectura modular y pruebas.

### 1.5. Recursos y Entorno

- Repositorio GitHub y flujo de ramas/PR.
- Python 3.12, FastAPI, MySQL en producción y SQLite local/pruebas cuando corresponda.
- Hosting VPS, dominio institucional y despliegue.
- Equipo de estudiantes, referente técnico y herramientas de desarrollo.

### 1.6. Impacto Esperado

Se espera mejorar el acceso a información, comunicación, mantenibilidad y presencia en buscadores. No se dispone de métricas económicas ni ROI cuantificado.

### 1.7. Alcance del Sistema

- Sitio público y navegación.
- Información institucional y propuestas educativas.
- Noticias, eventos y comunicados.
- Formularios y canales de contacto.
- Panel administrativo de contenidos.
- SEO/GEO técnico y de contenidos.
- Prácticas de calidad, seguridad, pruebas y despliegue.

### 1.8. Fuera de Alcance (Out of Scope)

- Gestión académica integral, inscripción, calificaciones, legajos y asistencia.
- Pagos y comercio electrónico.
- DataMaq u otros sistemas ajenos al alcance.
- Agentes IA como funcionalidad runtime.
- Campañas SEM activas sin aprobación, presupuesto y evidencia.
- SLA, métricas de rendimiento o funcionalidades no auditadas.

### 1.9. Roles de Trabajo

| Rol | Responsabilidad |
|---|---|
| Docente/referente | Criterios técnicos, orientación, revisión/aprobación y despliegue. |
| Referente estudiantil | Coordinación del repositorio, revisión inicial, permisos y flujo de contribuciones. |
| Estudiantes | Ramas, desarrollo, pruebas, documentación y Pull Requests. |

### 1.10. Disponibilidad y Seguridad

La disponibilidad depende del hosting y servicios configurados. Se implementan controles para el panel, validación, protección de formularios y manejo de secretos. No se define SLA ni se afirma que todas las integraciones estén activas en producción.

---

## 2. Modelo de Negocio Canvas (BMC de 9 Bloques) & Gobernanza

### 2.1. Matriz del Business Model Canvas

| Bloque | Definición | Componentes |
|---|---|---|
| Socios clave (KP) | Institución, docente, hosting y proveedores. | VPS, dominio, repositorio y servicios configurados. |
| Actividades clave (KA) | Desarrollo, mantenimiento, contenidos, calidad y posicionamiento. | FastAPI, CRUD, testing, SEO/GEO y despliegues. |
| Recursos clave (KR) | Equipo, código, contenidos, infraestructura. | Repositorio, aplicación, datos, hosting y herramientas. |
| Propuesta de valor (VP) | Información centralizada, accesible y actualizable. | Portal público y contacto. |
| Relación (CR) | Autoservicio informativo y consulta. | Navegación, formularios y contacto. |
| Canales (CH) | Sitio y buscadores. | isftn199.com.ar y resultados orgánicos. |
| Segmentos (CS) | Aspirantes, estudiantes, docentes, personal y comunidad. | Visitantes del portal. |
| Costos | Hosting, dominio, mantenimiento, desarrollo y herramientas. | Infraestructura, recursos y servicios. |
| Ingresos | No aplica como producto comercial institucional. | No se documenta modelo de ingresos. |

### 2.2. Organigrama Operativo / Gobernanza de Agentes IA

No existen agentes IA integrados como componentes runtime. Las herramientas de IA se utilizan como apoyo al desarrollo, bajo revisión humana, y no forman parte de la arquitectura funcional del portal.

| Actor | Función |
|---|---|
| Docente/referente | Criterios, acompañamiento y revisión. |
| Referente estudiantil | Coordinación del repositorio y revisión inicial. |
| Equipo desarrollador | Implementación, pruebas, documentación y PRs. |
| Herramientas IA | Asistencia al desarrollo; no ejecutan funciones en producción. |

### 2.3. Escalera de Valor / Modelo de Conversión

No se aplica una escalera comercial. El recorrido institucional se interpreta como:

1. **Descubrimiento:** buscadores o enlaces.
2. **Consulta:** carreras, cursos, noticias, eventos y comunicados.
3. **Acción:** contacto o formularios.
4. **Seguimiento:** novedades y contenidos publicados.

---

## 3. Especificación de Requisitos de Software (SRS)

### 3.1. Requisitos Funcionales (FR)

| ID | Requisito |
|---|---|
| FR-01 | Presentar información institucional clara, organizada y accesible. |
| FR-02 | Permitir consultar propuestas educativas, carreras, cursos e información asociada. |
| FR-03 | Ofrecer navegación entre secciones y páginas. |
| FR-04 | Facilitar contacto mediante canales y formularios publicados. |
| FR-05 | Validar datos ingresados y aplicar controles servidor antes de procesarlos. |
| FR-06 | Permitir a usuarios autorizados gestionar contenidos desde el panel. |
| FR-07 | Administrar noticias; la publicación pública debe respetar su estado. |
| FR-08 | Administrar eventos y mostrar eventos publicados. |
| FR-09 | Administrar comunicados y mostrar los destinados a publicación. |
| FR-10 | Disponer de recursos técnicos y contenido que faciliten indexación cuando corresponda. |
| FR-11 | Contemplar datos estructurados apropiados para motores de búsqueda. |
| FR-12 | Aplicar prácticas GEO de organización/redacción y evaluar su efectividad. |
| FR-13 | Planificar/evaluar SEM; ejecución requiere aprobación, presupuesto y evidencia. |
| FR-14 | Adaptar interfaz a escritorio, tabletas y móviles. |

### 3.2. Requisitos No Funcionales (NFR)

| ID | Requisito |
|---|---|
| NFR-01 Usabilidad | Información y acciones comprensibles y fáciles de encontrar. |
| NFR-02 Compatibilidad | Funcionar en navegadores modernos compatibles. |
| NFR-03 Responsive | Adaptarse a distintos tamaños de pantalla. |
| NFR-04 Seguridad | Proteger áreas administrativas, credenciales y operaciones sensibles. |
| NFR-05 Validación | Validar datos antes de persistencia/procesamiento. |
| NFR-06 Mantenibilidad | Modularidad, separación de responsabilidades y convenciones. |
| NFR-07 SEO | Metadatos, estructura semántica, URLs y contenido apto para indexación. |
| NFR-08 Accesibilidad | Procurar semántica, navegación y prácticas accesibles; sin certificación declarada. |
| NFR-09 Rendimiento | Optimizar recursos críticos; no se fija latencia sin mediciones. |
| NFR-10 Disponibilidad | Depende del VPS y proveedores; sin SLA formal. |
| NFR-11 Protección de datos | Secretos fuera del repositorio y manejo seguro de datos de formularios. |
| NFR-12 Escalabilidad | Permitir evolución funcional y adaptación sin acoplamiento innecesario. |

### 3.3. Criterios de Aceptación

> Redactados a partir de funcionalidad verificada directamente en el código y los tests del repositorio (rutas reales, DTOs de validación, suite de pruebas ejecutada). Los requisitos marcados como aspiracionales o fuera de verificación (FR-12, FR-13) tienen un criterio que refleja esa limitación en lugar de afirmar una capacidad no comprobada.

| Requisito | Criterio de aceptación |
|---|---|
| FR-01 | Al solicitar la página de inicio (`GET /`), el sitio responde con código 200 y el HTML entregado contiene el nombre de la institución y al menos una carrera publicada en `data/content/carreras.yaml`. |
| FR-02 | Al solicitar el listado de carreras (`GET /carreras`) o de cursos (`GET /cursos`), el sitio responde 200 y el contenido mostrado coincide exactamente con lo declarado en `data/content/carreras.yaml` / `data/core/cursos/`, sin datos agregados en código ni en plantillas. |
| FR-03 | Toda página pública incluye una navegación (migas de pan y/o menú) con enlaces hacia las secciones principales del sitio (inicio, carreras, noticias, eventos, comunicados, contacto). En las páginas y rutas efectivamente verificadas en esta auditoría (home, carreras, cursos, noticias, panel), esos enlaces resuelven correctamente; no se realizó un rastreo exhaustivo de todos los enlaces de todas las páginas del sitio, por lo que no puede afirmarse que ninguno devuelva 404 en términos absolutos. |
| FR-04 | Al enviar el formulario de contacto (`POST /api/v1/contact`) con los campos obligatorios completos, el sitio responde 201 y **la consulta (lead) queda guardada en el repositorio de leads de forma incondicional**, verificado en el código (`SubmitLeadUseCase.execute()` llama a `repository.save(lead)` antes de intentar notificar). El **envío de la notificación** (email/Telegram, según los canales configurados en el entorno) es un paso posterior y de mejor esfuerzo: si falla, la respuesta indica `submitStatus: "partial_success"` en lugar de bloquear o perder la consulta. No se verificó en esta auditoría si los canales de notificación están efectivamente activos en producción (depende de variables de entorno del servidor, sin acceso en esta sesión). |
| FR-05 | Un envío al formulario de contacto sin email ni teléfono es rechazado con código 422 y un mensaje de validación explícito (no se persiste ningún dato incompleto). |
| FR-06 | Un usuario sin sesión iniciada que intenta acceder a `/panel` es redirigido al formulario de login; un usuario con sesión válida y rol `"autoridad"` accede al panel y ve las secciones de noticias, eventos y comunicados. |
| FR-07 | Una noticia creada desde el panel con `publicada = true` aparece en `GET /noticias`; si se marca `publicada = false`, deja de aparecer en el listado público y su página de detalle responde 404. |
| FR-08 | Análogo a FR-07, aplicado a `GET /eventos` y al estado de publicación de un evento. |
| FR-09 | Análogo a FR-07, aplicado a `GET /comunicados` y al estado de publicación de un comunicado. |
| FR-10 | `GET /sitemap.xml` y `GET /robots.txt` responden 200 y el sitemap incluye las URLs públicas reales del sitio (carreras, cursos, noticias, eventos, comunicados vigentes). |
| FR-11 | Las páginas de detalle de carrera, curso y noticia incluyen un bloque de datos estructurados (JSON-LD) con migas de pan coherentes con la navegación real de esa página. |
| FR-12 | **No verificable como práctica medible todavía.** El criterio actual se limita a que el contenido público use encabezados semánticos (`h1`/`h2`) y texto organizado por secciones, sin que exista en el repositorio un mecanismo de medición de efectividad GEO. Este requisito debería reformularse o posponerse hasta contar con esa evidencia. |
| FR-13 | La planificación y evaluación de campañas SEM forma parte de las actividades del Proyecto Integrador y fue asignada a otro integrante del equipo, no a quien realiza esta auditoría individual. Este criterio no se evalúa como cumplido, implementado ni pendiente desde esta auditoría. |
| FR-14 | Las páginas principales (inicio, carreras, noticias) no presentan desbordamiento horizontal ni contenido cortado en anchos de 390px (celular), 768px (tableta) y 1280px (escritorio). *(Criterio pendiente de verificación visual directa — no se comprobó con navegador en esta auditoría; se basa en el uso confirmado de CSS adaptable con media queries en el código, no en una captura real.)* |

### 3.4. Casos de Uso

> Casos de uso representativos, uno por cada flujo funcional distinto verificado. Noticias, eventos y comunicados comparten exactamente el mismo patrón de administración (confirmado en el código: mismas operaciones, misma protección CSRF, mismo esquema de permisos), por lo que se documenta una sola vez como caso de uso genérico en lugar de repetirlo tres veces.

**CU-01 — Consultar información de una carrera**
- **Actor:** Visitante del sitio (sin autenticación).
- **Objetivo:** Conocer los datos de una tecnicatura superior (duración, resolución, salida laboral).
- **Precondiciones:** La carrera existe y está publicada en `data/content/carreras.yaml`.
- **Flujo principal:**
  1. El visitante accede a `/carreras`.
  2. El sitio muestra el listado de carreras vigentes.
  3. El visitante selecciona una carrera y accede a `/carreras/{slug}`.
  4. El sitio muestra el detalle: duración, modalidad, turno, resolución, título otorgado y salida laboral.
- **Resultado:** El visitante obtiene la información oficial de la carrera sin necesidad de contactar a Secretaría.

**CU-02 — Enviar una consulta por el formulario de contacto**
- **Actor:** Aspirante o visitante interesado.
- **Objetivo:** Dejar sus datos de contacto para que Secretaría lo contacte.
- **Precondiciones:** Ninguna (formulario público).
- **Flujo principal:**
  1. El visitante accede a `/contact`.
  2. Completa nombre y al menos un dato de contacto (email o teléfono).
  3. Envía el formulario (`POST /api/v1/contact`).
  4. El sistema valida los datos con `ContactSubmitPayload` (longitud de campos, formato de email, regla de email-o-teléfono).
  5. Si la validación es correcta, el sistema responde 201 y guarda la consulta de forma incondicional en el repositorio de leads; intenta además notificar por los canales configurados (email/Telegram, según entorno), pero ese envío es de mejor esfuerzo y puede fallar sin afectar el registro ya guardado (ver criterio de aceptación de FR-04).
- **Flujo alternativo:** Si falta el campo `name` o no se informa ni email ni teléfono, el sistema responde 422 con el mensaje de error correspondiente y no se notifica nada.
- **Resultado:** La consulta queda registrada y disponible para seguimiento por parte de Secretaría.

**CU-03 — Administrar una noticia, evento o comunicado (caso genérico)**
- **Actor:** Usuario con rol `"autoridad"` y sesión activa.
- **Objetivo:** Publicar, actualizar o retirar contenido institucional (noticia/evento/comunicado).
- **Precondiciones:** El usuario inició sesión correctamente en `/login` y su cuenta tiene `rol = "autoridad"` y `is_active = true`.
- **Flujo principal:**
  1. El usuario accede al módulo del panel correspondiente al tipo de contenido (noticias, eventos o comunicados — por ejemplo, el listado administrativo de noticias en `/panel/noticias`).
  2. Selecciona la opción para crear un contenido nuevo, completa título y cuerpo, y opcionalmente sube una imagen.
  3. Envía el formulario; el sistema valida el token CSRF de la sesión y los campos obligatorios.
  4. Si la imagen subida no es un formato de imagen válido (verificado por contenido real, no solo por extensión), el sistema rechaza la carga con un mensaje de error y no persiste el registro.
  5. Si todo es válido, el sistema crea el contenido y lo marca según el estado de publicación elegido.
- **Flujo alternativo (edición/eliminación):** El usuario abre el contenido existente desde el listado administrativo del módulo correspondiente, elige editarlo o eliminarlo (por ejemplo, `/panel/noticias/{id}/editar` o `/panel/noticias/{id}/eliminar`), confirma el cambio, y el sistema actualiza o elimina el registro con la misma protección CSRF.
- **Resultado:** El contenido publicado (`publicada = true`) se vuelve visible de inmediato en la sección pública correspondiente; el no publicado permanece oculto.

**CU-04 — Intentar administrar contenido sin autorización**
- **Actor:** Usuario sin sesión, o con sesión pero sin rol `"autoridad"`.
- **Objetivo (del atacante o usuario erróneo):** Acceder al panel administrativo.
- **Precondiciones:** Ninguna sesión válida de autoridad.
- **Flujo principal:**
  1. El usuario intenta acceder a cualquier ruta bajo `/panel`.
  2. El sistema verifica la dependencia `require_authority`.
  3. Al no cumplirse, el sistema redirige a `/login` (sin sesión) o deniega el acceso (sesión con rol distinto).
- **Resultado:** Ninguna operación de administración se ejecuta; el contenido institucional permanece sin alteraciones.

---

## 4. Stack Tecnológico, Arquitectura Limpia & Convenciones (CONVENTIONS)

### 4.1. Stack Tecnológico Base

| Componente | Tecnología |
|---|---|
| Lenguaje | Python 3.12 |
| Framework | FastAPI |
| ASGI | Uvicorn |
| Schemas | Pydantic v2 |
| ORM | SQLAlchemy 2.0 async |
| Producción | MySQL + aiomysql |
| Local/pruebas | SQLite + aiosqlite según configuración |
| Templates | Jinja2 |
| Frontend | HTML, CSS, JavaScript vanilla; JSDoc/tsc |
| CSS | Tailwind CSS v4 y CSS institucional |
| Testing | Pytest, pytest-asyncio, httpx, pytest-xdist, pytest-cov |
| Calidad | Ruff, Pyright, tsc y scripts propios |
| Versionado | Git/GitHub |
| CI/CD | GitHub Actions, principalmente despliegue |

### 4.2. Estructura Canónica de Directorios (Screaming DDD + Clean Architecture)

```
.
├── src/
│   ├── domain/             # Entidades, reglas y contratos
│   ├── application/        # Casos de uso, DTOs y gateways
│   ├── adapters/           # Presenters y adaptación
│   └── infrastructure/     # FastAPI, persistencia, settings, integraciones
├── data/                   # Contenidos y configuración editorial
├── templates/              # Vistas Jinja2
├── static/                 # CSS, JS, imágenes y recursos
├── tests/                  # Pruebas
├── scripts/                # Validaciones y operación
├── .env.example            # Variables de ejemplo
└── .env                    # Configuración local; excluida de Git
```

### 4.3. Especificación de Configuración & Logging Centralizado

**A. Gestión de Entorno (`.env`, `.env.example`, `.gitignore`)**

- `.env` contiene configuración sensible y no debe versionarse.
- `.env.example` documenta variables con valores no secretos.
- Git debe excluir credenciales y archivos locales sensibles.
- Variables de entorno permiten configurar desarrollo y despliegue.

**B. Settings / Configuración**

La configuración se centraliza mediante Pydantic Settings. Se valida la configuración requerida y se contempla diferenciación por entorno. En producción `SECRET_KEY` debe estar definida; la aplicación no debe iniciar en modo no-debug si falta una clave requerida.

**C. Logging Centralizado**

El logging se configura centralizadamente y con niveles configurables. Los registros deben evitar exponer contraseñas, tokens, claves o información sensible.

### 4.4. Las Siete Reglas Innegociables de Arquitectura

> La plantilla denomina esta sección "Siete Reglas" aunque enumera ocho. Se conservan las ocho reglas enumeradas, adaptadas a lo verificado:

1. El dominio permanece independiente de frameworks, ORM y servicios externos.
2. Los casos de uso pertenecen a `application` y coordinan sin depender de detalles de infraestructura.
3. Las dependencias apuntan hacia capas internas; infraestructura implementa contratos.
4. Las rutas FastAPI actúan como adaptadores y delegan en casos de uso.
5. Los repositorios concretos encapsulan persistencia e implementan contratos.
6. Presenters adaptan datos para presentación sin lógica de negocio en templates.
7. Integraciones externas se abstraen y configuran mediante entorno.
8. Pruebas de arquitectura y calidad verifican restricciones relevantes.

El cumplimiento se verifica mediante pruebas/scripts; el alcance depende de las reglas implementadas.

---

## 5. Gobernanza Normativa, Calidad & Matriz de Pruebas

### 5.1. Filosofía de Desarrollo Asistido por Agentes IA (The Constraint Gauntlet)

Las herramientas IA pueden asistir en exploración, explicación y borradores. El equipo revisa cambios y conserva el criterio humano. La IA no es una funcionalidad del sistema en runtime.

- Mantener revisión humana.
- Aplicar restricciones de arquitectura, tipado, estilo, seguridad y pruebas.
- Evitar duplicación, código innecesario y sobreingeniería.
- Documentar cambios y trazabilidad Git/PR.

### 5.2. Las 11 Baterías del Guantelete (`tests/test_architecture.py`)

El repositorio incluye `tests/test_architecture.py`, `tests/test_clean_design.py` y `tests/test_god_components.py`. Verifican restricciones arquitectónicas y señales de diseño no deseado. La cantidad y reglas deben mantenerse sincronizadas con el código.

- Separación de capas y dirección de dependencias.
- Restricciones de imports y aislamiento del dominio.
- Delegación de rutas a casos de uso.
- Detección de componentes excesivamente grandes o responsabilidades concentradas.
- Convenciones y restricciones de diseño.

### 5.3. Detección Determinística de Código Muerto y Sobreingeniería (`tests/test_clean_design.py`)

Validaciones buscan código residual, estructuras innecesarias y desviaciones de convenciones. Deben complementarse con revisión humana, ya que resultados automatizados requieren interpretación.

### 5.4. Estándares de Calidad, Trazabilidad & Commits Atómicos

- Trabajo mediante ramas y Pull Requests; no push directo a ramas permanentes.
- Ramas permanentes: `main` (producción) y `develop` (integración).
- Convención de ramas documentada.
- Conventional Commits.
- PRs sujetos a revisión y reglas de protección configuradas.
- Vincular cambios a tareas, pruebas y documentación cuando corresponda.
- No incluir secretos en commits.
- Dependencias mayormente fijadas, pero existen rangos; no se declara reproducibilidad total.

### 5.5. Matriz de Verificación Automatizada Previa a Despliegues

El pre-push local ejecuta nueve verificaciones. GitHub Actions se utiliza principalmente para despliegue y no equivale a ejecutar todas las validaciones locales.

| Control | Objetivo |
|---|---|
| 1. CSS crítico | Validación/actualización de recursos CSS críticos. |
| 2. Tailwind | Verificación/generación de CSS. |
| 3. YAML/contenidos | Validar datos y contenidos. |
| 4. HTML/templates | Validar plantillas. |
| 5. Arquitectura | Controles arquitectónicos. |
| 6. Ruff | Linting. |
| 7. Pyright | Chequeos de tipos. |
| 8. tsc | Chequeos JS/JSDoc. |
| 9. Tests/cobertura | Suite y umbral de cobertura. |

Auditoría puntual sobre `main`: 1.068 pruebas aprobadas sin fallos y cobertura registrada de 88,42 %. El umbral mínimo establecido es 85 %. Estos valores corresponden a esa ejecución y no garantizan resultados idénticos en otros commits/ramas.

### 5.6. Configuración del Editor (Pylance / VS Code)

- VS Code con Python y Pylance.
- Seleccionar intérprete del entorno virtual.
- Aplicar formato, linting y chequeos configurados.
- Respetar Ruff y Pyright y ejecutar validaciones antes de PR.
- Las instrucciones para asistentes IA son documentación, no componentes runtime.

---

## Limitaciones, Riesgos y Mejoras Futuras

### Limitaciones conocidas

- Dependencia de hosting VPS y configuración del entorno.
- Rol administrativo verificado de autoridad única; no se documenta granularidad de permisos.
- `/ready` puede exponer detalles internos de error; requiere revisión.
- SMTP, Telegram y GA4 tienen mecanismos/configuración, pero activación en producción no verificada.
- Operación de dashboards Prometheus y `/metrics` no verificada.
- No todas las dependencias están fijadas a versiones exactas.
- Pruebas/cobertura citadas corresponden a auditoría puntual de `main`.

### Mejoras futuras

- Revisar readiness y evitar exposición de errores.
- Documentar/verificar integraciones por entorno.
- Evaluar permisos granulares si la institución lo requiere.
- Medir rendimiento y establecer objetivos con línea base.
- Mejorar accesibilidad, SEO y GEO mediante evaluaciones.
- SEM solo con planificación, aprobación y medición documentada.
- Actualizar documentación y pruebas junto con la arquitectura.

---

## Consideraciones Finales

Esta especificación es una base consolidada de requisitos, arquitectura, convenciones y gobernanza del Proyecto Web Institucional ISFT N.º 199. Debe mantenerse junto con el repositorio. Las afirmaciones sobre funcionalidades, integraciones, métricas y operación deben actualizarse con evidencia, distinguiendo requisitos, objetivos, implementaciones parciales y capacidades activas.

Documento preparado para revisión del equipo y docente/referente técnico.
