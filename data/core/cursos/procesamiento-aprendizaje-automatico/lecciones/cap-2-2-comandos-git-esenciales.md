# Guía de Laboratorio: Capítulo 2 — Git como Fundamento del Trabajo con Agentes

**Curso:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga Horaria:** 2.5 - 3 Horas de Práctica Guiada  

---

## 🛠️ Parte 2: Simulación de Propuestas Generadas por un Agente IA

Imagina que solicitaste a un agente de código lo siguiente:  
> *"Optimiza el script `calculadora_datos.py` agregando una función de desviación estándar y formateo de logs."*

El agente procesa la solicitud y modifica `calculadora_datos.py`. Ejecutemos la simulación del código modificado por la IA:

```bash
cat << 'EOF' > calculadora_datos.py
import math

# API KEY DE PRUEBA GENERADA POR EL AGENTE (¡ERROR GRAVE!)
API_KEY_TEMP = "sk-proj-9999888877776666"

def calcular_promedio(numeros):
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)

def calcular_desviacion_estandar(numeros):
    if not numeros or len(numeros) < 2:
        return 0.0
    media = calcular_promedio(numeros)
    varianza = sum((x - media) ** 2 for x in numeros) / (len(numeros) - 1)
    return math.sqrt(varianza)

if __name__ == "__main__":
    datos = [10.5, 20.0, 30.2, 40.8]
    print(f"[LOG INFO] Clave activa: {API_KEY_TEMP}") # Inyección no deseada
    print(f"Datos: {datos}")
    print(f"Promedio: {calcular_promedio(datos):.2f}")
    print(f"Desviación Estándar: {calcular_desviacion_estandar(datos):.2f}")
EOF
```

---

## 🕵️‍♂️ Parte 3: Protocolo de Auditoría y Staging Interactivo (`git add -p`)

No ejecutes `git add .` a ciegas. Sigue el protocolo de tres pasos:

### Paso 3.1: Inspección de Estado
Comprueba qué archivos sufrieron modificaciones:

```bash
git status
```

### Paso 3.2: Lectura Crítica con `git diff`
Inspecciona exactamente qué líneas agregó o eliminó la IA:

```bash
git diff
```

**Análisis de Auditoría:**
* 🟢 **Aceptable:** La función `calcular_desviacion_estandar` está matemáticamente correcta y bien estructurada.
* 🔴 **Rechazado (Inseguro):** La variable `API_KEY_TEMP` expone credenciales hardcodeadas en código fuente.
* 🔴 **Rechazado (Innecesario):** El print del log expone la clave privada en consola.

### Paso 3.3: Staging Parcial e Interactivo con `git add -p`
Ejecuta el comando interactivo por fragmentos (*hunks*):

```bash
git add -p calculadora_datos.py
```

Git mostrará los bloques de cambios. Durante el modo interactivo de `git add -p`, dispones de las siguientes claves principales:
- `y`: Aceptar este fragmento para staging.
- `n`: Omitir este fragmento.
- `s`: Dividir (*split*) el fragmento en bloques más pequeños si hay cambios juntos.
- `e`: Editar manualmente el fragmento antes de staging.
- `q`: Salir de la interfaz interactiva.

#### Instrucciones de Selección para el Ejercicio:
1. Si el fragmento incluye tanto la API Key como la función nueva, presiona **`s`** para dividir el bloque.
2. Para el bloque que contiene la `API_KEY_TEMP`, presiona **`n`** (no staging).
3. Para el bloque con la función `calcular_desviacion_estandar`, presiona **`y`** (staging).
4. Para el bloque de ejecución principal que imprime la clave privada, presiona **`n`**.

### Paso 3.4: Verificación del Área de Staging
Compara lo que quedó listo para commit versus los cambios rechazados:

```bash
# Ver cambios aprobados para commit
git diff --staged

# Ver cambios pendientes o descartados
git diff
```
