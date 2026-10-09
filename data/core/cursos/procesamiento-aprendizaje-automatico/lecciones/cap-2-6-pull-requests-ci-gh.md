# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.6: Pull Requests y CI: Qué Son y Cómo Consultarlos desde la Terminal

En la lección 2.5 leímos tareas con `gh`. En esta lección conocemos dos piezas del trabajo en equipo que vas a encontrar en cualquier proyecto profesional: la **Pull Request (PR)** y la **Integración Continua (CI)**. No vas a abrir ninguna PR en esta lección. El objetivo es que sepas qué es, cómo se propone un cambio y cómo consultar el resultado de las pruebas.

---

## Objetivos de Aprendizaje

1. Entender qué es una Pull Request y por qué un cambio se revisa antes de integrarse.
2. Entender qué es un fork y por qué un alumno trabaja en uno en lugar de publicar en el repositorio original.
3. Consultar corridas de CI con `gh run list` y `gh run view`.
4. Reconocer el comando que lee el registro de un fallo (`gh run view --log-failed`).
5. Listar PRs en JSON con `gh pr list --json`.

---

## 1. ¿Qué Es una Pull Request?

Una Pull Request es una solicitud para integrar los cambios de una rama en otra. Quien propone el cambio la abre, y otra persona la revisa: lee el diff, comenta y aprueba o pide cambios. Recién después se integra a la rama principal.

El ciclo típico es:

```
rama de trabajo ──commits──> Pull Request ──> CI (pruebas) ──> revisión ──> merge a main
```

Cada PR debe tener un solo propósito, para que la revisión sea fácil de seguir.

---

## 2. ¿Por Qué un Fork?

Los alumnos no tienen permiso para publicar ramas en el repositorio del caso de estudio. Por eso, cuando un alumno necesita proponer un cambio, trabaja en un **fork**: una copia del repositorio que queda bajo su cuenta. Desde el fork abre la PR hacia el repositorio original.

Un fork se crea con este comando (referencia, no lo ejecutes en esta lección):

```bash
gh repo fork datamaq-automation/energy-ml --remote-name fork
```

Y una PR se abre con `gh pr create` (también solo referencia):

```bash
gh pr create --repo datamaq-automation/energy-ml --base main --head <tu-usuario>:<rama>
```

---

## 3. Consultar el CI

`energy-ml` no tiene workflows de Integración Continua. Para ver cómo se consulta el CI usamos el repositorio de la materia, `solareco86-ai/proyecto-integrador`, que sí ejecuta pruebas automáticas. Estos comandos solo leen información; no modifican nada.

```bash
# Listar las ejecuciones recientes de los workflows
gh run list -R solareco86-ai/proyecto-integrador -L 5
```

Cada fila muestra el estado (`completed`, `in_progress`), el resultado (`success`, `failure`), el nombre del workflow, la rama y la fecha.

```bash
# Ver el detalle de una ejecución (reemplaza <id> por uno de la lista)
gh run view <id> -R solareco86-ai/proyecto-integrador
```

### Leer el registro de un fallo

Si una ejecución falla, `--log-failed` muestra solo los pasos que fallaron:

```bash
gh run view <id> --log-failed -R solareco86-ai/proyecto-integrador
```

Un agente de IA usaría este comando para leer la traza del error antes de proponer una corrección. Esa corrección se audita con `git diff`, como en la lección 2.2.

---

## 4. Listar PRs en JSON

Igual que con los Issues en la lección 2.5, puedes pedir solo los campos que necesitas. Este comando también es solo de lectura:

```bash
gh pr list -R solareco86-ai/proyecto-integrador --state all -L 5 --json number,title,state,headRefName
```

**Salida estructurada (ejemplo):**

```json
[
  {
    "headRefName": "feat/redondeo-potencia",
    "number": 42,
    "state": "OPEN",
    "title": "feat(domain): redondear consumo a 3 decimales"
  }
]
```

---

## Checkpoint de Verificación

Antes de avanzar a la lección 2.7 (Issues, Projects y Wiki):
- [ ] Explicas con tus palabras qué es una Pull Request y quién la revisa.
- [ ] Entiendes por qué un alumno trabaja en un fork y no en el repositorio original.
- [ ] Consultaste corridas de CI con `gh run list` y leíste una con `gh run view`.
- [ ] Sabes qué hace `gh run view --log-failed`.
- [ ] Listaste PRs en JSON con `gh pr list --json`.
