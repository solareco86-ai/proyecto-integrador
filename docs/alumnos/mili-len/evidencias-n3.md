# Evidencias N3 – Milagros Lencina

**Alumna:** Lencina Milagros (`@mili-len`).  
**Entrega:** N3 – Tests de las contribuciones propias.  
**Fecha de corte:** 22/11/2026.  
**Base de comparación:** `develop` en `5e8acd5`.

---

## 1. Consigna y criterio

> Sumar tests más allá del de `llms.txt`. N3 mide los tests de tu trabajo. En repos compartidos solo cuenta lo que commiteaste. Por cada cambio tuyo, escribí al menos un test que falle sin tu cambio y pase con él.

**Cómo lo verifiqué:** cada test se ejecutó dos veces, en copias descartables del repositorio, sin modificar ninguna rama:

- **antes:** contra el código anterior al cambio, con la versión final del test;
- **después:** contra el código que incluye el cambio.

Un test **cumple** si falla antes y pasa después. Un test que pasa en ambos casos se informa como control de regresión, no como prueba del cambio.

---

## 2. Matriz de pruebas

| Contribución | Cambio | Test | Commit del test | Dónde está | Antes | Después | N3 |
|---|---|---|---|---|---|---|---|
| `5d54353` | Contenido GEO de `llms.txt` y `llms-full.txt`, y sitemap de `robots.txt` | `tests/test_llms_txt.py`: `test_llms_txt_endpoint_returns_200`, `test_llms_full_txt_endpoint_returns_200` y `test_robots_txt_allows_ai_bots` | `5d54353` | **`develop`** | 3 fallan (en `2beb760`) | 3 pasan | Cumple |
| `5d54353` | Lista de negativas de Google Ads (`data/ads/`) | `tests/test_negative_keywords.py`: 5 tests de integridad | `f77e95e` | [PR #117](https://github.com/solareco86-ai/proyecto-integrador/pull/117): publicado, **pendiente de integración en `develop`** | 4 fallan y 1 pasa (con la lista heredada de `2beb760`) | 5 pasan | Cumple (el test llegó después del cambio) |
| `265e72b` | Concordancias de negativas (antecedente "T-32") | `test_negative_keywords_do_not_exclude_generic_price_searches` | `265e72b` | PR #117: pendiente de integración | 1 falla (con la lista de `develop`) | 1 pasa | Cumple |
| `8edd14f` + `f1991a7` | Guía 1.3 de PDI con imágenes de antes y después | `test_leccion_transformaciones_renderiza_imagenes_y_ejercicio` y `test_imagenes_de_la_leccion_se_sirven` | `db1dfe9`, actualizado en `f1991a7` | [PR #114](https://github.com/solareco86-ai/proyecto-integrador/pull/114): publicado, **pendiente de integración en `develop`** | 2 fallan (en `develop`) | 2 pasan | Cumple |
| `f1991a7` | Imágenes de `cv2.rotate` y de traslación | El mismo archivo | `f1991a7` | PR #114: pendiente de integración | 2 fallan y 1 pasa (en `b197eaf`) | 3 pasan | Cumple |
| `db1dfe9` | Control de enlaces a `static/` en todas las lecciones | `test_lecciones_no_referencian_archivos_estaticos_inexistentes` | `db1dfe9` | PR #114: pendiente de integración | Pasa | Pasa | Control de regresión |
| `b197eaf` | Precisión del código de la lección (rectángulo, `math.ceil`, nombres) | Ninguno automatizado | – | PR #114: pendiente de integración | 3 pasan | 3 pasan | **Sin test automatizado.** Verificación manual en la sección 4. |
| `5d54353` | Catálogo JSON-LD de `head.html` | Lo cubren los tests del PR #120 | `90446be` y `660b312` | [PR #120](https://github.com/solareco86-ai/proyecto-integrador/pull/120): publicado, **pendiente de integración en `develop`** | Ver sección 3 | Ver sección 3 | Cumple (con un cambio nuevo) |

En el caso de `f77e95e` se usó el código de `develop` cambiando solo los archivos de negativas por los de `2beb760`, para aislar el cambio de datos que valida el test. Fallan `test_negative_keywords_csv_format`, `test_negative_keywords_have_no_duplicates`, `test_negative_keywords_have_no_inherited_brand` y `test_negative_keywords_do_not_block_official_careers`. Pasa `test_negative_keywords_txt_and_csv_are_in_sync`.

**Resumen:** de los cambios con comportamiento verificable, todos tienen un test que falla antes y pasa después, salvo `b197eaf`.

> **Estado de integración (22/11/2026):** solo los tests de `5d54353` están en `develop`. Los tests de los PRs **#114, #117 y #120 están commiteados y publicados en GitHub, pero todavía no están integrados en `develop`**: los tres PRs siguen abiertos, a la espera de revisión.

---

## 3. JSON-LD del catálogo de carreras (issue #119 y PR #120)

**Cambio:** el `hasOfferCatalog` del JSON-LD global (`templates/partials/head.html`) tenía las 6 tecnicaturas escritas a mano. Ahora se genera desde `carreras.yaml`, mediante un presenter y `| tojson`.

- Issue: [#119](https://github.com/solareco86-ai/proyecto-integrador/issues/119)
- PR: [#120](https://github.com/solareco86-ai/proyecto-integrador/pull/120), rama `alumno/mili-len/jsonld-catalogo-carreras`
- Commits: `90446be` (presenter y tests unitarios) y `660b312` (plantilla y tests de integración)

Resultado de `tests/test_json_ld_catalogo.py` (versión de `660b312`) contra cada versión:

| Test | `develop` (`5e8acd5`) | Commit `90446be` (plantilla a mano) | Commit `660b312` |
|---|---|---|---|
| `test_presenter_arma_un_offer_con_su_course_por_carrera_en_orden` | No ejecuta: el presenter no existe | Pasa | Pasa |
| `test_presenter_con_catalogo_vacio_no_inventa_carreras` | No ejecuta | Pasa | Pasa |
| `test_json_ld_del_home_refleja_el_catalogo_inyectado` | No ejecuta | **Falla**: publica las 6 carreras fijas | Pasa |
| `test_json_ld_del_home_publica_las_descripciones_de_carreras_yaml` | No ejecuta | **Falla** | Pasa |
| `test_json_ld_del_catalogo_escapa_comillas_ampersand_y_etiquetas` | No ejecuta | **Falla** | Pasa |

**Validaciones de la rama:**
- **Suite completa:** 1072 tests aprobados y cobertura del 88,48 %. Falla solo `test_seo.py::test_ready_endpoint`, que necesita MySQL y también falla en `develop`.
- **Pyright:** sin errores nuevos.
- **Tests existentes:** `test_oferta_carreras_consistente.py` (de otros compañeros) sigue pasando.

El detalle completo está en la descripción del PR #120.

---

## 4. Verificación manual de la guía de OpenCV (`b197eaf`)

**Por qué es manual:** OpenCV no es dependencia del proyecto (`requirements.txt`), así que los ejemplos de la lección no pueden correr en la suite automatizada. Esta sección registra una verificación hecha a mano. **No es un test automatizado.**

**Fecha:** 22/11/2026, 17:49 (UTC−3).  
**Material:** la lección `cap-1-3-transformaciones-geometricas-operaciones.md` en la versión de `f1991a7`, que incluye `b197eaf`.  
**Imagen:** `coffee.png` de scikit-image (CC0). Su SHA-256 (`cc02f8ca188b167c…`) coincide con el de `static/media/cursos/pdi/cafe.png` commiteado.

| Comprobación | OpenCV 4.10.0 (NumPy 2.2.6) | OpenCV 5.1.0 (NumPy 2.5.5) |
|---|---|---|
| Bloques de Python de la lección | 9 de 9 terminan sin errores | 9 de 9 terminan sin errores |
| Tamaños impresos por los bloques | Coinciden con los comentarios del texto | Coinciden |

**Lienzo de "rotar sin perder las esquinas"** (rotación de 30°): posición de las 4 esquinas de la imagen rotada, calculada con la matriz de OpenCV.

| Cálculo del lienzo | Tamaño | Rango en x | Rango en y | Resultado |
|---|---|---|---|---|
| `int()` (antes de `b197eaf`) | 719 × 646 | −0,31 a 719,31 | −0,21 a 646,21 | Las puntas quedan **afuera** |
| `math.ceil` (con `b197eaf`) | 720 × 647 | 0,19 a 719,81 | 0,29 a 646,71 | Todo queda **adentro** |

**Comparación entre versiones** (hecha el mismo día, durante la revisión del PR #114): las imágenes que generan los bloques son idénticas píxel a píxel en OpenCV 4.10 y 5.1, salvo las dos rotaciones, que difieren en 5 niveles de intensidad como máximo por el redondeo de la interpolación.

**Cómo reproducirlo:**

```bash
# En un entorno aparte: pip install "opencv-python-headless==4.10.0.84"
mkdir prueba && cp static/media/cursos/pdi/cafe.png prueba/
python - data/core/cursos/procesamiento-imagenes-python-opencv/lecciones/cap-1-3-transformaciones-geometricas-operaciones.md prueba <<'EOF'
import re, subprocess, sys
bloques = re.findall(r"```python\n(.*?)```", open(sys.argv[1], encoding="utf-8").read(), re.S)
for i, codigo in enumerate(bloques, 1):
    r = subprocess.run([sys.executable, "-c", codigo], cwd=sys.argv[2], capture_output=True, text=True)
    print(f"[{i}] rc={r.returncode} {r.stdout.strip()}")
EOF
```

---

## 5. Limitaciones (lo que no se verificó)

- **`b197eaf` no tiene un test automatizado** que falle sin el cambio. Solo tiene la verificación manual de la sección 4.
- **La corrección del rectángulo del recorte** (`x2 - 1`, `y2 - 1`) se comprobó **solo visualmente**, mirando la imagen generada. No hay una medición numérica.
- **`test_seo.py::test_ready_endpoint` falla en el entorno local** porque necesita MySQL. No tiene relación con estos cambios: también falla en `develop`.
- **Integración pendiente:** salvo los de `5d54353`, los tests están en los PRs #114, #117 y #120, publicados pero **todavía no integrados en `develop`**.
- **Mejora pendiente, fuera de N3:** el JSON-LD de `carrera_detail.html` interpola texto sin escaparlo para JSON. Está documentado como mejora y no se corrigió.

---

## 6. Enlaces

| Contribución | Enlace |
|---|---|
| Guía 1.3 de PDI | [PR #114](https://github.com/solareco86-ai/proyecto-integrador/pull/114) · [Issue #101](https://github.com/solareco86-ai/proyecto-integrador/issues/101) |
| Negativas de Google Ads (división de `5d54353`) | [PR #117](https://github.com/solareco86-ai/proyecto-integrador/pull/117) · [Issue #116](https://github.com/solareco86-ai/proyecto-integrador/issues/116) |
| JSON-LD del catálogo | [PR #120](https://github.com/solareco86-ai/proyecto-integrador/pull/120) · [Issue #119](https://github.com/solareco86-ai/proyecto-integrador/issues/119) |
| Commit original con tests en `develop` | `5d54353` (rama `alumno/mili-len/seo-geo-sem`) |

**Uso de IA:** usé un asistente de IA en estas tareas. Está declarado con el trailer `Co-Authored-By` en cada commit.
