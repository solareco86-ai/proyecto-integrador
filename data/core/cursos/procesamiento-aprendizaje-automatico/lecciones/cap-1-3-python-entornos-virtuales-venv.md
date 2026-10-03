# Guía de Laboratorio Práctico — Capítulo 1: La Terminal y el Entorno de Desarrollo Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## 3. Sección 1.3: Aislamiento de Dependencias con Python 3 (`venv` y `pip`)

### 3.1. Conceptos Clave
* **¿Por qué aislar entornos?** Evita conflictos entre versiones de librerías instaladas globalmente en el sistema operativo. Cada proyecto mantiene su propio árbol de dependencias aislado.
* **Entorno Virtual (`venv`):** Carpeta autocontenida que aloja una copia ligera del ejecutable de Python y sus paquetes instalados.

### 3.2. Paso a Paso: Configuración del Entorno Virtual

```bash
# 1. Asegurar estar en la raíz del proyecto (laboratorio_cap1)
pwd

# 2. Crear el entorno virtual llamado 'venv'
python3 -m venv venv

# 3. Activar el entorno virtual
# En Linux / macOS:
source venv/bin/activate

# En Windows (Git Bash o CMD):
# source venv/Scripts/activate

# 4. Comprobar que el intérprete apunta al entorno virtual
which python3   # En Linux/macOS
# where python  # En Windows

# 5. Actualizar pip e instalar dependencias necesarias
pip install --upgrade pip
pip install python-dotenv requests

# 6. Congelar las dependencias instaladas en requirements.txt
pip freeze > requirements.txt
cat requirements.txt
```
