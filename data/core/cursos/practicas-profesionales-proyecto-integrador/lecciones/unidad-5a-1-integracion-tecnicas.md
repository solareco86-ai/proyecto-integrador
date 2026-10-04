# 5A.1 Integración de Técnicas: Arquitectura de Imágenes + Habla + ML

## Objetivo

Entender cómo **procesamiento de imágenes** (imágenes de drones, OCR), **procesamiento del habla** (NLP, extracción de intención), y **Machine Learning** (modelos predictivos) trabajan JUNTOS en un sistema coherente. NO es "usar 3 técnicas aisladas"; es diseñar **un flujo de datos** donde cada técnica prepara input para la siguiente, según la prescripción oficial del Anexo 1 DGCyE.

## Referencia

**spec:** § Stack Tecnológico (integración de componentes)

**PAA (2do año):** Unidad 1-4 (modelos ML, pipelines, evaluación)

**Procesamiento de Imágenes Digitales (3er año):** OCR, detección de patrones, clasificación visual

**Procesamiento del Habla / NLP (2do año):** Análisis morfológico, modelos de lenguaje, procesamiento de audio

## Contenidos

### 1. ¿Qué NO es integración?

Antes de definir qué es integración, veamos qué NO es:

**Antipatrón 1: 3 modelos aislados**
```
[Imagen] → OCR → [Texto] ❌ (no se usa)
[Audio] → NLP → [Intent] ❌ (no se usa)
[Datos] → ML → [Predicción] ❌ (se usa)
```
Problema: OCR y NLP no comunican con ML. Decisiones del usuario (intent) no afectan predicción.

**Antipatrón 2: Secuencial ingenuamente**
```
Input → OCR → NLP → ML → Output
```
Problema: Si OCR falla (ej: documento borroso), NLP recibe garbage y produce basura. No hay manejo de errores.

**Antipatrón 3: "Agregar técnicas hasta que funcione"**
```
Intentamos OCR. No funciona bien.
Agregamos NLP para "ayudar". Sigue sin funcionar.
Agregamos ML para "aprender". A veces funciona.
Documentación: "no sé cómo funciona esto, pero funciona a veces".
```
Problema: Sin arquitectura clara, nadie puede mantener el código.

### 2. ¿Qué ES integración?

**Definición:** Un **flujo de datos coherente** donde:
1. Cada técnica tiene una responsabilidad clara (Single Responsibility Principle)
2. Comunican vía **interfaces bien definidas** (DTOs, contratos)
3. **Manejo de errores en cascada:** si un componente falla, el sistema maneja gracefully
4. **Testeable:** se puede probar la integración, no solo componentes aislados
5. **Documentada:** decisiones arquitectónicas están explícitas

**Ejemplo:** Energy-ML con integración correcta
```
Sensores MQTT
    ↓
[Validación: ¿datos válidos?]
    ↓ (si NO) → Log error, continuar con datos anteriores
    ↓ (si SÍ)
[Normalización: escalar a unidades estándar]
    ↓
[ML (PAA): Predicción de consumo próxima hora]
    ↓
[Comparación: real vs predicción]
    ↓
[Decisión: ¿anomalía detectada?]
    ├─ SÍ → Alerta a operador
    └─ NO → Log normal
```

### 3. Caso 1: Energy-ML - Flujo de Integración

**Problema:** Instituto quiere saber si consumo eléctrico es anómalo (arriba de lo esperado).

**Solución:**

```markdown
## Entrada
- Sensores MQTT: envían consumo kWh cada 5 minutos
- Historial: datos de últimos 3 años (base de datos)

## Componente 1: Lectura y Validación (Infrastructure)
- Conectar a broker MQTT
- Recibir JSON: {timestamp, power_kw, voltage_v, current_a}
- Validar: ¿valores en rango esperado?
- Si error: loguear, usar último valor válido (fallback)
- Output: DT O `MedidaEléctrica(timestamp, power_kw)`

## Componente 2: Limpieza y Normalización (Application)
- Input: MedidaEléctrica cruda
- Eliminar outliers (ej: picos causados por ruido)
- Normalizar: convertir a "% del consumo promedio"
  Ej: 50 kW actual vs 40 kW promedio = 125%
- Output: DTO `MedidaNormalizada(timestamp, percent_of_average)`

## Componente 3: ML - Predicción (Application - PAA)
- Input: Datos históricos + hoy
- Entrenar modelo (regresión, serie temporal)
- Predecir: consumo esperado para próxima hora
- Output: DTO `Predicción(timestamp, predicted_kw, confidence)`

## Componente 4: Comparación y Detección de Anomalías (Application)
- Input: MedidaNormalizada (real) + Predicción (esperado)
- Lógica: Si real > (predicted + 20%), marcar como anomalía
- Output: DTO `Anomalía(timestamp, severity: LOW|MEDIUM|HIGH, reason)`

## Salida
- Dashboard: muestra consumo real vs predicción (visualización)
- Alertas: si anomalía MEDIUM/HIGH, notificar a operador
- Historial: registrar todas las medidas para retraining mensual

## NLP (Bonus - 2do año):
- Operador pregunta: "¿Por qué consumo subió?"
- NLP entiende intención de la pregunta
- Sistema responde: "Consumo subió porque viernes hubo evento en auditorio"
```

### 4. Caso 2: Portal Institucional - Flujo de Integración

**Problema:** Alumno no sabe qué carrera elegir. Consultar a secretaría es lento.

**Solución:**

```markdown
## Entrada
- Consulta de alumno (texto libre): "Hola, me interesa programación"

## Componente 1: NLP - Entendimiento (Application - 2do año)
- Input: "Hola, me interesa programación"
- NLP analiza:
  - Intención: consulta_carrera (vs consulta_horario, consulta_requisito)
  - Entidad extraída: "programación"
- Output: DTO `Intención(tipo, entidades_extraídas)`

## Componente 2: ML - Recomendador (Application - PAA)
- Input: Intención + perfil del alumno (si existen datos: materias aprobadas, aptitudes)
- Modelo: Recomendador (ML, PAA) basado en:
  - Similitud: "programación" → buscar carreras con programming
  - Perfil: si alumno aprobó matemática avanzada, recomendar carrera técnica
  - Popularidad: qué carrera tiene más egresados empleados
- Output: DTO `Recomendación(carrera, score, justificación)`

## Componente 3: OCR (opcional - 3er año)
- Si alumno sube su análisis de 5to/6to año (foto escaneada)
- OCR extrae: materias cursadas, calificaciones
- Enriquece perfil para mejor recomendación
- Output: DTO `PerfilAlumno(materias, calificaciones)`

## Componente 4: Presentación (Adapters)
- Input: Recomendación + PerfilAlumno
- Generar respuesta natural: "Te recomendamos Ciencia de Datos porque se ajusta a tu perfil en lógica y matemática"
- Agregar links: plan de estudios, requisitos, docentes
- Output: HTML respuesta en chat

## Salida
- Chat: alumno ve respuesta personalizada
- Link: puede ir directamente a página de carrera
- Historial: registrar consulta para análisis futuro
```

### 5. Principios de Integración (Clean Architecture)

Ambos casos siguen estos principios:

1. **Separation of Concerns:** Cada componente tiene UNA responsabilidad
   - Lectura ≠ Validación ≠ ML ≠ Alertas
   - Si cambio lógica de ML, no toco código de lectura

2. **Contracts (DTOs):** Componentes comunican vía interfaces claras
   ```python
   # Input a ML
   @dataclass
   class MedidaNormalizada:
       timestamp: datetime
       percent_of_average: float
   
   # Output de ML
   @dataclass
   class Predicción:
       timestamp: datetime
       predicted_kw: float
       confidence: float
   
   # No hardcodeamos: "ML.predict(raw_data)"
   # Sí hacemos: "ML.predict(medida_normalizada) → predicción"
   ```

3. **Error Handling:** Cada componente puede fallar, asumimos que lo hace
   ```python
   try:
       medida = sensor.read()  # ¿Qué pasa si sensor offline?
   except SensorOfflineError:
       medida = usar_última_medida_válida()
       log.warning("Sensor offline, usando fallback")
   
   # El sistema NO crashea; continúa robustamente
   ```

4. **Testeable:** Cada componente se testea aislado + se testea integración
   ```python
   # Test unitario: ML predice bien (con datos mockeados)
   test_ml_predicts_correctly()
   
   # Test integración: Lectura → Normalización → ML → Comparación
   test_full_anomaly_detection_flow()
   ```

### 6. Decisiones Arquitectónicas Clave

Para cada proyecto, hay preguntas que responder:

**Energy-ML:**
- ¿OCR se usa? (SÍ, si hay facturas escaneadas; NO, si datos vienen digitales)
- ¿NLP se usa? (BONUS, para bot conversacional; no es Must)
- ¿ML es supervisado o no? (Supervisado: entrenamos con datos históricos)
- ¿Retraining es semanal, mensual, anual? (Semanal: datos cambian rápido)

**Portal:**
- ¿OCR se usa? (Opcional, para análisis de alumnos)
- ¿NLP es necesario? (SÍ, core del sistema; debe entender intent)
- ¿ML es colaborativo o contentbased? (Content-based: similitud carrera vs intent)
- ¿Retraining es manual o automático? (Manual: cambios en curriculum son raros)

**Documentación:** Cada decisión se justifica en `ARCHITECTURE.md`.

## Actividad Práctica

1. **Dibuja el flujo de datos de tu proyecto:**
   ```
   [Entrada] → [Componente 1] → [DTO] → [Componente 2] → [DTO] → ... → [Salida]
   ```

2. **Para cada componente, responde:**
   - ¿Qué entra? (DTO input)
   - ¿Qué sale? (DTO output)
   - ¿Qué pasa si falla? (error handling)
   - ¿Cómo se testea? (test case)

3. **Documenta en `INTEGRATION_ARCHITECTURE.md`:**
   ```markdown
   # Arquitectura de Integración

   ## Flujo de Datos
   [Diagrama ASCII o descripción]

   ## Componentes
   
   ### 1. Lectura (Infrastructure)
   **Entrada:** Sensores MQTT
   **Salida:** DTO `MedidaEléctrica`
   **Error handling:** Si sensor offline, usar último valor válido
   **Test:** test_mqtt_read_valid_data, test_mqtt_sensor_offline
   
   ### 2. Normalización (Application)
   ...
   ```

## Palabras clave

Integración, Flujo de datos, Pipeline, DTO, Contrato, Error handling, Componentes, Responsabilidad única

## Referencias

- spec § Stack Tecnológico (arquitectura de componentes)
- Uncle Bob, "Clean Architecture"
- Martin Fowler, "Microservices Patterns" (ch. Integration Patterns)
