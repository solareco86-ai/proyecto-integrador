# Guía de Laboratorio — Lección 3.2: OpenCode: Instalación, Proveedores Gratuitos y Configuración sin Tarjeta

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 3:** Asistentes de IA para Estudiantes: OpenCode y Antigravity CLI  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 3.1 (Economía de la IA Agéntica).

---

## 1. ¿Qué es OpenCode y Cómo Funciona?

**OpenCode** es una herramienta de asistencia en desarrollo de software construida desde cero bajo la filosofía del **software libre**. A diferencia de extensiones cerradas de editores comerciales, OpenCode se ejecuta de forma nativa en la terminal Bash y desacopla la interfaz del proveedor de inteligencia artificial:

```text
┌────────────────────────────────────────────────────────────────────┐
│                ARQUITECTURA MODULAR DE OPENCODE                    │
├────────────────────────────────────────────────────────────────────┤
│  Terminal Bash ──► OpenCode Engine (Lectura de archivos)           │
│                              │                                     │
│                  ┌───────────┴───────────┐                         │
│                  ▼                       ▼                         │
│        Zen / Free Tier          Ollama Local                       │
│        (Créditos $0)            (100% Offline)                     │
└────────────────────────────────────────────────────────────────────┘
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

OpenCode te ofrecerá diversas alternativas de conexión. Veamos las dos opciones recomendadas para los estudiantes del ISFT N° 199:

### Opción 1: Nivel Gratuito Zen (Free Tier Comunitario)
* **Requisito:** Ninguno. Sin registro ni tarjeta de crédito.
* **Ventaja:** Funciona de inmediato al finalizar la instalación. Permite realizar consultas diarias para generar scripts, corregir errores de sintaxis y resolver dudas de laboratorio.
* **Configuración:** Selecciona *"OpenCode Zen (Community Free Tier)"* en el menú de setup.

### Opción 2: Inferencia 100% Local y Offline con Ollama
* **Requisito:** 8 GB de RAM para ejecutar en CPU (más lento). Para trabajar con modelos grandes se recomienda una tarjeta gráfica con **24 GB de VRAM**. Es posible experimentar desde **2 GB de VRAM** con modelos pequeños. Antes de elegir un modelo, revisa la lección 3.1b.
* **Ventaja:** Cero consumo de internet y privacidad total. Tus datos nunca salen de tu disco rígido.
**Configuración:**

**Paso 1:** Instala Ollama en tu sistema:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

**Paso 2:** Descarga un modelo especializado en código:

```bash
ollama run qwen2.5-coder:7b
```

> [!NOTE]
> Si tu equipo tiene poca memoria (2 GB de VRAM o menos), usa un modelo más pequeño, por ejemplo `ollama run qwen2.5-coder:1.5b`. Las respuestas serán más simples, pero el flujo de trabajo es el mismo.

**Paso 3:** En OpenCode setup, selecciona *"Local Ollama endpoint (http://localhost:11434)"*.

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
