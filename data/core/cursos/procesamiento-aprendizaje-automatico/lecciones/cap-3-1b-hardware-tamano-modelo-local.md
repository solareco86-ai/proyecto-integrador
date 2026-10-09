# Guía de Laboratorio — Lección 3.1b: Hardware y Tamaño de Modelo para Inferencia Local

En la lección 3.1 comparamos el costo de usar modelos en la nube con el de ejecutarlos en tu propia máquina. Esta lección trata la segunda opción. Antes de instalar un modelo local (lección 3.2) tienes que responder una pregunta de ingeniería: **¿cabe en mi equipo?**

Responderla requiere entender qué es un modelo por dentro. Eso es machine learning, y lo vamos a usar tal como lo viste en el curso.

---

## Objetivos de Aprendizaje

1. Explicar qué es un parámetro y por qué un modelo ocupa memoria.
2. Estimar cuánta memoria necesita un modelo según su cantidad de parámetros y su cuantización.
3. Distinguir la RAM del sistema de la VRAM de la tarjeta gráfica, y entender cómo se reparte un modelo entre ambas.
4. Elegir un tamaño de modelo para tu equipo y justificar la elección con datos.

---

## 1. ¿Qué es un Parámetro?

Un modelo de lenguaje es una función con muchos números ajustables. Esos números se llaman **parámetros** o **pesos**, y el entrenamiento consiste en encontrar buenos valores para ellos.

Ya trabajaste con este concepto en el curso: en **Naive Bayes** (capítulo 3), las probabilidades a priori y condicionales que el modelo aprende desde los datos son sus parámetros.

La diferencia es de escala. Un modelo de **8,2 mil millones de parámetros** (8,2 B) tiene 8.200 millones de números que guardar.

---

## 2. Predicción Antes de Medir

Antes de seguir leyendo, responde por escrito:

> Si cada parámetro se guarda como un número de 32 bits (4 bytes), ¿cuántos gigabytes ocupan los pesos de un modelo de 8,2 B parámetros?

Anota tu estimación. Después compara con el cálculo de la sección 3.

---

## 3. Cuantización: Cuántos Bytes por Parámetro

Cada parámetro se puede guardar con distinta precisión. Menos bits significan menos memoria, a cambio de cierta pérdida de calidad. Ese proceso se llama **cuantización**.

| Precisión | Bytes por parámetro | Memoria aproximada para 8,2 B parámetros |
| :--- | :---: | :---: |
| 32 bits (float32) | 4 | ~32,8 GB |
| 16 bits (float16) | 2 | ~16,4 GB |
| 8 bits | 1 | ~8,2 GB |
| 4 bits | 0,5 | ~4,1 GB |

Son estimaciones de los pesos solamente. El archivo real suele ser algo mayor, porque incluye metadatos y algunas capas que se conservan en más precisión.

Un ejemplo real del equipo de la cátedra:

```bash
ollama show deepseek-r1:8b
```

**Salida (fragmento):**

```output
  Model
    architecture        qwen3
    parameters          8.2B
    quantization        Q4_K_M
```

El modelo tiene 8,2 B parámetros y está cuantizado en 4 bits (`Q4_K_M`). Su archivo ocupa 5,2 GB en disco, lo que coincide con la fila de 4 bits de la tabla, con un margen por metadatos y capas conservadas.

> [!NOTE]
> Compara tu predicción de la sección 2 con la tabla. Si tu estimación fue de 32 GB, estás en la fila de 32 bits: es la precisión de entrenamiento, no la que se usa para ejecutar modelos locales de forma práctica.

---

## 4. RAM y VRAM: Dónde Vive el Modelo

El modelo tiene que estar cargado en memoria para responder. Hay dos memorias posibles:

* **RAM del sistema:** la memoria general de tu computadora. Ejecutar el modelo solo en CPU usa esta memoria, y es más lento.
* **VRAM:** la memoria de la tarjeta gráfica. Si el modelo cabe completo en la VRAM, se ejecuta en la GPU y responde mucho más rápido.

Si el modelo no cabe completo en la VRAM, Ollama reparte sus capas entre GPU y CPU. Funciona, pero cada respuesta es más lenta. Además, un contexto más largo (más texto de entrada y de respuesta) también consume memoria adicional.

> [!IMPORTANT]
> Una tarjeta gráfica integrada, como las de muchos procesadores de notebooks, usa la RAM del sistema y no tiene VRAM dedicada. En ese caso, el criterio es la RAM disponible.

---

## 5. Medir Tu Equipo

Estos comandos solo leen información. No modifican nada.

```bash
# Memoria RAM total y disponible (GNU/Linux)
free -h

# Modelos instalados y su tamaño en disco
ollama list

# Parámetros y cuantización de un modelo instalado
ollama show <modelo>

# Modelos cargados en este momento y dónde se ejecutan
ollama ps
```

**Salida de `ollama list` en el equipo de la cátedra (ejemplo):**

```output
NAME                                    ID              SIZE      MODIFIED
MFDoom/deepseek-r1-tool-calling:1.5b    92edb72a7c72    1.1 GB    3 weeks ago
deepseek-r1:8b                          6995872bfe4c    5.2 GB    3 weeks ago
```

En `ollama ps`, la columna `PROCESSOR` indica si el modelo corre en CPU, en GPU o repartido entre ambas. Ese dato te dice si tu equipo está respondiendo como esperabas.

Si tienes una tarjeta NVIDIA, `nvidia-smi` muestra la VRAM total y la usada. En Windows, el Administrador de tareas (pestaña Rendimiento) muestra RAM y GPU. En macOS, la información del sistema muestra la memoria instalada.

---

## 6. Elegir el Tamaño del Modelo

La siguiente tabla es **orientativa**. Antes de decidir, verifica con `ollama show` cuántos parámetros tiene el modelo y con `free -h` o tu administrador de tareas cuánta memoria tienes libre. Recuerda que el sistema operativo y tus programas también usan memoria.

| Memoria disponible | Tamaño de modelo recomendado (cuantizado en 4 bits) | Dónde corre |
| :--- | :--- | :--- |
| 8 GB de RAM, sin GPU dedicada | Hasta ~2 B parámetros | CPU (más lento) |
| 16 GB de RAM, sin GPU dedicada | Hasta ~8 B parámetros | CPU (lento para uso intensivo) |
| 8 GB de VRAM | Hasta ~8 B parámetros | GPU |
| 24 GB de VRAM | Hasta ~30 B parámetros | GPU |

> [!TIP]
> Si tu equipo tiene 2 GB de VRAM o menos, usa modelos de alrededor de 1 a 2 B parámetros. El modelo de 1,8 B del ejemplo de la sección 5 ocupa 1,1 GB en disco.

---

## Ejercicio de Verificación

1. Escribe tu predicción de la sección 2 y compárala con la tabla de la sección 3.
2. Ejecuta `free -h` y anota tu RAM total y disponible.
3. Si tienes modelos instalados, ejecuta `ollama list` y `ollama show` sobre uno de ellos. Si no tienes ninguno, usa los datos de los ejemplos.
4. Elige el tamaño de modelo para tu equipo usando la tabla de la sección 6, y justifica tu elección con los números que obtuviste.

---

## Checkpoint de Verificación

Antes de avanzar a la lección 3.2 (OpenCode y Ollama):
- [ ] Explicas qué es un parámetro y das un ejemplo de los que viste en el curso.
- [ ] Calculas la memoria aproximada de un modelo a partir de sus parámetros y su cuantización.
- [ ] Distingues RAM de VRAM y sabes qué pasa cuando el modelo no cabe completo en la GPU.
- [ ] Elegiste un tamaño de modelo para tu equipo y puedes justificarlo con datos.
