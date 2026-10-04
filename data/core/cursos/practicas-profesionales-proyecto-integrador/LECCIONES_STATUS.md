# Estado de Lecciones - Prácticas Profesionales: Proyecto Integrador

## Resumen
- **Total de lecciones planificadas:** 26 lecciones + 5 talleres
- **Lecciones completadas:** 3 / 26 (11.5%)
- **Lecciones con estructura (placeholders):** 31 / 31 (100%)
- **Talleres completados:** 0 / 5 (0%)
- **Última actualización:** 2026-10-04 (sesión 2)

---

## Unidad 1: Procesamiento de Datos (8 lecciones + 1 taller)

### Cap 1: Ingesta y Exploración de Datos (3 lecciones)
- [x] **1.1** `cap-1-1-ingesta-fuentes.md` - Fuentes de datos: sensores, logs, APIs
- [x] **1.2** `cap-1-2-exploracion-pandas.md` - Exploración con Pandas
- [ ] **1.3** `cap-1-3-visualizacion-exploracion.md` - Visualización exploratoria (30 min)
  - Histogramas, boxplots, scatter plots con Matplotlib/Seaborn
  - Detección visual de outliers y patrones
  - Correlaciones entre variables

### Cap 2: Limpieza y Preprocesamiento (3 lecciones)
- [ ] **2.1** `cap-2-1-valores-faltantes.md` - Valores faltantes (40 min)
  - Detección, imputación (media, mediana, forward fill)
  - Eliminación segura de filas/columnas
  - Estrategias por tipo de datos
  
- [ ] **2.2** `cap-2-2-outliers-validacion.md` - Outliers y validación (35 min)
  - Métodos: IQR, Z-score, Isolation Forest
  - Validación de rangos esperados
  - Decisión: mantener, eliminar, o transformar
  
- [ ] **2.3** `cap-2-3-normalizacion-escalado.md` - Normalización (35 min)
  - StandardScaler, MinMaxScaler, RobustScaler
  - Log transform para datos sesgados
  - Importancia para ML (regresión, clustering)

### Cap 3: Feature Engineering (3 lecciones)
- [ ] **3.1** `cap-3-1-feature-engineering.md` - Feature Engineering (40 min)
  - Derivación de features (ratio, diferencias, productos)
  - Composición de features relevantes
  - Agregaciones por grupos
  
- [ ] **3.2** `cap-3-2-features-temporales.md` - Features temporales (35 min)
  - Extracción: hora, día, mes, estación, día de semana
  - Ventanas deslizantes (rolling windows)
  - Lags y differencing para series temporales
  
- [ ] **3.3** `cap-3-3-feature-selection.md` - Selección de features (40 min)
  - Importancia de features (Random Forest, permutation)
  - Análisis de correlación y multicolinealidad
  - Métodos: filtrado, wrapper, embedded

### Taller 1
- [ ] `taller-1-datos-energetico.md` - **Taller 1: Proyecto Energético - Datos de Sensores** (90 min)
  - Ingesta de telemetría real
  - Limpieza y normalización
  - Extracción de features temporales
  - Entrega: Dataset preprocesado validado

---

## Unidad 2: Procesamiento de Imágenes (OCR) (6 lecciones + 1 taller)

### Cap 1: Fundamentos de OCR (3 lecciones)
- [ ] **1.1** `cap-1-1-ocr-conceptos.md` - OCR: conceptos básicos (30 min)
  - Qué es OCR, cuándo usar, limitaciones
  - Flujo básico: imagen → preprocesamiento → extracción → validación
  - Casos de uso: facturas, certificados, documentos
  
- [ ] **1.2** `cap-1-2-preprocesamiento-imagen.md` - Preprocesamiento de imágenes (40 min)
  - OpenCV: conversión a escala de grises, binarización
  - Rotación, escalado, crop
  - Noise removal (Gaussian blur, morphological ops)
  
- [ ] **1.3** `cap-1-3-tesseract-paddleocr.md` - Tesseract y Paddleocr (40 min)
  - Instalación y configuración
  - Parámetros de configuración por idioma/tipo de documento
  - Extracción de texto crudo vs. estructurado

### Cap 2: Extracción de Datos desde Facturas (3 lecciones)
- [ ] **2.1** `cap-2-1-facturas-pdf.md` - Facturas en PDF (35 min)
  - PyPDF2, pdfplumber para lectura de PDFs
  - Extracción de tablas desde documentos digitales
  - Desafíos: PDFs escaneados vs. PDFs nativos
  
- [ ] **2.2** `cap-2-2-facturas-fotos.md` - OCR en fotografías (40 min)
  - Captura de fotos de facturas
  - Corrección de orientación automática
  - OCR con Tesseract/Paddleocr
  - Validación de calidad
  
- [ ] **2.3** `cap-2-3-parsing-validacion.md` - Parsing y validación (40 min)
  - Expresiones regulares para extracción de campos
  - Validación: rango de consumo, período coherente
  - Manejo de variantes (diferentes distribuidoras)

### Taller 2
- [ ] `taller-2-ocr-facturas.md` - **Taller 2: Proyecto Energético - OCR de Facturas** (90 min)
  - Procesamiento de facturas PDF y fotos reales
  - Extracción de consumo, período, monto
  - Validación y integración con datos de sensores
  - Entrega: Dataset de facturas estructurado

---

## Unidad 3: Procesamiento de Habla y NLP (6 lecciones + 1 taller)

### Cap 1: Fundamentos de NLP (3 lecciones)
- [ ] **1.1** `cap-1-1-conceptos-pnl.md` - Conceptos de PNL (40 min)
  - Tokenización (palabras, subpalabras)
  - Lemmatización y stemming
  - Embeddings de palabras (Word2Vec, GloVe)
  
- [ ] **1.2** `cap-1-2-speech-recognition.md` - Speech-to-Text (35 min)
  - Bibliotecas: SpeechRecognition, Vosk, Whisper
  - Transcripción de audio en tiempo real
  - Manejo de ruido y acentos
  
- [ ] **1.3** `cap-1-3-chatbot-basico.md` - Bots conversacionales (40 min)
  - Arquitectura: intenciones, entities, respuestas
  - Pattern matching vs. machine learning
  - Framework: Rasa, ChatterBot, LLM-based

### Cap 2: Bots Energético y Académico (3 lecciones)
- [ ] **2.1** `cap-2-1-bot-energetico.md` - Bot energético (40 min)
  - Preguntas frecuentes: consumo, tarifas, facturación
  - Integración con datos de sensores
  - Respuestas contextuales (ej: "¿Cuál fue mi consumo en octubre?")
  
- [ ] **2.2** `cap-2-2-bot-academico.md` - Bot académico (40 min)
  - Orientación: carreras, requisitos, inscripción
  - Información de cursos y docentes
  - Recomendaciones personalizadas
  
- [ ] **2.3** `cap-2-3-analisis-sentimiento.md` - Análisis de sentimiento (35 min)
  - Clasificación: positivo, negativo, neutral
  - Herramientas: TextBlob, Transformers (BERT)
  - Aplicación: feedback de estudiantes

### Taller 3
- [ ] `taller-3-nlp-bots.md` - **Taller 3: Bots Energético y Académico** (120 min)
  - Diseño de flujos conversacionales
  - Implementación de bots integrados
  - Entrega: Bots funcionando en ambos contextos

---

## Unidad 4: Creación de Modelos Predictivos (9 lecciones + 1 taller)

### Cap 1: Regresión y Series Temporales (3 lecciones)
- [ ] **1.1** `cap-1-1-regresion-lineal.md` - Regresión lineal (40 min)
  - Modelo lineal simple y múltiple
  - Evaluación: R², RMSE, MAE
  - Predicción de consumo energético
  
- [ ] **1.2** `cap-1-2-series-temporales.md` - Series temporales (45 min)
  - ARIMA (AutoRegressive Integrated Moving Average)
  - Exponential Smoothing (Holt-Winters)
  - Prophet para predicciones robustas
  
- [ ] **1.3** `cap-1-3-validacion-temporal.md` - Validación temporal (35 min)
  - Train-test split temporal (sin "future leakage")
  - Cross-validation para series
  - Métricas de forecasting

### Cap 2: Clasificación y Recomendación (3 lecciones)
- [ ] **2.1** `cap-2-1-clasificacion-basica.md` - Clasificación (40 min)
  - Logistic Regression, SVM, Naive Bayes
  - Árboles de decisión
  - Matriz de confusión, precision, recall
  
- [ ] **2.2** `cap-2-2-ensambles.md` - Métodos de ensamble (45 min)
  - Random Forest: ventajas y ajustes
  - Gradient Boosting (XGBoost, LightGBM)
  - Stacking y voting
  
- [ ] **2.3** `cap-2-3-recomendacion.md` - Sistemas de recomendación (40 min)
  - Filtrado colaborativo
  - Recomendación basada en contenido
  - Aplicación: sugerencias de cursos

### Cap 3: Evaluación y Ajuste (3 lecciones)
- [ ] **3.1** `cap-3-1-metricas-evaluacion.md` - Métricas (40 min)
  - Clasificación: accuracy, precision, recall, F1, AUC-ROC
  - Regresión: MAE, RMSE, R²
  - Elección según el problema
  
- [ ] **3.2** `cap-3-2-hyperparameter-tuning.md` - Ajuste de hiperparámetros (35 min)
  - GridSearchCV, RandomSearchCV, Optuna
  - Early stopping, validación cruzada
  
- [ ] **3.3** `cap-3-3-overfitting-regularizacion.md` - Overfitting (35 min)
  - Detección: brecha entre train/test
  - Regularización: L1/L2
  - Técnicas: dropout, early stopping, data augmentation

### Taller 4
- [ ] `taller-4-ml-modelos.md` - **Taller 4: Modelos Energético y Académico** (120 min)
  - Entrenamiento de modelo de predicción de consumo
  - Sistema de recomendación de cursos
  - Evaluación comparativa de modelos
  - Entrega: Modelos entrenados y validados

---

## Unidad 5: Post-Procesamiento y Comunicación (6 lecciones + 1 taller)

### Cap 1: Visualización y Dashboards (3 lecciones)
- [ ] **1.1** `cap-1-1-matplotlib-plotly.md` - Visualización (40 min)
  - Matplotlib, Seaborn para gráficos estáticos
  - Plotly para visualizaciones interactivas
  - Mejores prácticas de diseño
  
- [ ] **1.2** `cap-1-2-dashboards-dash.md` - Dashboards (45 min)
  - Plotly Dash: componentes, callbacks, layouts
  - Streamlit como alternativa
  - Deployment local y en cloud
  
- [ ] **1.3** `cap-1-3-kpi-metricas.md` - KPIs y métricas (35 min)
  - Diseño de KPIs para audiencias no técnicas
  - Scorecards y métricas clave
  - Storytelling con datos

### Cap 2: Informes y Documentación (3 lecciones)
- [ ] **2.1** `cap-2-1-informe-tecnico.md` - Informe técnico (40 min)
  - Estructura: resumen, metodología, resultados, conclusiones
  - Redacción clara y profesional
  - Citación de fuentes y reproducibilidad
  
- [ ] **2.2** `cap-2-2-jupyter-notebooks.md` - Jupyter Notebooks (35 min)
  - Notebooks como medio de comunicación
  - Cells de código + markdown narrativo
  - Interactividad con widgets
  
- [ ] **2.3** `cap-2-3-presentacion-defensa.md` - Presentación y defensa (40 min)
  - Estructura de slides (20-30 min de exposición)
  - Storytelling del proyecto
  - Manejo de preguntas del tribunal

### Taller 5
- [ ] `taller-5-visual-dashboards.md` - **Taller 5: Dashboards y Defensa** (120 min)
  - Dashboards interactivos finales
  - Informe técnico completo
  - Preparación de presentación de defensa
  - Entrega: Materiales de defensa listos

---

## Notas de desarrollo

### Prioridades
1. **Semana 1-2:** Completar Unit 1 (Datos) → Taller 1
2. **Semana 3-4:** Completar Unit 2 (OCR) → Taller 2
3. **Semana 5-6:** Completar Unit 3 (NLP) → Taller 3
4. **Semana 7-8:** Completar Unit 4 (Modelos) → Taller 4
5. **Semana 9-10:** Completar Unit 5 (Comunicación) → Taller 5

### Convenciones de archivos
- Archivos `.md` nombrados como: `cap-{numero}-{subtitulo}.md`
- Todos los archivos en: `lecciones/`
- Lenguaje: **exclusivamente español**
- Ejemplos de código: Python 3.10+

### Plantilla de lección
```markdown
# {numero}. {Título de la Lección}

## Objetivo
[1-2 líneas de qué aprenderán]

## Contenidos
[Desarrollo temático con subtítulos, ejemplos de código, diagramas]

## Actividad práctica
[Tarea concreta a realizar]

## Palabras clave
[Lista de términos para índice]

## Referencias
[Enlaces y bibliografía]
```

---

## Historial de cambios

| Fecha | Cambio |
|-------|--------|
| 2026-10-04 | Creación de estructura y primeras 2 lecciones (Cap 1.1, 1.2) |
