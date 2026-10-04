# Guía de Laboratorio — Lección 3.3: Antigravity CLI: La Mejor Relación Calidad/Precio para Estudiantes y Modo Navegador

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** El Cuarteto de IA Agéntica: OpenCode, Antigravity CLI, Claude Code y Aider  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado la Lección 3.2 (OpenCode).

---

## 1. ¿Por Qué Antigravity CLI Ocupa el 2do Lugar para Estudiantes?

Cuando un estudiante busca dar el salto desde herramientas gratuitas a un entorno con modelos de frontera y capacidades agénticas avanzadas, **Antigravity CLI (`agy`)** representa **la mejor relación costo-beneficio de toda la industria**:

* **Tarifa Estudiantil Bonificada:** Mediante el programa para instituciones educativas y estudiantes (con correo `@abc.gob.ar` o acreditación académica), se accede a un **descuento de 15 USD por mes durante 12 meses**. Esto reduce el plan estándar de 20 USD a únicamente **5 USD mensuales**.
* **Cuota Extremadamente Generosa:** Por 5 USD al mes, ofrece acceso intensivo a modelos de última generación (como Gemini Pro y Flash de Google DeepMind) sin el riesgo de agotar la cuota en pocas preguntas.
* **Control de Navegador Web Integrado (`/browser`):** Permite al agente no solo leer archivos locales, sino navegar páginas web, consultar documentación oficial de librerías en tiempo real, extraer datasets y validar interfaces gráficas.
* **Orquestación Multi-Agente y Poda AST:** Dispone de integración nativa con herramientas de bajo consumo de contexto para inspección quirúrgica de código.

---

## 2. Instalación y Autenticación de Antigravity CLI

Antigravity CLI se instala en la terminal Bash mediante el gestor oficial o el paquete binario de Google DeepMind:

```bash
curl -fsSL https://antigravity.google/install.sh | bash
```

### Comprobación de Instalación y Versión

Verifica que el ejecutable `agy` se encuentre en tu `$PATH`:

```bash
agy --version
```

### Autenticación con Cuenta Estudiantil

Para activar el beneficio de 5 USD/mes, autentica tu sesión vinculando tu cuenta educativa:

```bash
agy auth login
```

El comando abrirá el navegador para autorizar las credenciales y guardar el token seguro en `~/.gemini/antigravity-cli/`.

---

## 3. Configuración y Uso del Modo Navegador (`/browser`)

Una de las ventajas competitivas más destacadas de Antigravity CLI frente a otros asistentes de consola es su **motor de navegación web headless e interactivo**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│               FLUJO DE TRABAJO AGÉNTICO CON NAVEGADOR                 │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Consulta del Agente ──► Inspección Web (Playwright / Chromium)      │
│ 2. Extracción de Datos ──► Filtrado de Markdown sin publicidad/scripts │
│ 3. Inyección Local     ──► Aplicación directa de la API al código      │
└────────────────────────────────────────────────────────────────────────┘
```

### Activación del Navegador en Sesión Interactiva

Dentro de una sesión interactiva de Antigravity, puedes solicitar al agente que busque o inspeccione documentación técnica en internet utilizando el comando slash `/browser`:

```text
/browser
```

O formulando la instrucción técnica directamente:

> *"Utiliza el navegador para buscar la documentación más reciente de la función `train_test_split` de Scikit-Learn. Verifica cuáles son los argumentos obligatorios y cómo se configura el parámetro `stratify`."*

### ¿Por Qué Esta Capacidad es Revolucionaria para el Estudiante?

1. **Cero Alucinaciones por Datos Desactualizados:** Los modelos de IA tienen una fecha de corte de conocimiento. Con `/browser`, el agente consulta la versión exacta de la librería instalada en tu entorno virtual.
2. **Descarga y Validación de Datasets:** El agente puede verificar si una URL pública de un dataset de energía está activa y descargar únicamente la cabecera CSV para validar su esquema sin saturar la memoria.

---

## 4. Taller Práctico: Refactor Asistido con `agy` sobre `energy-ml`

Navegamos al repositorio `energy-ml`:

```bash
cd ~/proyectos_software/energy-ml
```

Iniciamos Antigravity CLI en el espacio de trabajo actual:

```bash
agy
```

### Paso 1: Petición Técnica con Restricciones

Ingresamos la siguiente instrucción en la consola de Antigravity:

> *"Examina `src/modelo.py` y los tests en `tests/test_modelo.py`. Necesitamos agregar una función `calcular_metricas_regresion(y_real: list[float], y_pred: list[float]) -> dict[str, float]` que retorne el Error Cuadrático Medio (MSE) y el Error Absoluto Medio (MAE). Consulta con el navegador si la definición matemática de Scikit-Learn coincide con la nuestra. Agrega su correspondiente test unitario en `tests/test_metricas.py` y ejecuta `pytest`."*

### Paso 2: Ejecución Autónoma y Diagnóstico Local

Antigravity CLI:
1. Usará `/browser` o consulta HTTP para contrastar la firma estándar de Scikit-Learn.
2. Escribirá el archivo `src/metricas.py` o editará `src/modelo.py`.
3. Creará el archivo de test `tests/test_metricas.py`.
4. Ejecutará automáticamente `pytest tests/test_metricas.py` en la terminal local sin gastar tokens en ciclos de prueba manuales.

### Paso 3: Revisión de Diffs y Commit Atómico

Sal de la sesión interactiva con `/quit` o `exit` y verifica el resultado en Git:

```bash
git status
git diff --stat
pytest
```

Registramos el avance en el historial con un commit atómico:

```bash
git add src/ tests/
git commit -m "feat(metricas): incorporar cálculo de MAE y MSE validado por Antigravity CLI"
```

---

## 5. Recomendación de Uso en la Carrera

Gracias a su tarifa de 5 USD/mes, Antigravity CLI se convierte en el **asistente de cabecera predeterminado** para cursar las asignaturas técnicas del instituto. Te brinda potencia de nivel comercial con el presupuesto accesible de un plan universitario.

En la siguiente lección, exploraremos **Claude Code**, el asistente preferido en entornos corporativos para comprender cómo operan los equipos en la industria.
