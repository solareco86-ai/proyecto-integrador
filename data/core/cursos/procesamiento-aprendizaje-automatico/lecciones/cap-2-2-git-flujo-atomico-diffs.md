# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.2: Lectura e Interpretación de `git diff`: El Antídoto a la Aceptación Ciega de IA

En la lección 2.1 fijamos nuestra **línea base en verde** ejecutando `pytest -q` sobre `energy-ml`. En esta lección aprenderemos a utilizar `git diff` para inspeccionar con precisión quirúrgica las modificaciones propuestas por un asistente de Inteligencia Artificial antes de aceptarlas o incluirlas en el control de versiones.

---

## Objetivos de Aprendizaje

1. Comprender por qué la auditoría crítica es la competencia central del desarrollador frente a los modelos de lenguaje (LLMs).
2. Simular un escenario real de refactorización asistida por IA en un módulo de `energy-ml`.
3. Ejecutar e interpretar la anatomía de un `git diff` línea por línea (bloques de contexto, cabeceras `@@`, líneas eliminadas `-` y líneas agregadas `+`).
4. Utilizar `pytest` para verificar cómo un cambio incorrecto detectado en el diff rompe los contratos de prueba existentes.
5. Clasificar cada cambio propuesto por la IA según las tres categorías de riesgo, justificando la decisión.

---

## 1. El Riesgo de la Aceptación Ciega

Cuando le pedimos a un agente (Cursor, Copilot, Aider o ChatGPT) que *"optimice"* una función o *"agregue un filtro"*, el modelo suele generar código que a primera vista parece elegante, pero que frecuentemente introduce tres tipos de errores silenciosos:

1. **Alucinaciones Matemáticas/Lógicas:** Modificar umbrales numéricos, constantes de calibración o condiciones de corte.
2. **Efectos Colaterales Ocultos:** Eliminar validaciones de casos borde (ej. valores negativos o divisiones por cero).
3. **Refactorizaciones Invasivas:** Reformatear variables o alterar la arquitectura del archivo sin haberlo solicitado.

> [!IMPORTANT]
> **Principio de Auditoría Activa:** Ningún cambio generado por una IA se confirma a ciegas. La consola y el comando `git diff` son tu microscopio para certificar cada caracter antes de hacer commit.

---

## 2. Escenario Práctico: Modificación Asistida en `energy-ml`

Asegúrate de estar en la raíz del proyecto clonado:

```bash
cd ~/Desktop/aprendizaje-automatico/energy-ml  # O tu ruta equivalente
```

Simularemos que un asistente de IA intervino sobre el archivo de cálculo de potencia `src/domain/services/energy_service.py`. Para que el `git diff` tenga una referencia contra la cual compararse, primero creamos la **versión base** y la confirmamos en una rama de ejercicio, sin tocar `main`.

### 2.1 Crear la versión base y confirmarla

```bash
git checkout -b ejercicio/diff-energia
mkdir -p src/domain/services tests
touch src/domain/services/__init__.py tests/__init__.py

cat << 'EOF' > src/domain/services/energy_service.py
"""Servicio de dominio para procesamiento y filtrado de señales de potencia."""

def calcular_consumo_activo(potencia_w: float, tiempo_horas: float) -> float:
    """Calcula el consumo en kilovatios-hora (kWh)."""
    if potencia_w <= 0:
        raise ValueError("La potencia no puede ser negativa")
    if potencia_w < 10.0:
        return 0.0
    return (potencia_w * tiempo_horas) / 1000.0
EOF

cat << 'EOF' > tests/test_energy_service.py
import pytest

from src.domain.services.energy_service import calcular_consumo_activo


def test_calcular_consumo_activo():
    assert calcular_consumo_activo(100.0, 1.0) == 0.1


def test_consumo_de_potencia_alta():
    assert calcular_consumo_activo(1000.0, 1.0) == 1.0


def test_potencia_negativa_lanza_error():
    with pytest.raises(ValueError):
        calcular_consumo_activo(-5.0, 1.0)
EOF

git add src/domain/services tests
git commit -m "chore: versión base del servicio de energía"
```

### 2.2 Inyectar la propuesta del agente

Ahora simulamos la propuesta que entregó el agente. Lee el código antes de continuar: el objetivo de la lección es que lo audites, no que lo confíes.

```bash
cat << 'EOF' > src/domain/services/energy_service.py
"""Servicio de dominio para procesamiento y filtrado de señales de potencia."""

def calcular_consumo_activo(potencia_w: float, tiempo_horas: float) -> float:
    """Calcula el consumo en kilovatios-hora (kWh) con filtro de ruido."""
    if potencia_w < 500.0:
        return 0.0
    return round((potencia_w * tiempo_horas) / 1000.0, 3)
EOF
```

---

## 3. Inspección del Estado con `git status`

Comprobemos cómo reacciona Git ante la intervención:

```bash
git status
```

**Salida en consola:**

```output
En la rama ejercicio/diff-energia
Cambios no rastreados para el commit:
  (usa "git add <archivo>..." para actualizar lo que será confirmado)
  (usa "git restore <archivo>..." para descartar los cambios en el directorio de trabajo)
	modificados:     src/domain/services/energy_service.py

sin cambios agregados al commit (usa "git add" y/o "git commit -a")
```

Git detecta que el archivo fue modificado en el **Árbol de Trabajo (*Working Tree*)**, pero aún no ha sido enviado al **Área de Preparación (*Staging Area*)**.

---

## 4. Anatomía de `git diff`

Antes de ejecutar el comando, haz una **predicción por escrito** (en un cuaderno o en un comentario de tu terminal):

- ¿Qué líneas esperas ver en rojo (`-`) y cuáles en verde (`+`)?
- ¿Alguna validación de la versión original podría desaparecer? ¿Cuál?
- ¿Hay algún cambio que no tenga relación con lo que se pidió?

Recién después ejecutamos el comando de auditoría fundamental:

```bash
git diff
```

**Salida analítica de Git** (los hashes `index` pueden variar en tu equipo):

```diff
diff --git a/src/domain/services/energy_service.py b/src/domain/services/energy_service.py
index 53e9896..57408da 100644
--- a/src/domain/services/energy_service.py
+++ b/src/domain/services/energy_service.py
@@ -1,9 +1,7 @@
 """Servicio de dominio para procesamiento y filtrado de señales de potencia."""
 
 def calcular_consumo_activo(potencia_w: float, tiempo_horas: float) -> float:
-    """Calcula el consumo en kilovatios-hora (kWh)."""
-    if potencia_w <= 0:
-        raise ValueError("La potencia no puede ser negativa")
-    if potencia_w < 10.0:
+    """Calcula el consumo en kilovatios-hora (kWh) con filtro de ruido."""
+    if potencia_w < 500.0:
         return 0.0
-    return (potencia_w * tiempo_horas) / 1000.0
+    return round((potencia_w * tiempo_horas) / 1000.0, 3)
```

### Desglose de Cada Elemento del Diff:

1. **`diff --git a/... b/...`**: Compara la versión previa registrada en Git (`a/`) contra la versión modificada en disco (`b/`).
2. **`--- a/...` y `+++ b/...`**:
   * Las líneas que comiencen con `-` (rojas) corresponden al código original que se eliminará.
   * Las líneas que comiencen con `+` (verdes) corresponden al código nuevo que se agregará.
3. **`@@ -1,9 +1,7 @@` (Encabezado de Hunk / Bloque):**
   * `-1,9`: En el archivo original, este bloque comenzaba en la línea 1 y abarcaba 9 líneas.
   * `+1,7`: En el archivo modificado, este bloque comienza en la línea 1 y abarca 7 líneas.
4. **Líneas de contexto (sin signo `+` ni `-`):** Se muestran para que el auditor entienda exactamente dónde está ubicado el cambio sin perderse en el archivo.

Compara tu predicción con el resultado. Si alguna línea te sorprendió, anota por qué: esa diferencia es lo que más vas a aprender en esta lección.

---

## 5. Corroboración con `pytest`: La Detección de la Regresión

El diff nos muestra dos cambios que merecen atención:
- El umbral de corte se elevó de `10.0` a `500.0`.
- Desapareció la validación de potencias negativas.

Ejecutemos la suite de pruebas para contrastar el cambio contra los contratos de software:

```bash
pytest -q
```

**Salida esperada (falla en rojo):**

```output
F.F                                                                      [100%]
=================================== FAILURES ===================================
_________________________ test_calcular_consumo_activo _________________________
>       assert calcular_consumo_activo(100.0, 1.0) == 0.1
E       assert 0.0 == 0.1

______________________ test_potencia_negativa_lanza_error ______________________
>       with pytest.raises(ValueError):
E       Failed: DID NOT RAISE ValueError

=========================== short test summary info ============================
FAILED tests/test_energy_service.py::test_calcular_consumo_activo - assert 0.0 == 0.1
FAILED tests/test_energy_service.py::test_potencia_negativa_lanza_error - Failed: DID NOT RAISE
2 failed, 1 passed
```

Cada falla corresponde a un cambio del diff:
- `test_calcular_consumo_activo`: un electrodoméstico de 100 W ahora arroja 0 kWh porque el umbral subió a 500 W.
- `test_potencia_negativa_lanza_error`: la función acepta potencias negativas sin error porque se eliminó la validación.

La prueba de 1000 W sigue pasando, porque el cambio no afecta a las potencias altas. Un error que solo aparece en algunos valores es justamente el que la revisión visual suele dejar pasar.

---

## 6. Clasificación del Cambio

Como última tarea, completa esta tabla con cada modificación del diff. Para cada una, indica la categoría de la sección 1 y justifica con una línea:

| Cambio en el diff | Categoría (1, 2 o 3) | Justificación |
|---|---|---|
| Umbral de 10.0 a 500.0 | | |
| Eliminación de `raise ValueError` | | |
| Redondeo a 3 decimales | | |
| Cambio en la docstring | | |

Compara tu tabla con la de un compañero antes de seguir: si no coinciden en alguna fila, discutan por qué.

---

## Checkpoint de Verificación

Antes de avanzar a la lección 2.3 (Staging selectivo con `git add -p`):
- [ ] Hiciste la predicción antes de ejecutar `git diff` y la comparaste con el resultado.
- [ ] Puedes identificar las líneas eliminadas (`-`) y agregadas (`+`) y explicar el encabezado `@@ -1,9 +1,7 @@`.
- [ ] Completaste la tabla de clasificación de la sección 6.
- [ ] Verificaste con `pytest -q` que dos pruebas fallan, y puedes asociar cada falla con un cambio del diff.
- [ ] Mantén el archivo modificado sin agregarlo al commit (`working tree dirty`).
