# Guía de Laboratorio — Lección 3.5: Aider con DeepSeek API (Opcional): Arquitectura Agéntica Interna, Repomap y Pago por Uso

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** El Cuarteto de IA Agéntica: OpenCode, Antigravity CLI, Claude Code y Aider  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado las Lecciones 3.1 a 3.4.

---

## 1. ¿Por Qué Aider es Clave para Entender la IA Agéntica por Dentro?

Mientras que otras herramientas comerciales presentan una interfaz pulida pero cerrada, **Aider** es el proyecto de código abierto que definió los estándares modernos de pair programming en consola con Git.

Estudiar Aider nos permite comprender los fundamentos de la ingeniería agéntica:
1. **El Mapa de Repositorio (*Repository Map / Repomap*):** ¿Cómo hace un LLM con una ventana de contexto limitada para no perderse en un proyecto de 500 archivos? Aider analiza el Árbol de Sintaxis Abstracta (AST) de cada archivo y construye un grafo compacto de clases, funciones e identificadores clave clasificados por PageRank.
2. **Formatos de Edición Quirúrgica:** En lugar de reescribir un archivo completo de 1000 líneas (lo que gastaría miles de tokens de salida y arriesgaría cortes por límite de longitud), Aider entrena y guía al modelo para producir diffs unificados mínimos (*search/replace blocks*).
3. **Commits Atómicos con Mensajes Contextuales:** Cada vez que el agente completa una tarea exitosa, formula un commit en Git con un mensaje estructurado que describe exactamente el cambio.

> ℹ️ **Carácter Opcional:**  
> Esta lección es opcional y está pensada para estudiantes con inquietud por la arquitectura interna de los agentes y que deseen experimentar con una API comercial bajo el modelo de pago por uso.

---

## 2. Configuración Segura: Saldo Prepago de 2 USD en DeepSeek

Para esta práctica, utilizaremos la API de **DeepSeek**, el proveedor más económico y eficiente del mercado:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   CONFIGURACIÓN DE SEGURIDAD FINANCIERA                │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Crear cuenta en https://platform.deepseek.com/                      │
│ 2. Cargar un saldo prepago inicial de exactamente 2 USD.               │
│ 3. Desactivar recargas automáticas (Auto-recharge: OFF).               │
│ 4. Generar una API Key y guardarla en variables de entorno locales.    │
└────────────────────────────────────────────────────────────────────────┘
```

Con una tarifa base de ~0,14 USD por millón de tokens de entrada y ~0,28 USD por millón de tokens de salida, **2 USD equivalen a más de 7 millones de tokens**, suficiente para decenas de sesiones de laboratorio completas.

### Aprovechamiento del Descuento Horario (*Off-Peak Discount*)

Recordemos la ventaja estratégica de DeepSeek:
* **Franja Horaria Bonificada:** De **16:30 a 00:30 UTC** (en Argentina: de **13:30 a 21:30 hs**).
* **Descuento:** **50% de reducción** en las tarifas de tokens.
* Si programas durante la tarde o noche, ¡tus 2 USD rendirán el doble!

---

## 3. Instalación de Aider en el Entorno Virtual

Recomendamos instalar Aider utilizando `pipx` o dentro de un entorno virtual aislado para no alterar las librerías del sistema:

```bash
pip install aider-chat
```

### Configuración de la Clave de API

Exporta tu clave de DeepSeek en tu terminal:

```bash
export DEEPSEEK_API_KEY="sk-tu-clave-secreta"
```

---

## 4. Taller Práctico: Sesión de Desarrollo en `energy-ml`

Nos posicionamos en el repositorio `energy-ml`:

```bash
cd ~/proyectos_software/energy-ml
```

### Paso 1: Iniciar Aider con el Modelo de DeepSeek y Repomap

Iniciamos Aider vinculándolo a DeepSeek y agregando el archivo sobre el que queremos trabajar:

```bash
aider --model deepseek/deepseek-chat src/pipeline.py
```

Observa la salida inicial de Aider en la consola:
* Notarás que Aider escanea el repositorio y genera el *Repo-map* resumiendo los símbolos de `energy-ml`.
* Informa el costo estimado de tokens al inicio de la sesión.

### Paso 2: Instrucción Técnica de Prueba

En la consola de Aider, escribe la siguiente consigna:

> *"Agrega una función `generar_resumen_estadistico(df: pd.DataFrame) -> dict[str, float]` en `src/pipeline.py` que calcule la media, mediana y desviación estándar de la columna `kwh`. Retorna los valores redondeados a 2 decimales. Incluye Type Hints completos y docstring explicativo."*

### Paso 3: Observación de la Magia Agéntica

Observa la pantalla:
1. DeepSeek genera un bloque de búsqueda y reemplazo (*diff*).
2. Aider aplica el diff directamente en `src/pipeline.py`.
3. Aider detecta que Git está limpio y **realiza automáticamente un commit atómico**:
   ```text
   Commit 8a1b2c3: Agregada función generar_resumen_estadistico en src/pipeline.py
   ```
4. Aider muestra en pantalla el desglose exacto de tokens consumidos y el costo en centavos de dólar (típicamente menos de 0,005 USD).

---

## 5. Salir de Aider e Inspeccionar el Historial

Escribe `/exit` o `/quit` para salir de Aider. Luego verifica el commit realizado por el agente:

```bash
git log -n 1 --stat
git show HEAD
```

Comprobarás cómo Aider no solo editó el archivo con precisión quirúrgica, sino que mantuvo la higiene de tu historial de Git.

---

## 6. Conclusión: La Diferencia Fundamental

Comprender la diferencia entre una **suscripción mensual fija** ($5 o $20 con límites de cuota) y el **pago por uso con APIs hiper-competitivas como DeepSeek** es una competencia técnica invaluable. Te permite elegir la herramienta más adecuada según el volumen de trabajo, el presupuesto y la criticidad del proyecto.

En la lección final del capítulo, completaremos el panorama analizando otros **arneses de IA agéntica** fundamentales del ecosistema: **Codex**, **Kimi Code** y **DeepSeek Harness (DPH)**.
