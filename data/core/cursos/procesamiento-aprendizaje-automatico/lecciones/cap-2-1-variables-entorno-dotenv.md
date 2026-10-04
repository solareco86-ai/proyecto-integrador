# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.1: Variables de Entorno (`.env`), Resguardo de Credenciales y Línea Base con `pytest`

Bienvenido al **Capítulo 2**. En este capítulo asumiremos el rol de **auditores técnicos**: aprenderemos a inspeccionar diffs, discriminar propuestas de asistentes de IA, aplicar staging selectivo (`git add -p`) y gestionar marchas atrás seguras (`git restore`, `reset` y `revert`), trabajando directamente sobre el repositorio real **`energy-ml`**.

Antes de auditar o modificar código, la regla número uno de la ingeniería de software es **establecer la línea base (*baseline*) de seguridad y pruebas**.

---

## Objetivos de Aprendizaje

1. Comprender la función crítica de las variables de entorno en la configuración de proyectos de Machine Learning.
2. Gestionar la separación entre plantillas públicas (`.env.example`) y credenciales locales privadas (`.env`).
3. Auditar la protección de secretos mediante las reglas de exclusión de `.gitignore` con `git status`.
4. Ejecutar la validación inicial con `pytest -q` para certificar que el repositorio parte de un estado 100% en verde antes de cualquier intervención.

---

## 1. El Principio de Secreto y Configuración

En proyectos profesionales de Inteligencia Artificial y Machine Learning:
* **Separación de Código y Configuración:** Las rutas a bases de datos, llaves de API (OpenAI, Anthropic, Gemini), puertos de servidores y modos de depuración varían entre la computadora del alumno y el servidor de producción. Nunca deben escribirse fijas en el código fuente.
* **La Tríada de Archivos:**
  1. `.env.example`: Archivo público versionado en Git que documenta qué variables necesita el proyecto, usando valores de ejemplo vacíos.
  2. `.env`: Archivo local privado que contiene los valores reales. **Nunca se sube a Git**.
  3. `.gitignore`: Archivo de texto que le indica a Git qué archivos ignorar permanentemente para no filtrar secretos ni binarios pesados.

---

## 2. Paso a Paso: Configuración de Variables en `energy-ml`

### Paso 1: Inspeccionar la protección en `.gitignore`
Antes de crear cualquier archivo con secretos, verifica que el `.gitignore` de `energy-ml` contenga las reglas de protección:

```bash
# Comprobar que venv y .env están protegidos
grep -E "(venv|\.env)" .gitignore
```

Observarás que tanto `.env` como `venv/` están declarados para ser ignorados por Git.

---

### Paso 2: Crear el Archivo `.env` desde la Plantilla
Copia la plantilla oficial `.env.example` para generar tu archivo de configuración local:

```bash
cp .env.example .env
```

---

### Paso 3: Auditoría con `git status`
Comprueba que Git no rastrea tu nuevo archivo `.env`:

```bash
git status
```

Git debe informar `nothing to commit, working tree clean` (o no listar el archivo `.env`). Si `.env` apareciera como archivo no rastreado (*Untracked*), significaría que el `.gitignore` no está funcionando y existiría riesgo de fuga de credenciales.

---

### Paso 4: Inspeccionar la Configuración Local
Visualiza las variables definidas para el proyecto `energy-ml`:

```bash
cat .env
```

Encontrarás configuraciones para el entorno de desarrollo, el puerto del servidor (`PORT=8000`), el nivel de logging y las rutas de almacenamiento de datos.

---

## 3. Línea Base en Verde: Ejecución Inicial de `pytest`

Para certificar que el repositorio parte de un estado sano antes de auditar o refactorizar código en las siguientes lecciones, corre la suite completa de pruebas:

```bash
# Ejecutar las pruebas unitarias con pytest
pytest -q
```

**Salida esperada (solo lectura):**

```output
........                                                         [100%]
8 passed in 0.42s
```

> [!IMPORTANT]
> **La Línea Base (*Baseline*):** Si las pruebas no pasan antes de empezar a trabajar, nunca sabrás si un error futuro fue introducido por una sugerencia alucinada de la IA o si ya existía de antemano. Todo ciclo de auditoría comienza con una suite de pruebas en verde.

---

## Checkpoint de Auditoría

Antes de avanzar a la inspección analítica de `git diff` en la lección 2.2:
- [ ] Tu terminal está posicionada en `aprendizaje-automatico/energy-ml/`.
- [ ] El entorno virtual `venv` está activado (`(venv)` visible en el prompt).
- [ ] El archivo `.env` existe en la raíz de `energy-ml/`.
- [ ] `git status` no muestra archivos no deseados ni secretos expuestos.
- [ ] La ejecución de `pytest -q` corre satisfactoriamente con todas las pruebas aprobadas (línea base fijada).
