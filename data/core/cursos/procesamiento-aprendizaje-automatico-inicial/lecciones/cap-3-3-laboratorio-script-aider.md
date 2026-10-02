# Guía de Laboratorio — Capítulo 3: La Tríada de Asistentes (Aider, OpenCode y AGY CLI)

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga horaria estimada:** 2.5 horas  

---

## 3. Práctica: Refactorización, Explicación y Bloque Main

### Tarea 3.3: Petición de Refactorización y Explicación
Vuelve a ingresar a Aider o continúa la sesión interactiva:

> **Prompt 2 (Refactor):**  
> *"Agrega la función `procesar_eventos(lineas: list[str]) -> dict[str, int]`. Esta función debe recorrer cada línea y contar la frecuencia de los niveles `[INFO]`, `[WARNING]`, `[ERROR]` y `[CRITICAL]`. Utiliza el módulo estándar `re` (expresiones regulares)."*

> **Prompt 3 (Explicación de Código):**  
> *"Explica paso a paso la expresión regular que utilizaste en `procesar_eventos` y aclara si existe algún caso borde que pueda romper la función."*

### Tarea 3.4: Construcción del Bloque Principal (`main`)
> **Prompt 4:**  
> *"Agrega un bloque `if __name__ == '__main__':` que ejecute el pipeline: cargue `app.log`, procese los eventos e imprima el diccionario resultante en formato JSON formateado (`json.dumps` con sangría de 2 espacios)."*

---

## 4. Verificación, Auditoría Final y Desafíos

### Paso 4: Verificación y Auditoría Final

1. Ejecuta el script utilitario generado por Aider:
   ```bash
   python analizador_logs.py
   ```

2. **Resultado esperado por consola:**
   ```json
   {
     "INFO": 2,
     "WARNING": 1,
     "ERROR": 2,
     "CRITICAL": 1
   }
   ```

3. Audita la totalidad del trabajo realizado con Git:
   ```bash
   git status
   git log --oneline
   git diff HEAD~1
   ```

---

## 5. Ejercicios Desafío

1. **Ampliación de Funcionalidad (OpenCode / Aider):** Solicita al asistente agregar soporte para argumentos de línea de comandos usando `argparse`, permitiendo ejecutar:
   ```bash
   python analizador_logs.py --archivo app.log --salida resumen.json
   ```
2. **Auditoría de Inseguridad:** Pide al asistente que agregue una función para enviar el resumen a un servidor web remoto. Audita la sugerencia para confirmar que no incluya URLs ni credenciales de prueba en duro.

---

## 6. Rúbrica de Evaluación

| Criterio | Logrado (100%) | En Proceso (50%) | No Logrado (0%) |
| :--- | :--- | :--- | :--- |
| **Instalación y Configuración** | Herramientas instaladas y operativas en el `venv` con variables de entorno validadas. | Herramientas instaladas pero con errores en la carga de variables. | No logró instalar ni configurar el entorno virtual. |
| **Calidad de Prompting** | Estructura la instrucción técnica con contexto, tarea, restricciones y Type Hints. | Prompt ambiguo o vago que requiere múltiples iteraciones para corregir. | Copia prompts genéricos sin adaptar restricciones ni contexto. |
| **Auditoría de Cambios** | Verifica con `git diff` cada cambio del agente antes de realizar el commit final. | Acepta cambios del agente a ciegas y solo revisa al finalizar. | No utiliza Git para auditar los cambios generados por la IA. |
| **Ejecución del Script** | `analizador_logs.py` procesa correctamente el log y emite JSON estructurado. | El script funciona parcialmente o tiene errores en casos borde. | El script no ejecuta o genera sintaxis errónea. |
