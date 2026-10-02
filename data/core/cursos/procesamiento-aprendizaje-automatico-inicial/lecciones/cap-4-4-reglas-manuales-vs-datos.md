# Guía de Laboratorio: Capítulo 4 - De Script de Consola a Servicio Web con FastAPI

**Trayecto Formativo:** Procesamiento y Aprendizaje Automático (Nivel 0 — Nivelación)  
**Slug:** `procesamiento-aprendizaje-automatico-inicial`  
**Carga Horaria:** 5 horas (Práctica y Evaluación)  

---

## 5. Ejercicio 4.3: De Reglas Manuales a Decisiones Basadas en Datos

Para comprender la diferencia fundamental entre programación tradicional (reglas fijas) y aprendizaje automático (decisiones basadas en ejemplos):

### 1. Enfoque Rígido (Reglas Cableadas)
```python
def clasificar_riesgo_manual(edad: int, ingresos: float) -> str:
    # Reglas if/else construidas manualmente por el programador
    if edad < 25 and ingresos < 30000:
        return "alto"
    elif edad >= 25 and ingresos >= 30000:
        return "bajo"
    return "medio"
```

### 2. Enfoque Guiado por Datos (Listado de Ejemplos / Búsqueda por Similitud Básica)
```python
# Conjunto de datos histórico (ejemplos etiquetados)
EJEMPLOS_HISTORICOS = [
    {"edad": 20, "ingresos": 20000, "categoria": "alto"},
    {"edad": 22, "ingresos": 25000, "categoria": "alto"},
    {"edad": 40, "ingresos": 60000, "categoria": "bajo"},
    {"edad": 50, "ingresos": 80000, "categoria": "bajo"},
    {"edad": 30, "ingresos": 35000, "categoria": "medio"},
]

def clasificar_por_ejemplos(edad: int, ingresos: float) -> str:
    """Encuentra el ejemplo más cercano en los datos históricos (distancia Manhattan simple)."""
    def calcular_distancia(ejemplo):
        return abs(ejemplo["edad"] - edad) + abs(ejemplo["ingresos"] - ingresos) / 1000

    ejemplo_mas_cercano = min(EJEMPLOS_HISTORICOS, key=calcular_distancia)
    return ejemplo_mas_cercano["categoria"]
```

### 3. Endpoint `POST /clasificar` en FastAPI para Comparar Ambos Enfoques
```python
from pydantic import BaseModel

class EvaluacionRequest(BaseModel):
    edad: int
    ingresos: float

@app.post("/clasificar")
def comparar_clasificacion(datos: EvaluacionRequest):
    resultado_manual = clasificar_riesgo_manual(datos.edad, datos.ingresos)
    resultado_datos = clasificar_por_ejemplos(datos.edad, datos.ingresos)
    
    return {
        "entrada": {"edad": datos.edad, "ingresos": datos.ingresos},
        "resultado_reglas_manuales": resultado_manual,
        "resultado_basado_en_ejemplos": resultado_datos
    }
```

---

## 6. Auditoría y Control de Versiones con Git

Aplica la metodología de auditoría aprendida en el Capítulo 2 antes de confirmar tus cambios:

1. Revisa el estado de tus archivos:
   ```bash
   git status
   ```

2. Audita los cambios generados con **OpenCode**:
   ```bash
   git diff main.py
   ```

3. Realiza Staging selectivo:
   ```bash
   git add -p main.py
   ```

4. Realiza el commit descriptivo:
   ```bash
   git commit -m "feat(api): implementa endpoints /operar y /clasificar con FastAPI y Pydantic"
   ```

---

## 7. Rúbrica de Evaluación del Laboratorio

| Criterio | Excelente (100%) | Satisfactorio (75%) | Requiere Mejora (50%) | No Aprobado (0%) |
| :--- | :--- | :--- | :--- | :--- |
| **Despliegue e Interfaz Swagger** | Servidor Uvicorn operativo; interfaz Swagger (`/docs`) interactiva y sin errores. | Servidor levanta pero presenta errores menores en Swagger. | Requiere ayuda docente para levantar Uvicorn. | No logra ejecutar el servidor web. |
| **Endpoint `POST /operar`** | Implementado con tipos Pydantic, validación de errores (división por cero) y soporte de OpenCode. | Funciona pero carece de manejo explícito de excepciones HTTP. | Endpoint básico sin validación de Pydantic ni tipos. | No implementa el endpoint `POST /operar`. |
| **Comparación Reglas vs. Datos** | Endpoint `/clasificar` demuestra claramente ambas aproximaciones con código limpio. | Implementa la comparación pero sin explicar las diferencias conceptuales. | Funciona parcialmente o sólo incluye la lógica `if/else`. | No realiza el ejercicio de comparación. |
| **Auditoría Git** | Uso estricto de `git diff` y `git add -p` con mensajes de commit estructurados. | Realiza commit directo con `git add .` sin auditar diferencias. | Historial de Git desorganizado o incompleto. | No utiliza Git para gestionar los cambios. |
