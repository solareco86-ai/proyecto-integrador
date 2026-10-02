# Guía de Laboratorio — Capítulo 3: La Tríada de Asistentes (Aider, OpenCode y AGY CLI)

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga horaria estimada:** 2.5 horas  

---

## 2. Anatomía de una Instrucción Técnica (Prompting de Ingeniería)

Para obtener código robusto y determinístico de un agente de desarrollo, la instrucción debe formularse delimitando con precisión el alcance y las restricciones del problema:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   ANATOMÍA DE UNA INSTRUCCIÓN TÉCNICA                  │
├─────────────────┬──────────────────────────────────────────────────────┤
│ 1. Contexto     │ Archivos específicos o funciones sobre las que actuar│
│ 2. Objetivo     │ Tarea concreta (crear, refactorizar, explicar, fix) │
│ 3. Restricciones│ Reglas (Type Hints, manejo de excepciones, no deps) │
│ 4. Criterio     │ Cómo debe comportarse o probarse el resultado        │
└─────────────────┴──────────────────────────────────────────────────────┘
```

**Ejemplo de mala instrucción:**  
> *"Hazme un script que lea logs y me diga si hay errores."*  
*(Es vago, no impone restricciones, genera código desestructurado y sin tipado).*

**Ejemplo de buena instrucción técnica:**  
> *"Crea en `analizador_logs.py` la función `filtrar_errores(lineas: list[str]) -> dict`. Debe filtrar líneas con 'ERROR' o 'CRITICAL' usando expresiones regulares. Retorna un diccionario con los conteos. No uses librerías externas."*

---

## 3. Práctica: Generación y Auditoría con Aider

### Tarea 3.1: Iniciar Aider acotando el contexto
Para evitar que la IA cargue archivos innecesarios o alucine, inicia Aider especificando solo el archivo objetivo:

```bash
aider analizador_logs.py
```
*(Aider creará el archivo en caso de que no exista y lo agregará al contexto de trabajo).*

### Tarea 3.2: Petición de Creación Inicial (Generación con Restricciones)
Ingresa la siguiente instrucción técnica en la consola de Aider:

> **Prompt 1:**  
> *"Crea una función `cargar_logs(ruta: str) -> list[str]` en `analizador_logs.py`. Debe abrir el archivo indicado por `ruta`, leer las líneas y retornarlas en una lista. Incluye Type Hints, docstring y manejo de la excepción `FileNotFoundError` informando un mensaje claro por consola."*

### Acción Obligatoria de Auditoría:
Sal de Aider con `/quit` o abre una segunda pestaña de terminal para inspeccionar el cambio antes de continuar:

```bash
git diff
```
Verifica que el agente no haya introducido imports ajenos ni lógica fuera de la solicitada.
