# Guía de Laboratorio — Lección 3.2: OpenCode: El Asistente Open Source y su Cuota Gratuita para Empezar sin Tarjeta

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** El Cuarteto de IA Agéntica: OpenCode, Antigravity CLI, Claude Code y Aider  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 3.1 (Economía de la IA Agéntica).

---

## 1. ¿Por Qué OpenCode Ocupa el 1er Lugar para Estudiantes?

Al comenzar la carrera técnica, encontrarse con pasarelas de pago, suscripciones en moneda extranjera o requisitos de tarjeta de crédito representa una barrera innecesaria. Por este motivo, **OpenCode** se posiciona como el primer asistente del cuarteto:

* **100% Código Abierto (Open Source):** El código fuente de la herramienta es público y auditable. No depende de los términos cerrados de una única corporación.
* **Cuota Gratuita Aceptable:** Permite operar mediante capas gratuitas comunitarias y proveedores que ofrecen créditos de cortesía (*free tiers* sin necesidad de registrar medios de pago).
* **Multi-Proveedor e Interoperable:** Admite conectar modelos remotos (Groq, OpenRouter, Mistral, Google Gemini Free Tier) o modelos locales que se ejecuten en tu propia máquina mediante Ollama.
* **Integración Nativa con Git y Terminal:** Lee el directorio actual de trabajo, formula diffs quirúrgicos y respeta la estructura del proyecto.

---

## 2. Instalación de OpenCode en el Entorno Local

OpenCode se distribuye habitualmente como un paquete ejecutable para entornos Node.js o como binario compilado multiplataforma.

### Verificación de Requisitos Previos

Abre tu terminal Bash y comprueba la versión de Node y npm disponible en tu sistema:

```bash
node -v
npm -v
```

### Instalación Global mediante npm / npx

Puedes instalar la herramienta de forma global en tu máquina o ejecutarla bajo demanda:

```bash
npm install -g opencode-ai
```

*(O verificar su disponibilidad directa mediante `npx opencode-ai --help`)*.

---

## 3. Configuración Inicial sin Tarjeta de Crédito

Al iniciar OpenCode por primera vez, el asistente te consultará por el proveedor de inferencia que deseas vincular:

```bash
opencode setup
```

### Opciones de Conexión Recomendadas para el ISFT N° 199

1. **Opción A: Proveedor Gratuito Comunitario (Zen / Free Tier):**
   - Selecciona la opción de nivel gratuito predeterminada de OpenCode.
   - Permite un volumen diario de consultas suficiente para resolver ejercicios de laboratorio, crear funciones y analizar errores de sintaxis sin desembolsar dinero.
2. **Opción B: API Key Gratuita de Google AI Studio (Gemini Flash):**
   - Si dispones de una cuenta de Google, puedes generar una clave gratuita en [Google AI Studio](https://aistudio.google.com/) con generosos límites por minuto (*rate limits*) sin costo.
   - Configura la clave en tu entorno:
     ```bash
     export OPENCODE_API_KEY="tu-clave-aistudio-aqui"
     ```
3. **Opción C: Motor 100% Local y Privado con Ollama:**
   - Si tu equipo cuenta con GPU o CPU suficiente, puedes ejecutar modelos locales como `llama3.2` o `qwen2.5-coder` sin conexión a internet ni consumo de saldo.

---

## 4. Taller Práctico: Auditoría y Refactor en `energy-ml`

Nos ubicamos en el repositorio de trabajo `energy-ml` que clonamos y configuramos en los capítulos anteriores:

```bash
cd ~/proyectos_software/energy-ml
```

### Paso 1: Iniciar OpenCode en el Directorio del Repositorio

Inicia el asistente indicando explícitamente el contexto de la tarea para evitar lecturas innecesarias:

```bash
opencode --context src/preprocesamiento.py
```

### Paso 2: Instrucción Técnica de Verificación

Envía la siguiente consigna al asistente:

> *"Inspecciona la función `limpiar_datos` en `src/preprocesamiento.py`. Verifica si maneja adecuadamente los registros con valores negativos en el consumo eléctrico. Si no lo hace, añade una regla que descarte o marque los valores menores a 0 kWh con una advertencia y retorna el DataFrame limpio. Asegúrate de incluir anotaciones de tipo completas."*

### Paso 3: Análisis del Diff Propuesto

OpenCode presentará un diff unificado en la consola similar al que aprendiste a interpretar en la Lección 2.1:

```diff
--- a/src/preprocesamiento.py
+++ b/src/preprocesamiento.py
@@ -14,6 +14,11 @@ def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
     """Limpia valores nulos y registros corruptos."""
     df_limpio = df.dropna().copy()
+    # Filtro de seguridad: el consumo en kWh no puede ser negativo
+    consumo_invalido = df_limpio['kwh'] < 0
+    if consumo_invalido.any():
+        df_limpio = df_limpio[~consumo_invalido]
     return df_limpio
```

---

## 5. Salir del Asistente y Consolidar en Git

Una vez aceptado el cambio propuesto por OpenCode, sal de la herramienta con `exit` o `Ctrl+C` y audita el cambio en Git:

```bash
git status
git diff src/preprocesamiento.py
pytest tests/
```

Si las pruebas pasan exitosamente, realiza tu commit atómico:

```bash
git add src/preprocesamiento.py
git commit -m "fix(pipeline): filtrar consumos anomalos negativos sugerido por OpenCode"
```

---

## 6. Conclusión y Buenas Prácticas

OpenCode demuestra que **no es necesario contar con un presupuesto para iniciarse profesionalmente en el desarrollo asistido por IA**. Su condición de software libre garantiza que siempre tendrás acceso a una herramienta de desarrollo en consola, independiente de cambios en las políticas de suscripción de plataformas comerciales.

En la siguiente lección, daremos el salto al segundo componente del cuarteto: **Antigravity CLI**, aprovechando el beneficio estudiantil y su integración directa con el navegador web.
