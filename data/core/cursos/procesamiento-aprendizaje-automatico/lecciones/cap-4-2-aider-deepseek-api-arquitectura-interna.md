# Guía de Laboratorio — Lección 4.2: Aider con DeepSeek API (Opcional): Arquitectura Agéntica Interna, Repomap y AST

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 4:** Ecosistema Avanzado de IA Agéntica: Claude Code, Aider y Arneses Autónomos  
**Carga horaria estimada:** 30 min  
**Prerrequisitos:** Haber completado la Lección 4.1 (Claude Code).

---

## 1. ¿Por Qué Aider es la Mejor Herramienta para Entender la IA Agéntica por Dentro?

Mientras que muchas herramientas comerciales operan como "cajas negras" con interfaces cerradas, **Aider** es el proyecto de código abierto pionero que definió la arquitectura de los agentes de pair programming en consola con Git.

Estudiar Aider nos permite desmitificar cómo un agente de IA comprende un proyecto completo sin saturar su ventana de contexto ni alucinar rutas inexistentes:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ARQUITECTURA INTERNA DE UN AGENTE (AIDER)            │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Árbol de Archivos ──► Árbol de Sintaxis Abstracta (AST) de cada .py │
│ 2. Grafo de Símbolos ──► Clases, funciones y llamadas entre módulos    │
│ 3. PageRank          ──► Identifica los 20 símbolos más influyentes    │
│ 4. Repo-map          ──► Esquema ultra-compacto (<1000 tokens) inyectado│
│ 5. Prompt de Edición ──► Instrucción de reemplazo quirúrgico (Search/Replace)
└────────────────────────────────────────────────────────────────────────┘
```

> ℹ️ **Carácter Opcional:**  
> Esta lección está pensada para estudiantes con vocación técnica profunda que deseen comprender la ciencia de la ingeniería agéntica y el consumo granular de tokens por API.

---

## 2. El Repomap: La Solución Elegante al Problema del Contexto

Imagina un repositorio con 200 archivos y 50.000 líneas de código. Si intentaras enviarle todos los archivos a un modelo en cada consulta:
1. El costo por petición sería astronómico (varios dólares por mensaje).
2. El modelo sufriría de *"pérdida de atención"* (*needle in a haystack*), cometiendo errores groseros.
3. El tiempo de respuesta sería inaceptablemente lento.

### ¿Cómo Resuelve Aider Este Desafío?
Aider utiliza **Tree-sitter** para analizar el **AST (Árbol de Sintaxis Abstracta)** de cada archivo del proyecto. Extrae exclusivamente las firmas de las funciones, los argumentos tipados y las definiciones de clases, omitiendo los cuerpos internos de las funciones.

Luego, aplica un algoritmo de **PageRank** sobre el grafo de llamadas para priorizar los símbolos más referenciados del proyecto. El resultado es un mapa esquemático de alta densidad informativa llamado **`Repo-map`**, que suele ocupar menos del 2% de los tokens que requeriría el código completo.

---

## 3. Formatos de Edición: Por Qué Reescribir Archivos Enteros es un Error de Diseño

Cuando un LLM genera código, cada token de salida cuesta el doble que un token de entrada y tiene un límite estricto de generación (usualmente 4096 u 8192 tokens). Si un agente reescribe un archivo entero de 800 líneas solo para cambiar 2 líneas:
* Desperdicia miles de tokens de salida.
* Corre el riesgo de que la respuesta se corte por la mitad si se agota la ventana de salida.
* Puede introducir regresiones accidentales en funciones que no debían modificarse.

Aider resolvió este problema obligando al modelo a responder exclusivamente con bloques de **Búsqueda y Reemplazo Quirúrgico (*Search/Replace Blocks*)**:

```text
<<<<<<< SEARCH
def calcular_consumo(potencia, tiempo):
    return potencia * tiempo
=======
def calcular_consumo(potencia: float, tiempo: float) -> float:
    """Calcula el consumo en vatios-hora garantizando valores positivos."""
    if potencia < 0 or tiempo < 0:
        raise ValueError("Potencia y tiempo deben ser valores no negativos.")
    return potencia * tiempo
>>>>>>> REPLACE
```

El motor local de Aider busca el bloque original en el archivo y lo reemplaza con precisión milimétrica.

---

## 4. Instalación de Aider en el Entorno Virtual

Instalamos Aider dentro del entorno virtual de nuestro proyecto para mantener las librerías aisladas:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
pip install aider-chat
```

Verificamos la instalación:

```bash
aider --version
```

---

## 5. Conexión con la API de DeepSeek

Para experimentar con Aider bajo el modelo de pago por uso más eficiente del mercado, utilizaremos la API de **DeepSeek**:

```bash
export DEEPSEEK_API_KEY="sk-tu-clave-aqui"
```

Iniciamos Aider indicando el modelo y un archivo de prueba en `energy-ml`:

```bash
aider --model deepseek/deepseek-chat src/pipeline.py
```

Al iniciar, observarás en la terminal el mensaje de inicialización del `Repo-map` y el desglose de archivos incluidos en el contexto activo.

---

## 6. Conclusión

Aider nos permite comprender cómo los agentes de desarrollo más avanzados gestionan la memoria del código mediante **Árboles de Sintaxis Abstracta (AST)**, **PageRank** y **bloques de edición quirúrgica**.

En la siguiente lección, aprenderemos a gestionar **la seguridad financiera en el pago por uso**, configurando un saldo prepago controlado de **2 USD en DeepSeek** y aprovechando su **50% de descuento en horario nocturno**.
