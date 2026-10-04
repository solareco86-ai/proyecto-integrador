# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.5: GitHub CLI (`gh`): Automatización de Pull Requests, Issues y Gobernanza para Agentes de IA

En las lecciones anteriores dominamos el control de versiones en nuestra máquina local: inspeccionamos diffs, filtramos alucinaciones con `git add -p`, aprendimos a retroceder con `git restore/reset/revert` y registramos un commit atómico limpio en `energy-ml`.

Sin embargo, el ciclo de vida del software profesional no termina en tu disco local. En equipos de ingeniería y entornos con **agentes autónomos de Inteligencia Artificial**, el código debe someterse a revisión por pares (*Code Review*), integrarse mediante *Pull Requests* y validarse en servidores de Integración Continua (CI/CD). Para este propósito entra en juego una herramienta complementaria indispensable: **GitHub CLI (`gh`)**.

---

## Objetivos de Aprendizaje

1. Comprender la complementariedad entre `git` (control de versiones local) y `gh` (orquestación remota de GitHub desde la terminal).
2. Entender por qué los agentes autónomos de IA utilizan `gh` en lugar de la interfaz web gráfica.
3. Dominar los comandos esenciales de `gh`: autenticación (`gh auth`), gestión de incidentes (`gh issue`), creación de solicitudes de cambios (`gh pr`) y observabilidad de pipelines (`gh run`).
4. Aprender a extraer salidas estructuradas en formato JSON (`--json` y `--jq`), la técnica que permite a los agentes procesar datos con mínimo consumo de tokens.

---

## 1. La Complementariedad: `git` vs. `gh`

Es crucial no confundir ambas herramientas:

```
┌────────────────────────────────────────────────────────┐
│                      Tu Terminal                       │
├──────────────────────────┬─────────────────────────────┤
│        Git CLI           │       GitHub CLI (`gh`)     │
├──────────────────────────┼─────────────────────────────┤
│ • Opera sobre el disco.  │ • Opera sobre la API remota.│
│ • Commits, ramas, diffs. │ • Pull Requests, Issues.    │
│ • Árbol de trabajo local.│ • GitHub Actions, Releases. │
│ • Motor de bajo nivel.   │ • Plataforma colaborativa.  │
└──────────────────────────┴─────────────────────────────┘
```

* **`git`** no sabe qué es un Pull Request ni qué es un Issue; Git solo entiende de grafos de commits, árboles y blobs en tu máquina.
* **`gh`** es la herramienta oficial de GitHub que te permite gestionar toda la plataforma colaborativa (abrir PRs, comentar issues, inspeccionar pipelines de prueba) **directamente desde la consola de comandos**.

---

## 2. ¿Por qué le damos `gh` a los Agentes de IA?

Cuando incorporamos herramientas agénticas (como Aider, OpenCode, Claude Code o agentes con integración MCP):

1. **Entorno *Headless* (Sin Interfaz Gráfica):** Los agentes corren en terminales, contenedores Docker o servidores de desarrollo. No tienen un mouse ni un navegador web para hacer clic en el botón verde *"New Pull Request"*.
2. **Automatización Integral del Ciclo de Vida:** Con `gh`, un agente puede:
   - Leer las especificaciones de una tarea desde un issue: `gh issue view 12`.
   - Crear una rama de desarrollo: `git checkout -b fix/issue-12`.
   - Implementar y confirmar los cambios: `git commit -m "fix: ..."`.
   - Abrir la Pull Request automáticamente: `gh pr create --fill`.
   - Esperar y verificar el resultado de las pruebas remotas: `gh pr checks`.
3. **Salidas en JSON sin Ruido Visual:** Con la bandera `--json`, los LLMs reciben únicamente los datos estructurados que necesitan sin gastar tokens en elementos gráficos de HTML.

---

## 3. Comandos Esenciales de GitHub CLI (`gh`)

### Paso 1: Comprobación de Autenticación
Para verificar si tu terminal está conectada con tu cuenta de GitHub:

```bash
gh auth status
```

**Salida esperada (solo lectura):**

```output
github.com
  ✓ Logged in to github.com account tu-usuario (keyring)
  - Active account: true
  - Git operations protocol: https
```

> [!NOTE]
> Si aún no has autenticado tu terminal en tu computadora personal, puedes hacerlo en cualquier momento ejecutando `gh auth login` y seleccionando la opción interactiva vía navegador o token de acceso personal (PAT).

---

### Paso 2: Exploración de Issues del Proyecto
Para consultar las tareas pendientes registradas en el repositorio sin abrir el navegador:

```bash
# Listar los últimos issues abiertos
gh issue list

# Ver el detalle técnico de un issue específico
gh issue view 1
```

---

### Paso 3: Creación Automatizada de una Pull Request
En la lección 2.4 registramos un commit atómico en `energy-ml`. Si estuviéramos trabajando en una rama temática (`feat/redondeo-potencia`), el comando para proponer la integración del código es:

```bash
# 1. Crear y cambiar a una rama de trabajo
git checkout -b feat/redondeo-potencia

# 2. Publicar la rama en tu fork remoto
git push -u origin feat/redondeo-potencia

# 3. Crear la Pull Request desde la terminal con un solo comando
gh pr create \
  --title "feat(domain): agregar redondeo a 3 decimales en calculo de consumo" \
  --body "Auditoría completada: Se validó la fórmula matemática, se descartaron umbrales erróneos y la suite de pytest corre 100% en verde."
```

Inmediatamente, `gh` emite la URL pública de la Pull Request creada en GitHub:

```output
https://github.com/datamaq-automation/energy-ml/pull/42
```

---

### Paso 4: Monitoreo de Pipelines de CI/CD (`gh run`)
Para comprobar el estado de los tests automatizados que se disparan en GitHub Actions tras abrir el PR:

```bash
# Listar las ejecuciones recientes de CI
gh run list

# Ver el resultado de la última corrida en tiempo real
gh run view
```

Si el pipeline remoto de pruebas falla, un agente de IA puede leer la traza del error con `gh run view --log-failed` y generar un nuevo commit de reparación automáticamente.

---

## 4. El Superpoder Agéntico: Extracción Estructurada con `--json`

Cuando los humanos usamos la consola, leemos texto formateado. Pero cuando un agente de IA utiliza `gh`, utiliza la bandera `--json` para recibir información en formato nativo consumible por sus herramientas internas:

```bash
# Obtener número, título y estado de las PRs abiertas en JSON compacto
gh pr list --json number,title,state,headRefName
```

**Salida estructurada:**

```json
[
  {
    "headRefName": "feat/redondeo-potencia",
    "number": 42,
    "state": "OPEN",
    "title": "feat(domain): agregar redondeo a 3 decimales en calculo de consumo"
  }
]
```

Esta articulación entre la terminal Bash, Git de bajo nivel y `gh` es el cimiento técnico que utilizaremos en el **Capítulo 3** para poner a trabajar a nuestros asistentes de IA (Aider, OpenCode y AGY CLI).

---

## Checkpoint de Verificación

Has finalizado con éxito el **Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml**:
- [ ] Comprendes la diferencia de rol entre `git` (local) y `gh` (remoto).
- [ ] Sabes por qué los agentes autónomos de IA requieren `gh` para operar de forma desatendida.
- [ ] Conoces el flujo para abrir una Pull Request desde la consola con `gh pr create`.
- [ ] Entiendes la utilidad de la bandera `--json` para alimentar agentes de lenguaje con datos precisos.
- [ ] Tu entorno está listo para adentrarse en la tríada de asistentes de IA en el Capítulo 3.
