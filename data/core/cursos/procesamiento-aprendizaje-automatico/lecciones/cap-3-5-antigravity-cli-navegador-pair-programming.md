# Guía de Laboratorio — Lección 3.5: AGY CLI en Acción: Control del Navegador (/browser), Documentación Técnica y Pair Programming

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** Asistentes de IA para Estudiantes: OpenCode y Antigravity CLI  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado la Lección 3.4 (Setup de Antigravity CLI).

---

## 1. El Superpoder del Navegador Web Integrado en la Terminal

Uno de los problemas más frecuentes de los modelos de inteligencia artificial es la **obsolescencia del conocimiento**: un modelo entrenado hace un año puede no conocer una función que cambió en la versión más reciente de Scikit-Learn o Pandas, generando código con advertencias de desuso (*DeprecationWarning*) o argumentos inexistentes.

**Antigravity CLI** resuelve esto de raíz al incorporar un **motor de navegación web autónomo (`/browser`)**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   FLUJO DE CONSULTA WEB CON AGY CLI                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Instrucción en Consola ──► El agente detecta una duda sobre una API │
│ 2. Activación /browser    ──► Abre sesión headless en Chromium/Playwright│
│ 3. Poda de HTML           ──► Convierte la documentación oficial a MD   │
│ 4. Verificación de Firma  ──► Valida los parámetros exactos de la lib   │
│ 5. Generación de Código   ──► Escribe código sin errores de versión     │
└────────────────────────────────────────────────────────────────────────┘
```

El agente no "googlea ciegamente"; ingresa a la documentación técnica oficial, extrae la signatura exacta de la función y la aplica en tu código de forma inmediata.

---

## 2. Activación y Uso del Modo Navegador en `agy`

Puedes invocar el navegador de dos formas:

### Forma 1: Comando Slash `/browser`
Inicia una sesión dedicada de navegación web:

```text
/browser
```

El agente abrirá una instancia de navegador y te permitirá navegar hacia URLs específicas, hacer capturas o inspeccionar elementos interactivos.

### Forma 2: Directiva Natural en una Instrucción Técnica
Puedes pedirle directamente al agente que consulte la web dentro de una tarea de desarrollo:

> *"Utiliza el navegador para buscar la documentación oficial más reciente de `sklearn.preprocessing.StandardScaler`. Comprueba cuáles son los parámetros de inicialización y escribe un ejemplo en `src/pipeline.py`."*

---

## 3. Taller Práctico: Normalización de Señales Eléctricas en `energy-ml`

Nos ubicamos en el repositorio:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
agy
```

### El Desafío de Ingeniería
En `energy-ml`, las mediciones de voltaje oscilan alrededor de 220V, mientras que las de factor de potencia varían entre 0.0 y 1.0. Si entregamos estos datos sin escalar a ciertos algoritmos de Machine Learning, la variable de mayor magnitud numérica (el voltaje) opacará a las demás.

Necesitamos implementar una etapa de escalado o normalización estándar.

### Paso 1: Petición con Asistencia Web

Ingresamos en la consola de `agy`:

> *"Examina `src/pipeline.py`. Necesitamos agregar la clase `EscaladorTelemetria` que normalice las columnas numéricas (`voltaje_v`, `corriente_a`, `potencia_w`) restando la media y dividiendo por la desviación estándar. Consulta mediante el navegador si la fórmula matemática coincide con la de `StandardScaler` de Scikit-Learn y verifica si requiere manejar divisiones por cero cuando la varianza es nula. Implementa la clase con Type Hints, docstring y manejo seguro de división por cero."*

### Paso 2: Observación de la Operación de `agy`

Observa cómo el agente:
1. Activa la herramienta web para contrastar la documentación oficial de Scikit-Learn.
2. Comprueba que cuando la desviación estándar es 0 (señal constante), el escalador estándar retorna 0 en lugar de provocar un error `ZeroDivisionError`.
3. Edita `src/pipeline.py` utilizando un diff unificado quirúrgico sin alterar el resto de las funciones.

---

## 4. Tarea de Validación y Pruebas Unitarias

Dentro de la misma sesión de `agy`, solicitamos la creación del test automatizado:

> *"Crea `tests/test_escalador.py` con pruebas para `EscaladorTelemetria`. Verifica el caso estándar con datos variables y el caso borde con una señal constante donde la varianza sea 0. Luego ejecuta los tests en local."*

Antigravity CLI escribirá el archivo de test y ejecutará `pytest tests/test_escalador.py` en tu terminal local, confirmando el resultado positivo sin que tengas que salir de la sesión interactiva.

---

## 5. Salir y Consolidar en Git

Salimos de Antigravity con `/exit` y revisamos el trabajo realizado:

```bash
git status
git diff src/pipeline.py
pytest
```

Consolidamos el avance con un commit atómico:

```bash
git add src/pipeline.py tests/test_escalador.py
git commit -m "feat(pipeline): implementar EscaladorTelemetria validado con documentacion web oficial"
```

---

## 6. Balance y Cierre del Capítulo 3

Con la culminación de este capítulo, cuentas con un **arsenal completo de herramientas de cabecera para toda tu trayectoria académica**:
1. **OpenCode:** Tu asistente de código abierto, gratuito, multi-proveedor y sin tarjeta de crédito.
2. **Antigravity CLI:** Tu entorno de máxima potencia con plan estudiantil de 5 USD/mes, optimización de hardware local y navegador web integrado para resolver cualquier duda técnica viva.

En el **Capítulo 4**, ampliaremos nuestro horizonte técnico explorando el ecosistema corporativo y avanzado: **Claude Code**, la arquitectura interna de **Aider con la API ultra-económica de DeepSeek** y el panorama de **arneses autónomos (Codex, Kimi y DPH)**.
