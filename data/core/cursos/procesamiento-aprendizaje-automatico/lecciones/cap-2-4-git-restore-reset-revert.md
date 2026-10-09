# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.4: Marcha Atrás y Control de Daños: `git restore`, `git reset` (--soft / --hard) y `git revert`

En la lección 2.3 logramos aislar la alucinación de la IA en el *Working Tree* y preparamos únicamente la optimización legítima en el *Staging Area*. Ahora debemos responder a una pregunta crítica en el desarrollo profesional:

> **¿Qué herramientas ofrece Git cuando un agente de IA genera código defectuoso, cuando agregamos archivos por error o cuando necesitamos deshacer un cambio ya confirmado?**

En esta lección exploraremos en detalle la tríada de comandos de marcha atrás: **`git restore`**, **`git reset`** (en sus variantes `--soft` y `--hard`) y **`git revert`**, comprendiendo sus similitudes, sus diferencias arquitectónicas y sus casos de uso específicos.

---

## Objetivos de Aprendizaje

1. Dominar `git restore` para descartar modificaciones en disco o remover archivos del área de preparación (`--staged`).
2. Comprender el funcionamiento de `git reset` y la diferencia fundamental entre `--soft`, `--mixed` y `--hard`.
3. Entender por qué `git revert` es la única alternativa segura para revertir cambios en ramas compartidas o públicas.
4. Analizar la matriz comparativa de impacto sobre las tres áreas de Git: *Working Tree*, *Staging Area* e *Historial (HEAD)*.
5. Aplicar el descarte definitivo sobre la alucinación en `energy-ml`, confirmar el commit auditado y validar que `pytest` retorne al verde.

---

## 1. El Modelo de Tres Áreas de Git

Para entender con exactitud qué hace cada comando de marcha atrás, recordemos cómo fluye el código en Git:

```
┌─────────────────────────┐       ┌─────────────────────────┐       ┌─────────────────────────┐
│     Working Tree        │       │      Staging Area       │       │    Historial (HEAD)     │
│   (Archivos en Disco)   │ ────► │     (Index / Cache)     │ ────► │  (Base de Datos / Commits)│
└─────────────────────────┘       └─────────────────────────┘       └─────────────────────────┘
```

1. **Working Tree:** El directorio físico donde abres archivos, programas y donde los agentes escriben.
2. **Staging Area (Index):** El borrador intermedio de lo que se incluirá en el próximo commit.
3. **Historial (HEAD):** La cadena de confirmaciones inmutables registradas en la base de datos de `.git/`.

---

## 2. Los Comandos de Marcha Atrás: Catálogo y Comportamiento

### A. `git restore` (La herramienta quirúrgica de archivos)
Introducido en Git moderno para reemplazar los usos confusos de `git checkout`:

* **`git restore <archivo>`:**
  * **Qué hace:** Descarta las modificaciones locales de ese archivo en tu *Working Tree*, restaurando el contenido que Git tiene en el *Staging Area* (o en el último commit).
  * **Cuándo usarlo:** Cuando un agente de IA generó código alucinado en un archivo y quieres borrarlo de un plumazo para volver al estado limpio.
* **`git restore --staged <archivo>`:**
  * **Qué hace:** Saca un archivo del *Staging Area* sin tocar su contenido en el *Working Tree*.
  * **Cuándo usarlo:** Cuando hiciste `git add archivo_con_claves.env` por accidente y quieres sacarlo del commit sin borrar tu archivo de disco.

---

### B. `git reset` (El rebobinador del puntero HEAD)
`git reset` manipula hacia qué commit apunta la rama activa (`HEAD`). Posee tres modalidades clave:

#### 1. `git reset --soft HEAD~1`
* **Qué hace:** Deshace el último commit, pero **conserva todos los cambios en el Staging Area**.
* **Impacto:** Tu historial retrocede un commit, pero tus archivos quedan preparados en el index tal cual estaban.
* **Cuándo usarlo:** Hiciste commit demasiado rápido y olvidaste incluir un archivo, o quieres reescribir el mensaje de commit o unificar dos commits atómicos en uno solo.

#### 2. `git reset --hard HEAD~1` (o a un hash de commit)
* **Qué hace:** Deshace el commit y **destruye de forma permanente e irrevocable** todos los cambios tanto del *Staging Area* como del *Working Tree*.
* **Impacto:** Tu código vuelve exactamente al estado del commit indicado, borrando cualquier modificación no guardada.
* **⚠️ Advertencia Crítica:** `git reset --hard` es un comando destructivo. **Nunca permitas que un agente de IA ejecute `reset --hard` en tu terminal** sin haber verificado con `git status` que no tienes trabajo valioso pendiente.

#### 3. `git reset HEAD~1` (Modo mixto por defecto)
* **Qué hace:** Deshace el último commit y saca los cambios del *Staging Area*, pero **los conserva intactos en el Working Tree**.
* **Cuándo usarlo:** Cuando el commit contenía errores y quieres revisar los archivos tranquilamente en tu editor antes de volver a prepararlos.

---

### C. `git revert <commit>` (La marcha atrás segura en equipo)
A diferencia de `git reset` (que reescribe el historial borrando commits del pasado):

* **`git revert` NO borra el commit problemático:**
* **Qué hace:** Crea un **nuevo commit hacia adelante** que aplica exactamente la operación matemática inversa del commit que se desea anular.
  * Si el commit original agregó la línea `x = 5`, el commit de `revert` la borra.
  * Si el commit original eliminó un archivo, el commit de `revert` lo restaura.
* **Regla de oro de la industria:** En ramas públicas o compartidas con el equipo (`main`, `develop`), **siempre se utiliza `git revert`**. Si usaras `git reset` sobre código ya publicado (*pushed*), romperías el árbol de todos tus compañeros y los pipelines de CI/CD.

---

## 3. Matriz de Similitudes y Diferencias

| Comando | ¿Afecta Working Tree? | ¿Afecta Staging Area? | ¿Modifica Historial (HEAD)? | ¿Seguro en ramas compartidas? | Escenario de uso ante agentes de IA |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **`git restore <archivo>`** | ✅ **Sí** (descarta en disco) | ❌ No | ❌ No | ✅ Seguro (local) | Descartar código alucinado antes de hacer `git add`. |
| **`git restore --staged <archivo>`** | ❌ No (preserva disco) | ✅ **Sí** (remueve del index) | ❌ No | ✅ Seguro (local) | Sacar del commit un archivo agregado por error. |
| **`git reset --soft HEAD~1`** | ❌ No (preserva disco) | ❌ No (mantiene en index) | ✅ **Sí** (mueve puntero) | ⚠️ Solo en ramas locales | Reestructurar o corregir el último commit local. |
| **`git reset --hard HEAD~1`** | ⚠️ **Sí** (destruye en disco) | ⚠️ **Sí** (vacía index) | ✅ **Sí** (mueve puntero) | 🚫 **NUNCA** en compartidas | Abortar un experimento fallido por completo. |
| **`git revert <hash>`** | ✅ **Sí** (aplica parche inverso) | ✅ **Sí** (prepara commit) | ✅ **Sí** (crea nuevo commit) | ✅ **100% Seguro** | Deshacer un bug ya subido a GitHub sin romper a otros. |

---

## 4. Árbol de Decisiones de Recuperación

```
¿Dónde se encuentra el código problemático?
  │
  ├── 1. Solo en disco (Working Tree, antes de git add)
  │      └── Solución: git restore <archivo>
  │
  ├── 2. Preparado para el commit (Staging Area, tras git add)
  │      ├── Si querés sacarlo del commit pero conservar tus cambios:
  │      │     └── Solución: git restore --staged <archivo>
  │      └── Si querés borrarlo de disco y de staging:
  │            └── Solución: git restore --staged <archivo> && git restore <archivo>
  │
  ├── 3. Confirmado en un commit local (Aún NO enviado con git push)
  │      ├── Si querés reformular el commit conservando el código:
  │      │     └── Solución: git reset --soft HEAD~1
  │      └── Si querés descartar el commit y todo su código:
  │            └── Solución: git reset --hard HEAD~1 (¡con cautela!)
  │
  └── 4. Publicado en GitHub / servidor remoto (Ya hiciste git push)
         └── Solución obligatoria: git revert <commit>
```

---

## 5. Práctica de Cierre en `energy-ml`

Regresemos al estado en que dejamos `energy-ml` en la lección 2.3:
* La mejora legítima (el redondeo) está en el *Staging Area*.
* La alucinación (el umbral de 500W) quedó pendiente en el *Working Tree*.

### Paso 1: Descartar la alucinación con `git restore`
Ejecuta el descarte definitivo de las líneas que no pasaron la auditoría:

```bash
git restore src/domain/services/energy_service.py
```

### Paso 2: Verificar el árbol con `git status`
```bash
git status
```

**Salida en consola:**

```output
En la rama ejercicio/diff-energia
Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
	modified:   src/domain/services/energy_service.py
```

¡Las líneas erróneas desaparecieron del disco y solo permanece el cambio auditado en el Staging Area!

---

### Paso 3: Validación con `pytest`: Retorno al Verde
Comprobemos que la suite de pruebas ahora pasa al 100%:

```bash
pytest -q
```

**Salida:**

```output
........                                                         [100%]
8 passed in 0.41s
```

La suite volvió al verde: la función ahora calcula con la precisión redondeada sin omitir artefactos residenciales.

---

### Paso 4: Confirmación Atómica y Registro en el Historial
Registra el commit auditado en tu rama de ejercicio (`ejercicio/diff-energia`, de la lección 2.2) siguiendo la convención de commits atómicos:

```bash
git commit -m "feat(domain): agregar redondeo a 3 decimales en calculo de consumo activo"
```

Comprueba el nuevo commit en el historial:

```bash
git log -n 1 --stat
```

**Salida esperada:**

```output
[ejercicio/diff-energia 9f3e1a0] feat(domain): agregar redondeo a 3 decimales en calculo de consumo activo
 1 file changed, 2 insertions(+), 2 deletions(-)
```

---

## Checkpoint de Verificación del Capítulo 2

Has completado el ciclo completo de auditoría y gobierno de código:
- [ ] Conoces la diferencia entre `git restore`, `git reset` (--soft / --hard) y `git revert`.
- [ ] Entiendes por qué nunca se debe utilizar `git reset --hard` en ramas compartidas.
- [ ] Has descartado exitosamente la alucinación del umbral con `git restore`.
- [ ] Tu suite de pruebas `pytest` se encuentra 100% en verde.
- [ ] Tu árbol de trabajo en `ejercicio/diff-energia` está limpio (`working tree clean`) con tu commit atómico registrado.
