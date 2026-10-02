# Guía de Laboratorio Práctico — Capítulo 1: La Terminal y el Entorno de Desarrollo Python

**Módulo:** Procesamiento y Aprendizaje Automático Inicial (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga del Capítulo:** 5 horas (de 20 hs totales)

---

## 4. Sección 1.3: Variables de Entorno y Protección de Credenciales (`.env`)

### 4.1. Conceptos Clave
* **Variables de Entorno:** Paredes de memoria que almacenan configuraciones sensibles (como llaves de API o contraseñas de bases de datos) fuera del código fuente.
* **Resguardo de Credenciales:** La regla de oro del desarrollo profesional es **nunca hardcodear API keys en el código** ni subirlas a repositorios públicos o privados de Git.

### 4.2. Configuración del Archivo `.gitignore`
Abre el archivo `.gitignore` y añade las siguientes líneas para asegurarte de no subir el entorno virtual ni tus credenciales reales:

```gitignore
# Entorno virtual
venv/

# Variables de entorno con credenciales sensibles
.env

# Caché de Python
__pycache__/
*.pyc
```

### 4.3. Configuración de Plantillas y Variables
1. **Crear la plantilla pública (`.env.example`):**
   ```bash
   echo 'API_KEY="tu_api_key_aqui"' > .env.example
   ```

2. **Crear el archivo privado real (`.env`):**
   ```bash
   echo 'API_KEY="sk-lab-123456789-secret"' > .env
   ```

### 4.4. Ejercicio de Código: Lectura de Variables en Python
Abre el archivo `src/main.py` e incluye la siguiente lógica de verificación:

```python
import os
from dotenv import load_dotenv

def cargar_configuracion():
    # Cargar variables desde el archivo .env
    load_dotenv()
    
    api_key = os.getenv("API_KEY")
    
    if not api_key or api_key == "tu_api_key_aqui":
        print("❌ Error: API_KEY no configurada correctamente en el archivo .env")
        return False
    
    print("✅ Configuración cargada exitosamente.")
    print(f"🔑 API_KEY detectada (Longitud: {len(api_key)} caracteres)")
    return True

if __name__ == "__main__":
    cargar_configuracion()
```

### 4.5. Ejecución y Validación
Ejecuta el script desde la terminal con el entorno virtual activado:

```bash
python src/main.py
```

---

## 5. Checkpoint de Auditoría y Control de Calidad

Antes de considerar completado este laboratorio, verifica:
- [ ] El entorno virtual `venv` está activado (`(venv)` aparece en el prompt de la consola).
- [ ] El archivo `.gitignore` incluye explícitamente `venv/` y `.env`.
- [ ] El comando `ls -la` muestra los archivos `.env` y `.env.example`.
- [ ] La ejecución de `python src/main.py` lee correctamente la variable de entorno sin mostrar errores.
