# Guía de Contribución y Trabajo Colaborativo

> **Repositorio:** Portal Institucional y Campus Virtual — ISFT N° 199  
> **Rama de producción:** `main` · **Rama de integración:** `develop`

---

## 1. Roles y Responsabilidades

| Rol | Usuario(s) | Permisos en GitHub |
|---|---|:---:|
| **Profesor / Responsable Técnico** | Agustín Bustos (fuera del repo) | — |
| **Alumna Referente / Administradora** | `solareco86-ai` | Admin |
| **Alumna** | `VeroJuarez`, `mili-len` y otros | Write |
| **Automatización CI/CD** | `datamaq-automation` | Write |

### 1.1 Profesor
- Define los criterios técnicos y pedagógicos del proyecto.
- Revisa y aprueba Pull Requests de `develop → main` antes de cada despliegue a producción.
- **No trabaja directamente en el repositorio:** orienta y valida a través de la Alumna Referente.

### 1.2 Alumna Referente (`solareco86-ai`)
- Es la administradora del repositorio en GitHub.
- **Primera responsable** de revisar y aprobar Pull Requests hacia `develop`.
- Puede hacer merge a `main` previa consulta y aprobación del Profesor.
- Gestiona permisos, ramas protegidas y configuración del repositorio.

### 1.3 Alumna
- Trabaja exclusivamente en su **rama personal** (ver sección 3).
- Hace Pull Requests hacia `develop` al finalizar cada clase.
- No tiene permiso de hacer push directo a `develop` ni a `main`.


---

## 2. Estructura de Ramas

```
main          ← Producción (isftn199.com.ar). Solo el Profesor hace merge aquí.
 └── develop  ← Integración. Base de trabajo de todos los colaboradores.
       └── alumno/<nombre>/<tarea>  ← Rama personal de cada alumno.
       └── feat/<descripcion>       ← Funcionalidades nuevas (código).
       └── content/<descripcion>    ← Contenido del campus (lecciones, YAML).
       └── fix/<descripcion>        ← Corrección de errores.
```

### Reglas de protección

| Regla | `main` | `develop` |
|---|:---:|:---:|
| Push directo permitido | ❌ | ❌ |
| Requiere Pull Request | ✅ | ✅ |
| Aprobaciones requeridas | **1 (Profesor)** | **1 (Referente o Profesor)** |
| Reviews obsoletos se descartan al nuevo push | ✅ | ✅ |
| Force push permitido | ❌ | ❌ |

---

## 3. Convención de Nombres de Ramas

Todas las ramas se crean **desde `develop`**, nunca desde `main`.

| Tipo | Patrón | Ejemplo |
|---|---|---|
| Rama personal de alumno | `alumno/<nombre>/<tarea-kebab-case>` | `alumno/vero-juarez/leccion-3-opencv` |
| Nueva funcionalidad (código) | `feat/<descripcion-kebab-case>` | `feat/buscador-cursos` |
| Nuevo contenido (lecciones/cursos) | `content/<descripcion-kebab-case>` | `content/curso-opencv-morfologia` |
| Corrección de error | `fix/<descripcion-kebab-case>` | `fix/quiz-respuestas-erroneas` |
| Mantenimiento y configs | `chore/<descripcion-kebab-case>` | `chore/actualizar-dependencias` |

---

## 4. Flujo de Trabajo por Clase

```
┌─────────────────────────────────────────────────────────────┐
│ Inicio de clase                                             │
│  git checkout develop && git pull origin develop            │
│  git checkout -b alumno/<tu-nombre>/<tarea-de-hoy>          │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (trabajás durante la clase)
┌─────────────────────────────────────────────────────────────┐
│ Al finalizar la clase                                       │
│  git add .                                                  │
│  git commit -m "tipo(scope): descripción breve"             │
│  git push origin alumno/<tu-nombre>/<tarea>                 │
│  → Abrir Pull Request hacia develop en GitHub               │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (Referente o Profesor revisa)
┌─────────────────────────────────────────────────────────────┐
│ Revisión del PR                                             │
│  ✅ Todo en orden → Merge a develop                         │
│  🔄 Hay observaciones → Alumno corrige y hace nuevo push    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼ (acumulado de varias clases)
┌─────────────────────────────────────────────────────────────┐
│ Release a producción (solo el Profesor)                     │
│  PR: develop → main → Deploy automático en GitHub Actions   │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. Requisitos Mínimos para que un PR sea Revisable

Un Pull Request **no será revisado** si no cumple estos requisitos:

- [ ] **El pre-push hook local pasó sin errores** (linter Ruff, Pyright, tests con cobertura ≥ 85 %).
- [ ] **La rama sigue la convención de nombres** (sección 3).
- [ ] **El título del PR usa Conventional Commits** (ver sección 6).
- [ ] **El PR tiene una descripción** que explique qué se hizo y por qué.

---

## 6. Convención de Commits (Conventional Commits)

```
<tipo>(<alcance>): <descripción breve en minúsculas>
```

| Tipo | Cuándo usarlo |
|---|---|
| `feat` | Nueva funcionalidad o ruta |
| `content` | Lección, curso o contenido YAML nuevo |
| `fix` | Corrección de un error |
| `refactor` | Refactorización sin cambio de comportamiento |
| `test` | Agregado o corrección de tests |
| `chore` | Mantenimiento, actualización de dependencias |
| `docs` | Solo documentación |

**Ejemplos válidos:**
```
content(cursos): agregar lección 3.2 de OpenCV sobre morfología
feat(campus): implementar buscador de cursos por palabra clave
fix(quiz): corregir respuesta correcta en pregunta sobre Canny
```

---

## 7. Configuración Inicial para Nuevos Colaboradores

```bash
# 1. Clonar el repositorio
git clone git@github.com:solareco86-ai/proyecto-integrador.git
cd proyecto-integrador

# 2. Crear el entorno virtual e instalar dependencias
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Instalar dependencias de Node.js (CSS y TypeScript)
npm install

# 4. Verificar que todo funciona antes del primer commit
./.venv/bin/pytest

# 5. Posicionarse en develop (rama base de trabajo)
git checkout develop
git pull origin develop
```

---

## 8. Preguntas Frecuentes

**¿Puedo hacer push directo a `develop` o `main`?**  
No. Todo cambio entra por Pull Request para garantizar revisión pedagógica y técnica.

**¿Qué pasa si mi PR tiene conflictos?**  
Resolvé los conflictos haciendo `git merge develop` en tu rama local, commit con la resolución y push nuevamente.

**¿Puedo trabajar en la misma rama más de una clase?**  
Sí, siempre que la rama corresponda a una misma tarea atómica. Si empezás algo nuevo, creá una rama nueva desde `develop` actualizado.

**¿Qué hago si el pre-push hook me rechaza el push?**  
Leé el error del hook (Ruff, Pyright o Pytest), corregilos localmente y volvé a intentar el push.
