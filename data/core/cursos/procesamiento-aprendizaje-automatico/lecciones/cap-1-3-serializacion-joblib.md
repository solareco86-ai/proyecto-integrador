# Guía de Laboratorio — Lección 1.3: Serialización y Persistencia de Artefactos de ML con Joblib en energy-ml

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 1:** Arquitectura de Inferencia y Esquemas Pydantic  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado las Lecciones 1.1 y 1.2.

---

## 1. El Desacoplamiento Entre Entrenamiento e Inferencia

En un sistema industrial de Inteligencia Artificial como **`energy-ml`**, el ciclo de vida del aprendizaje automático consta de dos etapas completamente separadas en tiempo y arquitectura:

1. **Fase de Entrenamiento (Offline / Batch):** Se ejecuta periódicamente en servidores de cómputo dedicados, procesando meses de registros históricos de telemetría eléctrica para ajustar millones de parámetros numéricos.
2. **Fase de Inferencia (Online / Tiempo Real):** Se ejecuta en los servidores web de producción (FastAPI), respondiendo consultas en milisegundos para monitorear subestaciones activas.

Para conectar ambas etapas sin tener que reentrenar el modelo cada vez que se reinicia el servidor web, el estimador entrenado debe "congelarse" en disco mediante un proceso de **serialización binaria**.

---

## 2. ¿Por Qué `joblib` Sobre el Módulo `pickle` Estándar?

Aunque la biblioteca estándar de Python incluye el módulo `pickle` para serializar objetos arbitrarios, en la Ciencia de Datos moderna se utiliza **`joblib`**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   COMPARATIVA: PICKLE VS. JOBLIB                       │
├───────────────────────────────┬────────────────────────────────────────┤
│ pickle (Estándar de Python)   │ joblib (Optimizado para ML / NumPy)    │
├───────────────────────────────┼────────────────────────────────────────┤
│ • Serializa objetos genéricos.│ • Optimizado para grandes arrays       │
│ • Duplica datos en memoria    │   numéricos densos de NumPy.           │
│   durante la deserialización. │ • Utiliza mapeo directo de memoria     │
│ • Sin compresión integrada    │   (memory-mapping) sin duplicación.    │
│   para matrices numéricas.    │ • Soporta compresión nativa eficiente  │
│                               │   (zlib, gzip, lz4) en un solo archivo.│
└───────────────────────────────┴────────────────────────────────────────┘
```

---

## 3. El Antipatrón del Modelo Huérfano y la Prevención del *Schema Drift*

Un error muy extendido es guardar únicamente la instancia del estimador:
```python
# MALA PRÁCTICA: Guardar solo el modelo desnudo
joblib.dump(modelo_scikit, "modelo.joblib")
```

¿Qué ocurre tres meses después cuando un ingeniero actualiza el esquema de la base de datos y agrega una columna nueva o altera el orden de las variables? El modelo recibirá las columnas invertidas (por ejemplo, el voltaje en la posición de la corriente) sin emitir ningún error explícito, produciendo diagnósticos desastrosos. Este fenómeno se conoce como **desajuste de esquemas (*schema drift*)**.

### La Buena Práctica: El Diccionario de Artefacto Integral

En `energy-ml`, empaquetamos el modelo dentro de un contenedor estructurado que incluye **metadatos de trazabilidad y contratos de entrada**:

```python
artefacto = {
    "modelo": estimador_entrenado,
    "feature_names": [
        "voltaje_v",
        "corriente_a",
        "potencia_activa_kw",
        "temperatura_aceite_c",
        "frecuencia_hz"
    ],
    "version_pipeline": "2.0.0",
    "fecha_entrenamiento": "2026-10-03T22:00:00Z",
    "metricas_validacion": {
        "f1_score": 0.978,
        "precision": 0.981,
        "exactitud": 0.975
    }
}
```

---

## 4. Taller Práctico: Script de Entrenamiento y Persistencia

Navegamos a nuestro entorno de trabajo:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
```

Creamos el script de entrenamiento en `scripts/entrenar_modelo_transformador.py`:

```python
"""Script de entrenamiento y persistencia de artefacto para diagnóstico térmico."""

import os
import joblib
import numpy as np
from sklearn.naive_bayes import GaussianNB

def entrenar_y_persistir_artefacto():
    print("1. Generando datos de calibración histórica de transformadores...")
    # Features: [voltaje_v, corriente_a, potencia_kw, temp_aceite_c, frecuencia_hz]
    X_train = np.array([
        # Casos normales (temperatura baja/media, potencia normal)
        [220.0, 35.0, 7.7, 55.0, 50.0],
        [218.5, 40.0, 8.7, 60.0, 49.9],
        [222.0, 30.0, 6.6, 52.0, 50.1],
        # Casos de advertencia térmica
        [215.0, 65.0, 14.0, 85.0, 49.8],
        [217.0, 70.0, 15.2, 88.0, 50.0],
        # Casos de falla crítica (alta temperatura + sobrecarga)
        [205.0, 110.0, 22.5, 112.0, 49.2],
        [208.0, 115.0, 23.9, 115.0, 49.3],
    ])
    
    y_train = np.array([
        "normal", "normal", "normal",
        "advertencia", "advertencia",
        "falla_critica", "falla_critica"
    ])

    print("2. Ajustando modelo probabilístico GaussianNB...")
    estimador = GaussianNB()
    estimador.fit(X_train, y_train)

    print("3. Empaquetando artefacto con metadatos de gobernanza...")
    nombres_features = [
        "voltaje_v",
        "corriente_a",
        "potencia_activa_kw",
        "temperatura_aceite_c",
        "frecuencia_hz"
    ]

    artefacto = {
        "modelo": estimador,
        "feature_names": nombres_features,
        "version_pipeline": "2.0.0",
        "clases": list(estimador.classes_)
    }

    os.makedirs("modelos", exist_ok=True)
    ruta_salida = "modelos/clasificador_transformador.joblib"

    print(f"4. Persistiendo artefacto comprimido en {ruta_salida}...")
    # Compresión zlib nivel 3: óptimo balance entre tamaño y velocidad de descompresión
    joblib.dump(artefacto, ruta_salida, compress=("zlib", 3))
    print("¡Artefacto generado y guardado exitosamente!")

if __name__ == "__main__":
    entrenar_y_persistir_artefacto()
```

Ejecutamos el entrenamiento en la terminal:

```bash
python scripts/entrenar_modelo_transformador.py
```

---

## 5. Verificación de Carga y Validación de Esquema en la API

Comprobamos que el artefacto puede cargarse y que sus variables coinciden exactamente con las esperadas:

```python
import joblib

# Cargamos el archivo en memoria
artefacto_cargado = joblib.load("modelos/clasificador_transformador.joblib")

# Verificamos la integridad de las features
features_requeridas = [
    "voltaje_v", "corriente_a", "potencia_activa_kw",
    "temperatura_aceite_c", "frecuencia_hz"
]

assert artefacto_cargado["feature_names"] == features_requeridas, "¡Error de desajuste de esquema (Schema Drift)!"

# Inferencia de prueba
modelo = artefacto_cargado["modelo"]
lectura_prueba = [[210.0, 105.0, 22.0, 110.0, 49.5]]
pred = modelo.predict(lectura_prueba)
print(f"Resultado del diagnóstico: {pred[0]}")  # Imprime: falla_critica
```

---

## 6. Pruebas Automatizadas con Pytest

Creamos `tests/test_serializacion.py`:

```python
"""Pruebas unitarias de integridad de artefactos serializados."""

import os
import joblib

def test_artefacto_transformador_valido():
    ruta = "modelos/clasificador_transformador.joblib"
    assert os.path.exists(ruta), "El archivo de modelo no existe."
    
    artefacto = joblib.load(ruta)
    assert "modelo" in artefacto
    assert "feature_names" in artefacto
    assert len(artefacto["feature_names"]) == 5
    assert hasattr(artefacto["modelo"], "predict")
```

Ejecutamos las pruebas locales:

```bash
pytest tests/test_serializacion.py -v
```

---

## 7. Conclusión del Capítulo 1 de la Unidad 2

Has completado la arquitectura base de inferencia en producción:
1. Contratos de entrada y validación estricta con **Pydantic** para blindar al sistema de datos corruptos.
2. Gestión de memoria de alto rendimiento mediante el gestor **`lifespan`** de FastAPI, logrando inferencias en <2ms.
3. Persistencia profesional de artefactos de Machine Learning con **`joblib`**, incluyendo metadatos de gobernanza para erradicar el *schema drift*.

En el **Capítulo 2**, profundizaremos en los fundamentos teóricos del aprendizaje supervisado: **Deducción vs. Inducción**, partición rigurosa de datos (Train/Test) y prevención de fugas de información (*data leakage*) sobre telemetría de redes eléctricas.
---

## Autoevaluación Formativa y Caza de Código Alucinado

### Preguntas de Razonamiento Conceptual
1. ¿Cuál es el riesgo de seguridad crítico si deserializas un archivo `.joblib` de una fuente no confiable?
2. ¿Qué diferencia hay entre guardar un modelo con `joblib.dump()` versus `.pickle()` en cuanto a reproducibilidad entre versiones de Python?

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente código generado por un asistente de IA:

```python
# CÓDIGO CON BUG DE SEGURIDAD GENERADO POR IA:
import joblib
import os

# IA generó esto, sin validar la ruta
archivo_modelo = os.environ.get("MODELO_PATH", "/tmp/modelo.joblib")
modelo = joblib.load(archivo_modelo)  # ¡Puede cargar código arbitrario!

# Si un atacante controla MODELO_PATH, puede ejecutar código
```

**Diagnóstico del Revisor Humano:**
1. **Vulnerabilidad de Desserialización:** `joblib.load()` puede ejecutar código Python arbitrario.
2. **Falta de Validación de Rutas:** No verifica que la ruta sea confiable.
3. **Corrección Obligatoria en energy-ml:**
   ```python
   import joblib
   from pathlib import Path

   # Rutas autorizadas solo del proyecto
   RUTA_SEGURA = Path(__file__).parent / "modelos" / "knn_classifier.joblib"

   if not RUTA_SEGURA.exists():
       raise FileNotFoundError(f"Modelo no encontrado en {RUTA_SEGURA}")

   modelo = joblib.load(RUTA_SEGURA)
   ```

---
