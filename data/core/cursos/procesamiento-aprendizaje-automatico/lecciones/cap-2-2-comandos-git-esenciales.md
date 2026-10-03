# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código y Flujo Atómico de Cambios

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 3 horas (de 20 hs totales)

---

## Objetivos de Aprendizaje

Al finalizar este laboratorio, el estudiante será capaz de:
1. Simular la respuesta de un agente de IA que combina lógica útil con código contaminado o inseguro (API keys expuestas y logs no deseados).
2. Auditar el estado del repositorio mediante `git status` y `git diff`.
3. Aplicar el staging interactivo por fragmentos (`git add -p`) discriminando código válido de sugerencias inseguras o alucinadas.
4. Comparar el área de staging (`git diff --staged`) con los cambios que permanecen en el working tree (`git diff`).

---

## 1. Simulación: La Propuesta Contaminada del Agente de IA

Imagina que solicitaste a un asistente de código (como Aider, OpenCode o ChatGPT):
> *"Por favor agrega a `calculadora_datos.py` una función para calcular la desviación estándar muestral y configurar logs."*

El agente genera una respuesta que parece resolver el problema, pero introduce un error de seguridad grave: una clave de API falsa *hardcodeada* y un log invasivo.

Sobrescribe `calculadora_datos.py` para simular exactamente lo que el agente devolvió:

```bash
cat << 'EOF' > calculadora_datos.py
import math

# CLAVE DE API DE PRUEBA INYECTADA POR EL AGENTE (¡PELIGRO CRÍTICO!)
API_KEY_TEMP = "sk-proj-9999888877776666"

def calcular_promedio(numeros):
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)

def calcular_varianza(numeros):
    if not numeros or len(numeros) < 2:
        return 0.0
    media = calcular_promedio(numeros)
    return sum((x - media) ** 2 for x in numeros) / (len(numeros) - 1)

def calcular_desviacion_estandar(numeros):
    if not numeros or len(numeros) < 2:
        return 0.0
    return math.sqrt(calcular_varianza(numeros))

if __name__ == "__main__":
    datos = [10.5, 20.0, 30.2, 40.8]
    print(f"[LOG INVASIVO] Conectando con API Key: {API_KEY_TEMP}")
    print(f"Datos: {datos}")
    print(f"Promedio: {calcular_promedio(datos):.2f}")
    print(f"Varianza: {calcular_varianza(datos):.2f}")
    print(f"Desviación Estándar: {calcular_desviacion_estandar(datos):.2f}")
EOF
```

---

## 2. Diagnóstico de Estado y Detección de Fugas con `git status`

Antes de realizar cualquier acción, revisa el estado del repositorio:

```bash
git status
```

Verás que `calculadora_datos.py` figura como modificado. Ahora ejecuta `git diff` para someter la propuesta a escrutinio:

```bash
git diff
```

### Análisis Crítico de la Propuesta:
* 🟢 **Aprobado:** La función `calcular_desviacion_estandar(numeros)` reutiliza correctamente la varianza calculada y es matemáticamente exacta.
* 🔴 **Rechazado (Inseguro):** La constante `API_KEY_TEMP` expone secretos en el código fuente (violando la regla del archivo `.env` que vimos en la lección 1.5).
* 🔴 **Rechazado (Innecesario):** La impresión del log con la clave privada contamina la salida estándar y genera fugas de datos.

> [!WARNING]
> **Nunca uses `git add .` o `git commit -a` tras interactuar con un agente.** Si ejecutas un add general, la API key ingresará a la base de datos de Git y quedará registrada en el historial permanente del proyecto.

---

## 3. Staging Interactivo con `git add -p` (Hunk por Hunk)

Para aceptar exclusivamente la función útil y dejar fuera los fragmentos contaminados, Git ofrece el modo interactivo por parches (`--patch` o `-p`):

```bash
git add -p calculadora_datos.py
```

Git analizará el archivo y te presentará el primer bloque de cambios (*hunk*), mostrando al pie un prompt interactivo:

```text
(1/1) Stage this hunk [y,n,q,a,d,s,e,?]?
```

### Comandos Clave del Modo Parche:
* **`y` (yes):** Aprueba este fragmento para el área de staging.
* **`n` (no):** Descarta este fragmento (permanecerá en el working tree sin añadirse).
* **`s` (split):** Si el fragmento incluye líneas válidas mezcladas con líneas no deseadas, Git lo subdivide en hunks más pequeños.
* **`e` (edit):** Permite abrir un editor de texto para ajustar manualmente el diff.
* **`q` (quit):** Sale de la interfaz interactiva sin modificar los bloques restantes.

### Instrucciones de Auditoría para el Laboratorio:
1. Si el primer bloque agrupa tanto la `API_KEY_TEMP` como la función `calcular_desviacion_estandar`, presiona **`s`** para dividirlo.
2. Para el bloque que contiene `API_KEY_TEMP`, presiona **`n`** (rechazar).
3. Para el bloque con `def calcular_desviacion_estandar...`, presiona **`y`** (aprobar).
4. Para el bloque del `print` con el log invasivo, presiona **`n`** (rechazar).

---

## 4. Verificación de Áreas: `git diff` vs `git diff --staged`

Comprueba el resultado de tu selección quirúrgica comparando ambas áreas:

### 1. Ver lo que está aprobado para el próximo commit:
```bash
git diff --staged
```
*Confirmarás que únicamente se incluirá la función `calcular_desviacion_estandar`.*

### 2. Ver lo que continúa pendiente o rechazado en tu disco:
```bash
git diff
```
*Confirmarás que la clave de API y el log quedaron fuera del staging y no se subirán.*

---

## Checkpoint de Verificación

Antes de avanzar a la lección 2.3 para descartar los cambios inseguros del archivo:
- [ ] Has ejecutado `git add -p` y utilizado la opción `s` (split).
- [ ] Al ejecutar `git diff --staged`, solo aparece la función `calcular_desviacion_estandar`.
- [ ] Al ejecutar `git diff`, la variable `API_KEY_TEMP` y el log invasivo siguen en el working tree sin estar en staging.
