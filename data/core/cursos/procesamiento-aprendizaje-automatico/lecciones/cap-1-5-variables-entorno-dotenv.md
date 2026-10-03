# Guía de Laboratorio Práctico — Capítulo 1: La Terminal y el Entorno de Desarrollo Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## 1. Objetivos de Aprendizaje y Competencias

Al finalizar este laboratorio, el estudiante será capaz de:
1. Comprender la función crítica de las variables de entorno en la configuración de proyectos de Machine Learning.
2. Gestionar la separación entre plantillas públicas (`.env.example`) y credenciales locales privadas (`.env`).
3. Verificar la protección de secretos mediante las reglas de exclusión de `.gitignore`.
4. Ejecutar la validación inicial del caso de estudio `energy-ml` con `pytest` para confirmar el funcionamiento integral del entorno.

---

## 2. Sección 1.5: Variables de Entorno (`.env`), Resguardo de Credenciales y Verificación de `energy-ml`

### 2.1. Conceptos Clave: El Principio de Secreto y Configuración

En proyectos profesionales de Inteligencia Artificial y Machine Learning:
* **Separación de Código y Configuración:** Las rutas a bases de datos, llaves de API (OpenAI, Anthropic, Gemini), puertos de servidores y modos de depuración varían entre la computadora del alumno y el servidor de producción. Nunca deben escribirse fijas en el código fuente.
* **La Tríada de Archivos:**
  1. `.env.example`: Archivo público versionado en Git que documenta qué variables necesita el proyecto, usando valores de ejemplo vacíos.
  2. `.env`: Archivo local privado que contiene los valores reales. **Nunca se sube a Git**.
  3. `.gitignore`: Archivo de texto que le indica a Git qué archivos ignorar permanentemente para no filtrar secretos ni binarios pesados.

---

### 2.2. Paso a Paso: Configuración de Variables en `energy-ml`

#### Paso 1: Inspeccionar la protección en `.gitignore`
Antes de crear cualquier archivo con secretos, verifica que el `.gitignore` de `energy-ml` contenga las reglas de protección:

```bash
# Comprobar que venv y .env están protegidos
grep -E "(venv|\.env)" .gitignore
```

Observarás que tanto `.env` como `venv/` están declarados para ser ignorados por Git.

#### Paso 2: Crear el Archivo `.env` desde la Plantilla
Copia la plantilla oficial `.env.example` para generar tu archivo de configuración local:

```bash
cp .env.example .env
```

#### Paso 3: Auditoría con `git status`
Comprueba que Git no rastrea tu nuevo archivo `.env`:

```bash
git status
```

Git debe informar `nothing to commit, working tree clean` (o no listar el archivo `.env`). Si `.env` apareciera como archivo no rastreado (*Untracked*), significaría que el `.gitignore` no está funcionando.

#### Paso 4: Inspeccionar la Configuración Local
Visualiza las variables definidas para el proyecto `energy-ml`:

```bash
cat .env
```

Encontrarás configuraciones para el entorno de desarrollo, el puerto del servidor (`PORT=8000`), el nivel de logging y las rutas de almacenamiento de datos.

---

### 2.3. Verificación Final: Ejecución de Pruebas de `energy-ml`

Para comprobar que la terminal, Git, Python 3, el entorno virtual `venv`, las dependencias de `requirements.txt` y la configuración `.env` están perfectamente articulados, ejecuta la suite de pruebas del proyecto:

```bash
# Ejecutar las pruebas unitarias con pytest
pytest -q
```

Verás una salida confirmando que los tests de dominio, aplicación e inferencia pasaron exitosamente:

```text
........                                                         [100%]
8 passed in 0.42s
```

¡Felicitaciones! Has completado el circuito de desarrollo profesional: desde la consola del sistema operativo hasta la ejecución de un caso de estudio real de Machine Learning con control de versiones y dependencias aisladas.

---

## 3. Checkpoint de Auditoría del Capítulo 1

Antes de comenzar el Capítulo 2 (Trabajo con Agentes de Código), confirma:
- [ ] Tu terminal está posicionada en `aprendizaje-automatico/energy-ml/`.
- [ ] El entorno virtual `venv` está activado (`(venv)` visible en el prompt).
- [ ] El archivo `.env` existe en la raíz de `energy-ml/`.
- [ ] `git status` no muestra archivos no deseados ni secretos expuestos.
- [ ] La ejecución de `pytest -q` corre satisfactoriamente sin errores.
