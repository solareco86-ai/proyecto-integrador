# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código, Seguridad y Flujo Atómico en energy-ml

## Lección 2.2: Lectura e Interpretación de `git diff`: El Antídoto a la Aceptación Ciega de IA

En la lección 2.1 fijamos nuestra **línea base en verde** ejecutando `pytest -q` sobre `energy-ml`. En esta lección aprenderemos a utilizar `git diff` para inspeccionar con precisión quirúrgica las modificaciones propuestas por un asistente de Inteligencia Artificial antes de aceptarlas o incluirlas en el control de versiones.

---

## Objetivos de Aprendizaje

1. Comprender por qué la auditoría crítica es la competencia central del desarrollador frente a los modelos de lenguaje (LLMs).
2. Simular un escenario real de refactorización asistida por IA en un módulo de `energy-ml`.
3. Ejecutar e interpretar la anatomía de un `git diff` línea por línea (bloques de contexto, cabeceras `@@`, líneas eliminadas `-` y líneas agregadas `+`).
4. Utilizar `pytest` para verificar cómo una alucinación lógica detectada en el diff rompe los contratos de prueba existentes.

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

Simularemos que un asistente de IA intervino sobre el archivo de preprocesamiento de señales eléctricas `src/domain/services/energy_service.py` (o el servicio de cálculo de potencia de tu proyecto).

Para replicar este escenario exacto en tu terminal, inyectaremos la propuesta que entregó el agente:

```bash
# Simular la propuesta generada por el agente de IA
cat << 'EOF' > src/domain/services/energy_service.py
"""Servicio de dominio para procesamiento y filtrado de señales de potencia."""

def calcular_consumo_activo(potencia_w: float, tiempo_horas: float) -> float:
    """Calcula el consumo en kilovatios-hora (kWh) con filtro de ruido."""
    # MODIFICACIÓN DE LA IA:
    # 1. Agrega redondeo a 3 decimales (mejora deseada)
    # 2. ALUCINACIÓN: Modifica el umbral de detección de 10W a 500W (ignora artefactos residenciales)
    # 3. ALUCINACIÓN: Elimina la validación de potencias negativas
    if potencia_w < 500.0:  # <- Umbral erróneo inyectado por la IA
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
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   src/domain/services/energy_service.py

no changes added to commit (use "git add" to track)
```

Git detecta que el archivo fue modificado en el **Árbol de Trabajo (*Working Tree*)**, pero aún no ha sido enviado al **Área de Preparación (*Staging Area*)**.

---

## 4. Anatomía de `git diff`

Ahora ejecutamos el comando de auditoría fundamental:

```bash
git diff
```

**Salida analítica de Git:**

```diff
diff --git a/src/domain/services/energy_service.py b/src/domain/services/energy_service.py
index 4b825dc..a71e902 100644
--- a/src/domain/services/energy_service.py
+++ b/src/domain/services/energy_service.py
@@ -1,9 +1,11 @@
 """Servicio de dominio para procesamiento y filtrado de señales de potencia."""
 
 def calcular_consumo_activo(potencia_w: float, tiempo_horas: float) -> float:
-    """Calcula el consumo en kilovatios-hora (kWh)."""
-    if potencia_w <= 0:
-        raise ValueError("La potencia no puede ser negativa")
-    if potencia_w < 10.0:
-        return 0.0
-    return (potencia_w * tiempo_horas) / 1000.0
+    """Calcula el consumo en kilovatios-hora (kWh) con filtro de ruido."""
+    if potencia_w < 500.0:
+        return 0.0
+    return round((potencia_w * tiempo_horas) / 1000.0, 3)
```

### Desglose de Cada Elemento del Diff:

1. **`diff --git a/... b/...`**: Compara la versión previa registrada en Git (`a/`) contra la versión modificada en disco (`b/`).
2. **`--- a/...` y `+++ b/...`**:
   * Las líneas que comiencen con `-` (rojas) corresponden al código original que se eliminará.
   * Las líneas que comiencen con `+` (verdes) corresponden al código nuevo que se agregará.
3. **`@@ -1,9 +1,11 @@` (Encabezado de Hunk / Bloque):**
   * `-1,9`: En el archivo original, este bloque comenzaba en la línea 1 y abarcaba 9 líneas.
   * `+1,11`: En el archivo modificado, este bloque comienza en la línea 1 y abarca 11 líneas.
4. **Líneas de contexto (sin signo `+` ni `-`):** Se muestran 3 líneas por encima y por debajo para que el auditor entienda exactamente dónde está ubicado el cambio sin perderse en el archivo.

---

## 5. Corroboración con `pytest`: La Detección de la Regresión

El diff nos reveló dos hechos preocupantes:
- El umbral de corte se elevó arbitrariamente a `500.0W`.
- Desapareció la excepción `ValueError` ante potencias negativas.

Ejecutemos la suite de pruebas para contrastar el cambio contra los contratos de software:

```bash
pytest -q
```

**Salida esperada (falla en rojo):**

```output
.F......                                                         [100%]
=================================== FAILURES ===================================
_________________________ test_calcular_consumo_activo _________________________
    def test_calcular_consumo_activo():
>       assert calcular_consumo_activo(100.0, 1.0) == 0.1
E       assert 0.0 == 0.1

=========================== short test summary info ============================
FAILED tests/test_energy_service.py::test_calcular_consumo_activo - assert 0.0 == 0.1
1 failed, 7 passed in 0.28s
```

La suite que antes estaba 100% en verde ahora acusa una falla categórica: un electrodoméstico de 100W (como una heladera o una computadora) ahora arroja 0 kWh porque la IA "alucinó" un umbral de 500W.

---

## Checkpoint de Verificación

Antes de avanzar a la lección 2.3 (Staging selectivo con `git add -p`):
- [ ] Has ejecutado `git diff` y puedes identificar las líneas eliminadas (`-`) y agregadas (`+`).
- [ ] Entiendes qué significa el encabezado de chunk `@@ -1,9 +1,11 @@`.
- [ ] Has verificado con `pytest -q` que la prueba falla debido al umbral erróneo.
- [ ] Mantienes el archivo modificado en tu terminal sin agregarlo al commit (`working tree dirty`).
