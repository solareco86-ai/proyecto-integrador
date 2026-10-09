# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.7: Issues, Projects y Wiki desde la Terminal (`gh issue`, `gh project`, `gh browse`)

En la lección 2.5 leímos Issues y en la 2.6 abrimos Pull Requests. En esta lección completamos la gestión del trabajo: creamos Issues, los organizamos en un Project y ubicamos la Wiki del repositorio.

Un **Issue** registra una tarea, un defecto o una propuesta. Un **Project** es un tablero que agrupa Issues y PRs por estado. La **Wiki** es un espacio de documentación del repositorio, separado del código.

---

## Objetivos de Aprendizaje

1. Crear un Issue con `gh issue create` y relacionarlo con un Project.
2. Agregar un Issue o un PR a un Project con `gh project item-add`.
3. Ubicar la Wiki del repositorio con `gh browse --wiki` y clonarla con Git.
4. Reconocer qué permisos (scopes) necesita `gh` para cada acción.

---

## 1. Crear un Issue

Un Issue bien escrito tiene un título claro y una descripción con el contexto y el criterio de aceptación. Los Issues de la materia se crean en `solareco86-ai/proyecto-integrador`:

```bash
gh issue create -R solareco86-ai/proyecto-integrador \
  --title "Redondear el consumo a 3 decimales" \
  --body "El cálculo de kWh debe redondear a 3 decimales. Criterio: pytest pasa y el redondeo queda cubierto por un test."
```

Para una descripción más larga, escríbela en un archivo y pásalo con `--body-file`:

```bash
gh issue create -R solareco86-ai/proyecto-integrador --title "Redondear el consumo a 3 decimales" --body-file descripcion.md
```

> [!NOTE]
> Las etiquetas (`--label`) solo se pueden usar si ya existen en el repositorio. Si no existen, `gh` muestra un error. Consulta con el docente cuáles hay disponibles.

---

## 2. Projects: Organizar el Trabajo

Un Project agrupa Issues y PRs en un tablero. Para operar sobre Projects, `gh` necesita el scope `project` en su token.

### Paso 1: Verificar y agregar el scope

```bash
# Ver los scopes actuales del token
gh auth status

# Agregar el scope project si falta
gh auth refresh -s project
```

### Paso 2: Listar los Projects

```bash
gh project list --owner "@me"
```

### Paso 3: Agregar un Issue al Project

Hay dos formas. La primera crea el Issue y lo agrega al Project en un solo paso, usando el título del Project:

```bash
gh issue create -R solareco86-ai/proyecto-integrador --title "Redondear el consumo a 3 decimales" --project "Nombre del Project"
```

La segunda agrega un Issue o PR que ya existe, usando su URL:

```bash
gh project item-add <número-del-project> --owner <propietario> --url https://github.com/<owner>/<repo>/issues/<número>
```

Reemplaza `<número-del-project>`, `<propietario>` y la URL por los valores reales del tablero que te indiquen.

---

## 3. La Wiki del Repositorio

`gh` no tiene un comando propio para la Wiki. Hay dos caminos:

**Abrirla en el navegador:**

```bash
gh browse --wiki
```

**Obtener la dirección sin abrir el navegador:**

```bash
gh browse --wiki -n
```

**Clonarla como repositorio Git**, para editar sus páginas en tu máquina. La Wiki es un repositorio separado, con el nombre del repositorio seguido de `.wiki`:

```bash
git clone https://github.com/<owner>/<repo>.wiki.git
```

> [!NOTE]
> GitHub crea la Wiki como repositorio Git recién cuando se guarda la primera página desde el navegador. Si `git clone` responde `Repository not found`, la Wiki todavía no tiene páginas: ábrela con `gh browse --wiki`, crea la primera página y vuelve a intentar el clonado.

---

## Checkpoint de Verificación del Capítulo 2

Has finalizado el **Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml**. Antes de avanzar al Capítulo 3, verifica:
- [ ] Creaste un Issue con `gh issue create` y sabes cuándo usar `--body-file`.
- [ ] Verificaste el scope `project` y listaste los Projects con `gh project list`.
- [ ] Sabes agregar un Issue o PR a un Project, por título o por URL.
- [ ] Ubicaste la Wiki con `gh browse --wiki -n` y sabes clonarla con `git clone`.
- [ ] Tu entorno está listo para el Capítulo 3, asistentes de IA (OpenCode y Antigravity CLI).
