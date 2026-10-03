# Guía de Laboratorio Práctico — Capítulo 1: La Terminal, Git y el Entorno de Trabajo en Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## 1. Objetivos de Aprendizaje y Competencias

Al finalizar este laboratorio, el estudiante será capaz de:
1. Comprender la necesidad de aislar dependencias de Python en proyectos de Machine Learning.
2. Crear y activar un entorno virtual (`venv`) dentro del repositorio oficial clonado (`energy-ml`).
3. Administrar paquetes con `pip` e instalar el manifiesto de dependencias real (`requirements.txt`).
4. Comprobar que el intérprete de Python y las herramientas instaladas apuntan exclusivamente al entorno local del proyecto.

---

## 2. Sección 1.4: Aislamiento de Dependencias con Python 3 (`venv` y `pip`) sobre `energy-ml`

### 2.1. Conceptos Clave
* **¿Por qué aislar entornos?** Cada proyecto de Machine Learning requiere versiones específicas de librerías (como NumPy, Scikit-Learn o FastAPI). Instalar paquetes globalmente en el sistema operativo puede generar conflictos de versiones catastróficos entre distintos cursos o aplicaciones.
* **Entorno Virtual (`venv`):** Directorio autocontenido dentro de la carpeta del proyecto que aloja una copia aislada del ejecutable de Python, los binarios de `pip` y la carpeta `site-packages` donde residen las dependencias instaladas.
* **El archivo `requirements.txt`:** Contrato formal que enumera todas las bibliotecas de las cuales depende el proyecto `energy-ml` para operar correctamente.

---

### 2.2. Paso a Paso: Creación e Instalación en `energy-ml`

#### Paso 1: Confirmar ubicación en la raíz de `energy-ml`
Asegúrate de estar posicionado en la raíz del repositorio clonado en la lección 1.3:

```bash
pwd
# La salida debe terminar en .../aprendizaje-automatico/energy-ml
```

#### Paso 2: Crear el Entorno Virtual (`venv`)
Ejecuta el módulo `venv` de Python 3 para generar una nueva carpeta llamada `venv`:

```bash
python3 -m venv venv
```

Si estás en Windows (Git Bash) y `python3` no es reconocido, utiliza:
```bash
python -m venv venv
```

#### Paso 3: Activar el Entorno Virtual
La activación redirige las variables de entorno de tu terminal (`$PATH`) para que el comando `python` apunte al entorno recién creado.

* **En GNU/Linux Nativo o WSL 2:**
  ```bash
  source venv/bin/activate
  ```
* **En Windows con Git Bash:**
  ```bash
  source venv/Scripts/activate
  ```

*(Observarás que el indicador o prompt de tu terminal ahora comienza con `(venv)`, confirmando que el entorno está activo).*

#### Paso 4: Comprobar el Intérprete Activo
Comprueba que el ejecutable de Python proviene de tu carpeta local y no de la instalación global:

```bash
which python3 || which python
# Salida esperada: .../energy-ml/venv/bin/python (o venv/Scripts/python)
```

#### Paso 5: Actualizar pip e Instalar Dependencias de `energy-ml`
Con el entorno virtual activado, actualiza el gestor de paquetes e instala las dependencias reales del caso de estudio:

```bash
# 1. Actualizar el gestor de paquetes pip
pip install --upgrade pip

# 2. Instalar todas las dependencias del proyecto especificadas en requirements.txt
pip install -r requirements.txt
```

#### Paso 6: Inspeccionar las Librerías Instaladas
Verifica que las librerías científicas y web quedaron correctamente instaladas en tu entorno:

```bash
pip list
```

Observarás paquetes clave del curso como `fastapi`, `uvicorn`, `scikit-learn`, `pydantic` y `pytest`.

---

### 2.3. Interacción con Git: ¿Por qué `venv/` no se sube al repositorio?

Ejecuta el comando de estado de Git:

```bash
git status
```

Notarás que la carpeta `venv/` **no aparece** en la lista de archivos por añadir (*Untracked files*). Esto se debe a que el archivo `.gitignore` del proyecto contiene la regla `venv/`.

> [!IMPORTANT]
> **Regla de oro:** Nunca se versionan entornos virtuales en Git. Los entornos son específicos de la máquina y arquitectura de cada desarrollador. El código se comparte a través de Git y las dependencias se reproducen mediante `pip install -r requirements.txt`.

---

## 3. Checkpoint de Verificación

Antes de avanzar a la configuración de variables de entorno (`.env`):
- [ ] Tu prompt de terminal muestra el prefijo `(venv)`.
- [ ] El comando `which python` (o `which python3`) apunta al ejecutable dentro de `energy-ml/venv/`.
- [ ] `pip list` incluye `fastapi` y `scikit-learn`.
- [ ] Al ejecutar `git status`, la carpeta `venv/` es ignorada correctamente.
