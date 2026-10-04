# Guía de Laboratorio — Lección 3.3: Taller Práctico con OpenCode en energy-ml: Detección de Fallas, Refactor y Tests

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** Asistentes de IA para Estudiantes: OpenCode y Antigravity CLI  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado la Lección 3.2 (Instalación y Configuración de OpenCode).

---

## 1. El Rol de OpenCode en el Flujo Diario de Desarrollo

En la lección anterior configuramos OpenCode sin gastar un centavo. Ahora aplicaremos la herramienta sobre un problema concreto de ingeniería en **`energy-ml`**.

Aprenderás a usar OpenCode no como un "escritor automático de código ciego", sino como un **copiloto técnico subordinado a tus criterios de diseño y validación**.

---

## 2. Preparación del Espacio de Trabajo en `energy-ml`

Navegamos a nuestro repositorio local y activamos el entorno virtual:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Comprobamos el estado del árbol de trabajo con Git:

```bash
git status
```
*(Debe indicar que la rama `main` se encuentra limpia).*

---

## 3. Tarea 1: Detección de Anomalías con OpenCode

En `src/preprocesamiento.py`, los sensores de la planta eléctrica registran mediciones de potencia en vatios (`potencia_w`) y voltaje (`voltaje_v`). Sin embargo, en caso de microcortes de red, el sistema genera registros con valores negativos o nulos.

Iniciamos OpenCode delimitando el contexto:

```bash
opencode --context src/preprocesamiento.py
```

### Prompt Técnico 1: Diagnóstico y Propuesta de Limpieza

En la consola de OpenCode ingresamos:

> *"Examina `src/preprocesamiento.py`. Necesitamos una función `sanitizar_mediciones(df: pd.DataFrame) -> pd.DataFrame` que descarte filas donde `voltaje_v` sea menor a 180.0 o mayor a 260.0 V, y donde `potencia_w` sea estrictamente menor a 0. Debe registrar una advertencia informativa con la cantidad de filas descartadas usando el módulo estándar `logging` y retornar una copia limpia del DataFrame. Incluye Type Hints completos."*

### Análisis del Diff en Consola

OpenCode mostrará la propuesta de cambios como un diff unificado:

```diff
--- a/src/preprocesamiento.py
+++ b/src/preprocesamiento.py
@@ -3,6 +3,7 @@
 import pandas as pd
+import logging
+
+logger = logging.getLogger(__name__)

+def sanitizar_mediciones(df: pd.DataFrame) -> pd.DataFrame:
+    """Filtra lecturas de voltaje fuera de rango y consumos negativos."""
+    filtro_valido = (
+        (df["voltaje_v"] >= 180.0) & 
+        (df["voltaje_v"] <= 260.0) & 
+        (df["potencia_w"] >= 0.0)
+    )
+    descartadas = len(df) - filtro_valido.sum()
+    if descartadas > 0:
+        logger.warning(f"Se descartaron {descartadas} lecturas anómalas de telemetría.")
+    return df[filtro_valido].copy()
```

Aceptamos la modificación pulsando `Y` (o `Enter` según la configuración de tu cliente).

---

## 4. Tarea 2: Generación de Pruebas Unitarias Automatizadas

Un código sugerido por un modelo de IA jamás debe darse por válido sin pruebas automatizadas.

Dentro de OpenCode solicitamos la creación del test correspondiente:

### Prompt Técnico 2: Suite de Pruebas en Pytest

> *"Crea el archivo `tests/test_preprocesamiento.py` con pruebas para `sanitizar_mediciones`. Debe incluir al menos tres casos de prueba: 1) DataFrame con datos 100% válidos, 2) DataFrame con voltajes fuera de rango (150V y 300V), y 3) DataFrame con potencias negativas. Asegúrate de verificar que las dimensiones resultantes coincidan con lo esperado."*

OpenCode creará `tests/test_preprocesamiento.py` con la estructura de Pytest.

---

## 5. Tarea 3: Verificación Local en CPU ($0 Tokens)

Salimos de OpenCode con `/exit` y procedemos a la fase obligatoria de **auditoría y verificación local**:

```bash
pytest tests/test_preprocesamiento.py -v
```

**Salida esperada:**
```text
tests/test_preprocesamiento.py::test_sanitizar_mediciones_validas PASSED
tests/test_preprocesamiento.py::test_sanitizar_voltajes_anomalos PASSED
tests/test_preprocesamiento.py::test_sanitizar_potencia_negativa PASSED
============================== 3 passed in 0.18s ==============================
```

---

## 6. Consolidación del Trabajo en Git

Revisamos el diff exacto generado y el estado del repositorio:

```bash
git status
git diff src/preprocesamiento.py
```

Realizamos nuestro commit atómico:

```bash
git add src/preprocesamiento.py tests/test_preprocesamiento.py
git commit -m "feat(preprocesamiento): incorporar sanitizar_mediciones y tests unitarios asistido por OpenCode"
```

---

## 7. Conclusión

Has completado un ciclo profesional completo:
1. Identificaste un requerimiento técnico en `energy-ml`.
2. Usaste **OpenCode de forma gratuita** sin pagar suscripciones ni ingresar tarjetas.
3. Acotaste el contexto para obtener código determinístico.
4. Generaste pruebas unitarias y las validaste en tu propia CPU.
5. Consolidaste el cambio con un commit atómico en Git.

En la siguiente lección, conoceremos a nuestro segundo asistente: **Antigravity CLI**, aprovechando el beneficio estudiantil de 5 USD/mes para acceder a modelos de frontera.
