# Guía de Laboratorio — Lección 3.2: OpenCode: Instalación, Proveedores Gratuitos y Configuración sin Tarjeta

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** Asistentes de IA para Estudiantes: OpenCode y Antigravity CLI  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 3.1 (Economía de la IA Agéntica).

---

## 1. ¿Qué es OpenCode y Cómo Funciona?

**OpenCode** es una herramienta de asistencia en desarrollo de software construida desde cero bajo la filosofía del **software libre**. A diferencia de extensiones cerradas de editores comerciales, OpenCode se ejecuta de forma nativa en la terminal Bash y desacopla la interfaz del proveedor de inteligencia artificial:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                      ARQUITECTURA MODULAR DE OPENCODE                  │
├────────────────────────────────────────────────────────────────────────┤
│  Terminal Bash ──► OpenCode Engine (Lectura de archivos y AST)        │
│                           │                                            │
│        ┌──────────────────┼─────────────────────────┐                  │
│        ▼                  ▼                         ▼                  │
│  Zen / Free Tier    Google AI Studio          Ollama Local             │
│  (Créditos $0)      (Gemini Flash Gratuito)   (100% Offline en CPU)    │
└────────────────────────────────────────────────────────────────────────┘
```

Esta modularidad garantiza que el estudiante nunca quede bloqueado si una empresa cambia sus términos de servicio o cancela una promoción comercial.

---

## 2. Instalación de OpenCode en la Terminal

OpenCode se distribuye como paquete global para el ecosistema Node.js / JavaScript.

### Paso 1: Verificación de Requisitos Previos

Comprueba que dispones de Node.js y npm en tu terminal Bash:

```bash
node --version
npm --version
```
*(Se recomienda Node.js 18 o superior).*

### Paso 2: Instalación Global

Instala OpenCode de forma global en tu máquina:

```bash
npm install -g opencode-ai
```

Verifica la correcta instalación comprobando su versión y comandos de ayuda:

```bash
opencode --version
opencode --help
```

---

## 3. Configuración de Proveedores Gratuitos sin Tarjeta de Crédito

Para comenzar a operar, ejecuta el asistente interactivo de configuración:

```bash
opencode setup
```

OpenCode te ofrecerá diversas alternativas de conexión. Veamos las tres opciones recomendadas para los estudiantes del ISFT N° 199:

### Opción 1: Nivel Gratuito Zen (Free Tier Comunitario)
* **Requisito:** Ninguno. Sin registro ni tarjeta de crédito.
* **Ventaja:** Funciona de inmediato al finalizar la instalación. Permite realizar consultas diarias para generar scripts, corregir errores de sintaxis y resolver dudas de laboratorio.
* **Configuración:** Selecciona *"OpenCode Zen (Community Free Tier)"* en el menú de setup.

### Opción 2: Clave Gratuita de Google AI Studio (Gemini Flash)
* **Requisito:** Cuenta de correo Google personal o educativa.
* **Ventaja:** Acceso a modelos avanzados de razonamiento rápido (Gemini Flash) con límites de hasta 15 peticiones por minuto totalmente gratis.
* **Configuración:**
  1. Ingresa a [Google AI Studio](https://aistudio.google.com/) y pulsa *"Get API Key"*.
  2. Crea una clave y cópiala en tu portapapeles.
  3. Configura la variable en tu sesión o en tu archivo `~/.bashrc`:
     ```bash
     export OPENCODE_API_KEY="tu-clave-de-aistudio"
     ```

### Opción 3: Inferencia 100% Local y Offline con Ollama
* **Requisito:** Computadora con CPU multinúcleo o tarjeta gráfica (mínimo 8 GB de RAM).
* **Ventaja:** Cero consumo de internet y privacidad total. Tus datos nunca salen de tu disco rígido.
* **Configuración:**
  1. Instala Ollama en tu sistema: `curl -fsSL https://ollama.com/install.sh | sh`
  2. Descarga un modelo especializado en código:
     ```bash
     ollama run qwen2.5-coder:7b
     ```
  3. En OpenCode setup, selecciona *"Local Ollama endpoint (http://localhost:11434)"*.

---

## 4. Modos de Ejecución y Comandos Esenciales

OpenCode admite dos modos de operación según la naturaleza de la tarea:

### Modo 1: Instrucción Rápida Directa (One-Shot CLI)
Ideal para tareas puntuales sin abrir una sesión interactiva:

```bash
opencode "Explica qué hace la función calcular_metricas en src/modelo.py"
```

### Modo 2: Sesión Interactiva con Contexto Acotado
Inicia un diálogo interactivo cargando únicamente los archivos necesarios:

```bash
opencode --context src/preprocesamiento.py
```

Dentro del prompt interactivo de OpenCode:
* `/help`: Muestra la lista de atajos y comandos disponibles.
* `/context add <archivo>`: Añade un archivo específico al espacio de trabajo del agente.
* `/context clear`: Limpia los archivos cargados para ahorrar tokens.
* `/diff`: Muestra el diff de los cambios propuestos antes de aplicarlos.
* `/exit` o `Ctrl+C`: Sale de la sesión interactiva.

---

## 5. Ejercicio de Verificación

Verifiquemos que OpenCode responde adecuadamente en tu terminal ejecutando una consulta simple de diagnóstico:

```bash
opencode "Indica tres diferencias técnicas fundamentales entre una tupla y una lista en Python 3.12."
```

Si el asistente retorna una respuesta estructurada y concisa en formato Markdown, tu entorno se encuentra 100% configurado y listo para trabajar.

En la siguiente lección, realizaremos un **taller práctico intensivo con OpenCode sobre el repositorio `energy-ml`**, detectando bugs reales de telemetría y creando pruebas unitarias.
