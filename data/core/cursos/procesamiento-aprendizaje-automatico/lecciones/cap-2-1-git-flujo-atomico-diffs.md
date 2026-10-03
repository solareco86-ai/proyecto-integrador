# Guía de Laboratorio Práctico — Capítulo 2: Auditoría de Código y Flujo Atómico de Cambios

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 3 horas (de 20 hs totales)

---

## Objetivos de Aprendizaje

Al finalizar este laboratorio, el estudiante será capaz de:
1. Comprender por qué la auditoría crítica es la competencia fundamental al desarrollar con agentes de IA (evitando la "aceptación ciega").
2. Preparar un entorno de práctica aislado dentro del espacio del curso (`aprendizaje-automatico/lab-auditoria/`).
3. Construir la versión base de un script Python (`calculadora_datos.py`) y crear el primer commit del repositorio.
4. Ejecutar e interpretar la anatomía de un `git diff` línea por línea (bloques de contexto, líneas agregadas `+`, líneas removidas `-` y metadatos de hunks `@@`).

---

## 1. El Riesgo de la Aceptación Ciega: Por qué auditar a los agentes de código

Los asistentes de Inteligencia Artificial (Aider, OpenCode, ChatGPT, Claude) pueden redactar decenas de líneas de código en milisegundos. Sin embargo, en proyectos profesionales de Ciencia de Datos y Machine Learning conllevan tres riesgos graves:

1. **Alucinaciones Funcionales:** Reescribir algoritmos correctos con variantes que modifican sutilmente el comportamiento matemático o rompen compatibilidad.
2. **Inyección de Credenciales Hardcodeadas:** Escribir llaves de API falsas o tokens de prueba directamente en el código fuente en lugar de respetar la arquitectura de variables de entorno (`.env`).
3. **Refactorización Invasiva no Solicitada:** Cambiar nombres de variables, reformatear imports o alterar la estructura de directorios sin que se lo hayamos pedido.

> [!IMPORTANT]
> **Principio de Auditoría Activa:** El desarrollador humano es 100% responsable del código que ingresa a la base de código. Ninguna sugerencia de un agente se acepta sin ser inspeccionada previamente con `git diff`.

---

## 2. Preparación del Laboratorio en el Espacio de Trabajo

En la lección 1.3 ya configuraste tu identidad global de autor en Git (`user.name` y `user.email`). Ahora crearemos un laboratorio de práctica dentro de la carpeta del curso que estructuramos en la lección 1.2:

### Paso 1: Navegar al espacio de trabajo y crear la carpeta de práctica
Abre tu consola (**Git Bash**, **WSL** o **GNU/Linux Nativo**) y navega a la carpeta de trabajo:

```bash
# Navegar a la carpeta del curso (adaptado a tu plataforma)
if [ -d "$HOME/Desktop/aprendizaje-automatico" ]; then
    cd "$HOME/Desktop/aprendizaje-automatico"
elif [ -d "$HOME/Escritorio/aprendizaje-automatico" ]; then
    cd "$HOME/Escritorio/aprendizaje-automatico"
elif [ -d "/mnt/c/Users/$WIN_USER/Desktop/aprendizaje-automatico" ]; then
    cd "/mnt/c/Users/$WIN_USER/Desktop/aprendizaje-automatico"
elif [ -d "/c/Users/$USERNAME/Desktop/aprendizaje-automatico" ]; then
    cd "/c/Users/$USERNAME/Desktop/aprendizaje-automatico"
fi

# Crear la carpeta del laboratorio e ingresar
mkdir -p lab-auditoria
cd lab-auditoria

# Inicializar un nuevo repositorio local
git init
```

### Paso 2: Crear el archivo base `calculadora_datos.py`
Crea el script utilitario de análisis estadístico inicial:

```bash
cat << 'EOF' > calculadora_datos.py
import math

def calcular_promedio(numeros):
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)

if __name__ == "__main__":
    datos = [10.5, 20.0, 30.2, 40.8]
    print(f"Datos: {datos}")
    print(f"Promedio: {calcular_promedio(datos):.2f}")
EOF
```

### Paso 3: Configurar el archivo `.gitignore`
Protege el repositorio contra archivos de caché y entornos locales:

```bash
cat << 'EOF' > .gitignore
.env
venv/
__pycache__/
*.pyc
EOF
```

### Paso 4: Registrar el Commit Inicial
Guarda el estado base limpio en Git:

```bash
git add .
git commit -m "feat: version inicial de calculadora_datos y gitignore"
git log --oneline
```

---

## 3. Primera Modificación y Anatomía de `git diff`

Para comprender cómo Git detecta los cambios antes de aceptarlos, agrega manualmente una función simple de varianza al script:

```bash
cat << 'EOF' > calculadora_datos.py
import math

def calcular_promedio(numeros):
    if not numeros:
        return 0.0
    return sum(numeros) / len(numeros)

def calcular_varianza(numeros):
    if not numeros or len(numeros) < 2:
        return 0.0
    media = calcular_promedio(numeros)
    return sum((x - media) ** 2 for x in numeros) / (len(numeros) - 1)

if __name__ == "__main__":
    datos = [10.5, 20.0, 30.2, 40.8]
    print(f"Datos: {datos}")
    print(f"Promedio: {calcular_promedio(datos):.2f}")
    print(f"Varianza: {calcular_varianza(datos):.2f}")
EOF
```

Ahora ejecuta el comando esencial de auditoría:

```bash
git diff
```

### Desglose de la Salida de `git diff`:

1. **`--- a/calculadora_datos.py`:** Representa la versión previa (el estado del último commit).
2. **`+++ b/calculadora_datos.py`:** Representa la versión modificada en tu disco (working tree).
3. **`@@ -7,4 +7,10 @@` (*Hunk Header*):** Indica que a partir de la línea 7 de la versión original se reemplazaron 4 líneas por 10 líneas de la versión nueva.
4. **Líneas con `+` (verde):** Código nuevo agregado.
5. **Líneas con `-` (rojo):** Código eliminado.
6. **Líneas sin prefijo:** Contexto adyacente (usualmente 3 líneas arriba y abajo) para orientar la lectura.

---

## 4. Registro del Cambio Auditado

Dado que la función `calcular_varianza` es matemáticamente sólida y no introduce efectos secundarios ni claves privadas, aprobamos el cambio:

```bash
git add calculadora_datos.py
git commit -m "feat: agregar calculo de varianza muestral"
git log --oneline
```

---

## Checkpoint de Verificación

Antes de avanzar a la simulación con propuestas complejas de IA en la lección 2.2:
- [ ] La carpeta `lab-auditoria/` reside dentro de `aprendizaje-automatico/`.
- [ ] Al ejecutar `git status`, la consola indica `working tree clean`.
- [ ] Al ejecutar `git log --oneline`, se aprecian los dos primeros commits atómicos.
- [ ] Comprendes la estructura de un *hunk* (`@@`) y los indicadores `+` / `-` de `git diff`.
