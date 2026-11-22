# División del commit 5d54353 en commits atómicos (N2)

**Alumna:** Lencina Milagros (`@mili-len`).  
**Entrega:** N2 – Commits atómicos.  
**Fecha:** 22/11/2026.  
**Base de esta contribución:** `develop` en `5e8acd5` (verificado contra GitHub el 22/11/2026).

Este documento distingue dos conjuntos de commits:

- **Commits históricos (sección 2):** la división del commit original, hecha en una rama de trabajo local (`alumno/mili-len/seo-atomico-n2`), que **no forma parte de este PR**.
- **Commits nuevos (sección 4):** los que se crean en la rama `alumno/mili-len/seo-sem-pendientes` y **sí forman parte de este PR** hacia `develop`.

---

## 1. El commit original

| Dato | Valor |
|---|---|
| Commit | `5d54353` – `feat(seo): optimizar schema educacional, llms.txt y palabras clave sem` |
| Fecha | 09/09/2026 |
| Rama | `alumno/mili-len/seo-geo-sem` |
| Integración | Merge directo a `develop` en `fb7bb10` (11/09/2026), sin PR |
| Tamaño | 7 archivos, +462 / −451 líneas |

**Por qué no era atómico:** un solo commit mezclaba cuatro temas independientes, cada uno con su propio motivo y su propio riesgo:

| Tema | Archivos |
|---|---|
| SEO técnico | `static/robots.txt` |
| GEO (sistemas de IA) | `static/llms.txt`, `static/llms-full.txt`, `tests/test_llms_txt.py` |
| SEO (datos estructurados) | `templates/partials/head.html` |
| SEM (Google Ads) | `data/ads/negative_keywords_clean.txt`, `data/ads/negative_keywords_editor.csv` |

Con esa mezcla no se podía revisar, revertir ni probar un tema sin arrastrar los otros. Como el commit ya está integrado en `develop`, no se reescribió: la división se hizo en una rama aparte.

## 2. La división histórica (rama local, no incluida en este PR)

Rama `alumno/mili-len/seo-atomico-n2`, creada desde `2beb760` (el padre de `5d54353`). No está publicada en GitHub.

| # | Commit | Tema | Qué hace |
|---|---|---|---|
| 1 | `38ab7cf` | SEO | Apunta el sitemap de `robots.txt` a `isftn199.com.ar`. |
| 2 | `0fbc610` | GEO | Reescribe `llms.txt` y `llms-full.txt` para el ISFT N° 199. |
| 3 | `d38b825` | SEO | Declara el JSON-LD institucional como `EducationalOrganization`. |
| 4 | `0e374ec` | SEM | Reemplaza la lista de negativas heredada de DataMaq y agrega `tests/test_negative_keywords.py`. |
| 5 | `f245458` | SEM | Aplica la política de concordancias de negativas (registrada como "T-32" en el backlog de esa rama). |
| 6 | `c463654` | Corrección | Corrige el tipado del test del commit 3: con el commit 3 solo, Pyright marcaba 2 errores. |
| 7 | `d5c61c8` | Corrección | Restaura el código postal `B1618`, que la reescritura del commit 2 había omitido. |

Cada uno de los commits 1 a 5 trata un solo tema, incluye su prueba y pasa sus pruebas por sí solo: 3, 6, 9, 14 y 15 pruebas, respectivamente. Los commits 6 y 7 son correcciones que se agregaron después, sin reescribir la historia.

## 3. Qué se hizo con cada commit histórico frente al `develop` actual

Cada commit se simuló con cherry-pick sobre `develop` (`5e8acd5`):

| Commit histórico | Resultado sobre `develop` | Decisión | Motivo |
|---|---|---|---|
| `38ab7cf` robots.txt | Conflicto; cambio vacío | **Excluido** | `robots.txt` ya es idéntico en `develop`. |
| `0fbc610` llms | Conflicto | **Excluido: obsoleto** | `develop` tiene una versión posterior. La versión histórica vuelve a incluir "Mecatrónica", retirada en `52203b1`, y `tests/test_llms_txt.py` de `develop` exige que no aparezca. Incorporarla sería una regresión. |
| `d38b825` + `c463654` JSON-LD | Conflicto | **Excluido de este PR** | `head.html` cambió después en `develop`. El problema de fondo sigue existiendo: `knowsAbout` y el catálogo de cursos están escritos a mano en la plantilla, y `AGENTS.md` pide que los datos vivan en `data/`. La solución correcta es generarlos desde `carreras.yaml`. Quitarlos sin reemplazo empobrecería el SEO, así que queda para una contribución propia. |
| `d5c61c8` código postal | Conflicto; redundante | **Excluido** | `develop` ya tiene `B1618` en `llms-full.txt`. |
| `0e374ec` negativas | Aplica; solo agrega el test | **Se recupera solo el test** | Los dos archivos de negativas de `develop` son idénticos a los de este commit (el cambio de datos ya entró con `5d54353`), pero el test no existe en `develop`. |
| `f245458` concordancias | Aplica sin conflictos | **Se recupera, adaptado** | El cambio no está en `develop`. |

## 4. Commits nuevos de este PR

Rama `alumno/mili-len/seo-sem-pendientes`, creada desde `develop` (`5e8acd5`):

| Commit nuevo | Origen | Archivos | Qué hace |
|---|---|---|---|
| `f77e95e` `test(sem): validar palabras negativas de campañas` | `0e374ec` (solo el test) | `tests/test_negative_keywords.py` | 5 pruebas sobre los datos reales: sincronía entre el `.txt` y el `.csv`, formato de Google Ads Editor, sin duplicados, sin términos heredados y sin bloquear búsquedas de las carreras de `carreras.yaml`. |
| `265e72b` `feat(sem): aplicar correcciones de concordancia T-32` | `f245458`, adaptado | Los dos archivos de negativas, el test y `docs/CHANGELOG.md` | Lista de 108 a 102 términos (49 eliminados, 43 agregados, 1 concordancia modificada) y prueba de que 8 búsquedas genéricas de precio no se bloquean. |
| Este documento `docs(n2)` | – | `docs/alumnos/mili-len/division-commit-5d54353.md` | Explica la división y las decisiones. |

**Adaptaciones de `f245458` a `develop`:**
- Un caso de prueba usaba "cuanto cuesta la carrera de mecatronica"; ahora usa Turismo, porque Mecatrónica fue retirada.
- Se quitaron las referencias a "la estrategia SEO/SEM/GEO (§2.1.1)", un documento que no existe en `develop`. La política se explica en el propio texto.
- **No se agrega T-32 a `docs/todo.md`.** En `develop` las tareas llegan hasta T-26, y "T-32" era el identificador del backlog de la rama original. Solo se menciona como antecedente histórico.

## 5. Verificación

Resultados del 22/11/2026, en un clon independiente con `develop` verificado contra GitHub:

| Verificación | Resultado |
|---|---|
| Hashes de origen | `0e374ecd6f12…` y `f245458d6c98…` coinciden con los commits históricos. |
| Datos sin duplicar | Los archivos de negativas de `develop` son idénticos a los de `0e374ec`. Los de este PR son idénticos byte por byte a los de `f245458`. |
| Cifras de la lista | Recalculadas sobre los archivos: 108 → 102, con 49 eliminados, 43 agregados y 1 concordancia modificada (`matricula de pago`, de amplia a frase). |
| `tests/test_negative_keywords.py` | 6 aprobados. |
| Prueba de precio contra la lista anterior | Falla con la lista de `develop` y pasa con la corregida: demuestra el efecto del cambio. |
| Mutaciones del test | Si se agrega un término heredado, se desincronizan los archivos o se agrega una negativa que bloquea "Ciencia de Datos", el test falla. |
| Suite completa (`pytest --cov=src --cov-fail-under=85`) | 1073 aprobadas, cobertura del 88,47 %. Falla solo `test_seo.py::test_ready_endpoint`, que necesita MySQL; también falla en `develop`. |
| `validate_content.py`, `validate_templates.py`, `verify_architecture.py`, `ruff check` | Sin errores. |
| `pyright src/ scripts/ tests/` | 68 errores, **la misma cifra que `develop` sin estos cambios**. El archivo de test tiene 0 errores. |
| Alcance | El diff contra `develop` no toca `robots.txt`, `llms*.txt`, `head.html` ni `docs/todo.md`. |

**Cómo reproducirlo:**

```bash
git switch alumno/mili-len/seo-sem-pendientes
pytest tests/test_negative_keywords.py -q
git diff --stat develop...HEAD
```
