# 3.2 Evaluación de tecnologías: OCR, NLP, ML, frameworks

## Objetivo

Decidir CUÁNDO y POR QUÉ usar OCR, NLP, ML. No es "todo sirve", es "esto resuelve este problema".

## Contenidos

### 1. Matriz de Alternativas

```yaml
# Problema: Extraer datos de facturas

Opción A: OCR (Tesseract) + Regex
  Ventajas:
    - Rápido, bajo costo
    - Determinístico (reglas claras)
  Desventajas:
    - Frágil con formatos nuevos
    - No aprende

Opción B: ML + Vision (Keras, TensorFlow)
  Ventajas:
    - Adaptable a variaciones
    - Puede aprender de ejemplos
  Desventajas:
    - Requiere dataset de entrenamiento
    - Más lento

Opción C: API externa (Google Vision, AWS Textract)
  Ventajas:
    - Muy preciso
  Desventajas:
    - Costo por API
    - Dependencia externa

Recomendación para ISFT: Opción A (OCR + Regex)
  Razón: Facturas siguen patrón, OCR es suficiente
         Guardar ML para análisis de patrones después
```

### 2. Cuándo usar qué (spec guidance)

```
OCR (Procesamiento Digital Imágenes, 3er año):
  ✓ Cuando: Extraer texto de documentos
  ✗ No: No es ML, no aprende

NLP (Procesamiento del Habla, 2do año):
  ✓ Cuando: Bot conversacional, análisis de sentimiento
  ✗ No: Extracción simple de datos

ML (PAA, 3er año):
  ✓ Cuando: Predicción, patrones complejos, clasificación
  ✗ No: Reglas simples (usa if/else)

API REST:
  ✓ Cuando: Necesitas escalabilidad externa
  ✗ No: Si puedes resolverlo localmente
```

### 3. Decisión para cada Proyecto

```yaml
# Energético

Lectura sensores: API MQTT (no ML, es ingesta pura)
Predicción consumo: ML (PAA) ← sí, aquí hay patrón
Bot consultas: NLP (2do año) + reglas básicas
OCR facturas: Tesseract + Regex (3er año technique)

# Institucional

Listado carreras: BD + REST API (no need ML)
Bot orientación: NLP (2do año)
Recomendador: ML (PAA) si hay datos históricos
OCR documentos: OCR (3er año) si necesario
```

## Actividad Práctica

Para tu proyecto:
1. Listar cada funcionalidad
2. Decidir: ¿Necesita OCR? ¿NLP? ¿ML? ¿Plain code?
3. Justificar por qué

## Palabras clave

Evaluación, alternativas, OCR, NLP, ML, decisión tecnológica

