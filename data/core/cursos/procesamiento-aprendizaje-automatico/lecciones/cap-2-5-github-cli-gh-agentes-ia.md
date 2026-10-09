# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.5: GitHub CLI (`gh`): Autenticación y Lectura de Issues para Agentes de IA

En las lecciones anteriores trabajamos el control de versiones en nuestra máquina local: inspeccionamos diffs, filtramos cambios con `git add -p` y aprendimos a retroceder con `git restore`, `git reset` y `git revert`.

Pero el trabajo profesional no termina en el disco local. Las tareas viven en GitHub como *Issues*, los cambios se proponen como *Pull Requests* y las pruebas remotas corren en servidores de Integración Continua. Para operar sobre todo eso desde la terminal usamos **GitHub CLI (`gh`)**. En esta lección vemos lo básico: autenticarnos y leer las tareas. La creación de Pull Requests, el seguimiento de CI y los Projects se ven en las lecciones 2.6 y 2.7.

---

## Objetivos de Aprendizaje

1. Comprender la complementariedad entre `git` (control de versiones local) y `gh` (plataforma remota de GitHub desde la terminal).
2. Entender por qué los agentes autónomos de IA usan `gh` en lugar de la interfaz web.
3. Verificar la autenticación con `gh auth status` y leer Issues con `gh issue list` y `gh issue view`.
4. Extraer datos en formato JSON con `--json` y `--jq`, para que un agente procese solo la información que necesita.

---

## 1. La Complementariedad: `git` vs. `gh`

```
┌────────────────────────────────────────────────────────┐
│                      Tu Terminal                       │
├──────────────────────────┬─────────────────────────────┤
│        Git CLI           │       GitHub CLI (`gh`)     │
├──────────────────────────┼─────────────────────────────┤
│ • Opera sobre el disco.  │ • Opera sobre la API remota.│
│ • Commits, ramas, diffs. │ • Issues, Pull Requests.    │
│ • Árbol de trabajo local.│ • GitHub Actions, Projects. │
│ • Motor de bajo nivel.   │ • Plataforma colaborativa.  │
└──────────────────────────┴─────────────────────────────┘
```

* **`git`** no sabe qué es un Pull Request ni qué es un Issue. Solo entiende commits, ramas y árboles en tu máquina.
* **`gh`** gestiona la plataforma colaborativa desde la consola: lee tareas, abre solicitudes de cambio y consulta pipelines.

---

## 2. ¿Por qué los Agentes de IA usan `gh`?

1. **Entorno *headless* (sin interfaz gráfica):** Los agentes corren en terminales, contenedores o servidores. No tienen mouse ni navegador para hacer clic en un botón.
2. **Automatización del ciclo de vida:** Un agente puede leer la especificación de una tarea desde un Issue, implementar el cambio con `git` y consultar el estado de su trabajo con `gh`.
3. **Salidas en JSON:** Con `--json`, el modelo recibe solo los datos estructurados que necesita, sin texto decorativo que consuma tokens.

---

## 3. Comandos Esenciales de Lectura

### Paso 1: Comprobar la autenticación

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
> Si todavía no autenticaste `gh` en tu computadora, ejecuta `gh auth login` y elige la opción interactiva por navegador. Para consultar y, más adelante, crear recursos necesitas además el scope `project` (lección 2.7).

### Paso 2: Leer Issues desde la terminal

Los Issues de la materia viven en `solareco86-ai/proyecto-integrador`, porque `energy-ml` tiene los Issues deshabilitados. Para consultarlos sin abrir el navegador usa `-R`, que indica el repositorio:

```bash
# Listar los issues abiertos (por defecto muestra 30)
gh issue list -R solareco86-ai/proyecto-integrador

# Ver el detalle de un issue, incluido su cuerpo (reemplaza <número>)
gh issue view <número> -R solareco86-ai/proyecto-integrador
```

`gh issue view` muestra el título, el estado, las etiquetas y la descripción completa. Es la especificación que un agente debe leer antes de tocar código.

---

## 4. Extracción Estructurada con `--json` y `--jq`

Cuando un humano usa la consola lee texto formateado. Cuando un agente usa `gh`, pide JSON con los campos concretos que necesita:

```bash
# Número, título, estado y etiquetas de los issues abiertos
gh issue list -R solareco86-ai/proyecto-integrador --json number,title,state,labels -L 5
```

**Salida estructurada (ejemplo abreviado):**

```json
[
  {
    "labels": [{"name": "enhancement"}],
    "number": 34,
    "state": "OPEN",
    "title": "Sistema de identificación y seguimiento de avance de alumnos en el campus"
  }
]
```

Si solo necesitas un campo, `--jq` filtra la salida sin instalar nada extra:

```bash
# Solo los títulos de los issues abiertos
gh issue list -R solareco86-ai/proyecto-integrador --json title --jq '.[].title'
```

> [!TIP]
> Si no recuerdas qué campos existen, ejecuta `gh issue list -R solareco86-ai/proyecto-integrador --json xx`. `gh` responde con la lista completa de campos disponibles.

---

## Checkpoint de Verificación

Antes de avanzar a la lección 2.6 (Pull Requests y CI):
- [ ] Comprendes la diferencia de rol entre `git` (local) y `gh` (remoto).
- [ ] Verificaste tu autenticación con `gh auth status`.
- [ ] Listaste los issues con `gh issue list` y leíste uno con `gh issue view`.
- [ ] Obtuviste al menos un campo con `--json` y lo filtraste con `--jq`.
