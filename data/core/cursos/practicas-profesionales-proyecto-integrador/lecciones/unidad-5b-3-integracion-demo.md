# 5B.3 Integración de Módulos, Testing de Integración y Demo al Equipo

## Objetivo

Verificar que módulos trabajan juntos (no solo aislados). Demostrar funcionalidad completada al equipo. Reflexionar sobre lo aprendido y planificar mejoras (retrospective).

## Referencia

**Unidad 5A.1:** Integración de técnicas (arquitectura)

**Unidad 5B.2:** Desarrollo limpio (código que permite testing)

**spec:** § Testing de Integración

## Contenidos

### 1. Testing de Integración: Qué NO es Unitario

**Tests Unitarios (hechos antes, Unidad 6):**
```python
# Testea: funciones aisladas, con mocks
def test_ocr_reads_image():
    mock_image = MagicMock()
    result = ocr.read(mock_image)
    assert result == "extracted text"
    # El resto del sistema (NLP, ML) no existe aquí
```

Ventaja: Rápido (< 1 seg), aislado de dependencias
Problema: ¿Qué pasa cuando OCR + NLP se conectan?

**Tests de Integración (ahora, Unidad 5B):**
```python
# Testea: flujo completo, sin mocks
def test_ocr_nlp_integration():
    # Setup real: cargar imagen real, NLP real
    image = Image.open("test_data/invoice.png")
    
    # Ejecutar flujo: OCR → NLP
    extracted_text = ocr.read(image)        # Output: "kWh: 1250"
    intent = nlp.understand(extracted_text)  # Input: "kWh: 1250"
    
    # Assert: ¿flujo se comunicó bien?
    assert intent.type == "measurement"
    assert intent.value == 1250
    assert intent.unit == "kWh"
    
    # Verificar: si OCR falla, ¿NLP maneja gracefully?
    # Verificar: datos se pasaron correctamente
```

Ventaja: Detecta bugs de integración temprano
Problema: Más lento, depende de datos reales

### 2. Casos de Integración Típicos

**Energy-ML: MQTT → Normalización → ML**

```python
def test_mqtt_normalization_integration():
    """MQTT stream → datos normalizados → modelo puede predecir"""
    
    # Mock de MQTT: simula sensor enviando consumo
    mqtt_message = {
        "timestamp": "2026-10-04T18:00:00",
        "power_kw": 52.3,
        "voltage_v": 230,
        "current_a": 227  # 52.3 kW / 230V ≈ 227A
    }
    
    # Flujo: MQTT raw → aplicación → DTO normalizados
    raw_data = mqtt.consume(mqtt_message)
    validated = validate(raw_data)  # ¿valores en rango?
    normalized = normalize(validated)  # ¿% del promedio?
    
    # Verifica: DTO tenga forma esperada
    assert isinstance(normalized, MedidaNormalizada)
    assert 0 <= normalized.percent_of_average <= 200  # razonable
    
    # Verifica: modelo puede procesarla
    prediction = ml_model.predict(normalized)
    assert prediction.predicted_kw > 0
```

**Portal: NLP → Recomendador ML → Respuesta**

```python
def test_nlp_recommender_integration():
    """Consulta → NLP entiende → ML recomienda → respuesta amigable"""
    
    # Input: alumno pregunta en chat
    user_query = "Me interesa programación y datos"
    
    # Flujo: NLP extrae intención
    intent = nlp.extract_intent(user_query)
    assert intent.type == "query_carrera"
    assert "programacion" in intent.topics
    
    # ML recomienda carreras similares
    recommendations = ml_recommender.recommend(intent)
    assert len(recommendations) > 0
    assert recommendations[0].carrera_name == "Ciencia de Datos"
    
    # Post-procesamiento: generar respuesta
    response = format_response(recommendations)
    assert "Ciencia de Datos" in response
    assert "programación" in response.lower()
```

### 3. Manejo de Errores en Cascada

**Problema real:** Si un componente falla, el sistema NO debe crashear.

```python
def test_ocr_fails_handling():
    """Si OCR falla, NLP recibe error gracefully"""
    
    # Setup: imagen corrupta (OCR fallará)
    bad_image = Image.open("test_data/corrupted.bin")
    
    # OCR intenta, falla
    with pytest.raises(OCRException):
        extracted = ocr.read(bad_image)
    
    # El sistema maneja: retorna default o dummy
    # (no cruza NULL/error a siguiente componente)
    try:
        extracted = ocr.read(bad_image)
    except OCRException:
        extracted = DEFAULT_TEXT  # fallback
        logger.warn("OCR failed, using default")
    
    # NLP recibe algo razonable (no crash)
    intent = nlp.understand(extracted)
    assert intent is not None  # No crash
```

### 4. Sprint Review (Viernes, 1 hora)

Se ejecuta viernes de última semana del sprint.

**Objetivo:** Demo de lo que funciona. PO (docente) acepta o pide cambios.

**Participantes:**
- Dev Team (demuestra)
- PO (docente) + stakeholders si hay
- Otros estudiantes pueden observar

**Estructura (60 min):**

```
0-5 min: Intro
├─ "Sprint 1: Demo de MQTT + Dashboard"
└─ "Completamos 13/13 puntos. Sprint Goal: ✅ alcanzado"

5-40 min: Demo vivo
├─ Abren aplicación (no screenshots)
├─ Sensor MQTT: "Enviamos datos de consumo"
│  └─ Terminal: simulador de sensor publica JSON
├─ Dashboard: "Aquí aparecen datos en tiempo real"
│  └─ Abren navegador, dashboard actualiza
├─ "Si consumo sube > 20%, alerta roja"
│  └─ Simulan anomalía, alerta aparece
└─ Q&A rápidas

40-50 min: Métricas y documentación
├─ "Velocity: 13 pt (estimamos 12, hicimos 13)"
├─ "Tests: 87% cobertura"
├─ "Commits: 25 commits, todos atómicos"
└─ "Repositorio: todo en GitHub, branches limpias"

50-60 min: Feedback de PO
├─ PO: "Excelente, esto resuelve el problema real"
│  └─ Feedback: "¿Podríamos agregar filtro por horario en Sprint 2?"
└─ Documentar requests en Product Backlog para Sprint 2
```

**Documentación de Demo:**
```markdown
# Sprint 1 Review - energy-ml

**Date:** Viernes, Semana 11
**Attendees:** Dev1, Dev2, Dev3, Docente (PO), Invitado (operador)

## Demo Executed
- [ ] MQTT connect y recibe datos
- [ ] Dashboard actualiza en tiempo real
- [ ] Alertas funcionan (prueba con consumo simulado alto)

## Velocity
- Planned: 13 pt (US-02: 8, US-01: 5)
- Completed: 13 pt ✅
- Velocity this sprint: 13

## Code Quality
- Test coverage: 87%
- Commits: 25 (todos atómicos)
- Code review: 100% (todos PRs revieweados)
- Pyright errors: 0

## PO Feedback
- "Bueno, cumplió requisitos"
- "¿Próximo sprint: exportar datos a CSV?"
- "¿Integrar con Telegram para alertas?" (Could Have)

## Impediments Resolved
- Sensor MQTT estuvo offline martes, pero usamos fallback

## Next Steps
- Sprint 2: US-03 (Modelo ML) + US-04 (Anomalías)
```

### 5. Sprint Retrospective (Viernes después de Review, 1 hora)

**Objetivo:** Team reflexiona. ¿Qué salió bien? ¿Qué mejorar?

**Formato clásico (60 min):**

```
0-5 min: Setup y reglas
├─ "Retrospectiva es espacio seguro. Honestidad sin culpas."
└─ "Nadie es 'malo'. Procesos pueden mejorar."

5-20 min: "What went well?"
├─ Cada uno piensa 2-3 minutos
├─ Escriben en post-it (anónimo ayuda)
├─ Comparten en voz alta
├─ Ejemplos:
│  ├─ Dev1: "Planning claro, sabía exactamente qué hacer"
│  ├─ Dev2: "Code review tuvo comentarios constructivos, aprendí"
│  └─ Dev3: "Ayuda mutua cuando alguien estaba stuck"

20-35 min: "What could be better?"
├─ Similar: 2-3 min thinking, post-it anónimo
├─ Ejemplos:
│  ├─ "Daily standups fueron muy cortos, no aprovechamos"
│  ├─ "Tests: nos quedaron para último día, stresado"
│  └─ "Falta pair programming, muy siloed"

35-50 min: "Acción concreta para Sprint 2"
├─ De "mejoras", elegir 1-2 que **realmente haremos**
├─ NO: "mejorar comunicación" (vago)
├─ SÍ: "En standups, cada uno habla máximo 3 min. Facilitador usa timer."
├─ SÍ: "Tests se escriben en paralelo con código, no al final"
└─ Documentar en `SPRINT_1_RETRO.md`

50-60 min: Celebración
├─ "Completamos 13 puntos, código es limpio, demo fue éxito"
├─ Foto de equipo (opcional)
└─ "Vamos a Sprint 2 con mejoras implementadas"
```

**Documento de Retrospective:**
```markdown
# Sprint 1 Retrospective

**Date:** Viernes, Semana 11
**Participants:** Dev1, Dev2, Dev3, Docente (Scrum Master)

## What Went Well ✅
- Planning fue claro, todos entendieron qué hacer
- Code review constructivo, aprendimos mucho
- Comunicación en Slack fue ágil
- Demo funcionó (nervios pero bien)

## What Could Be Better 🔄
- Standups fueron muy rápidos, no hablamos de riscos
- Escribimos tests último día, fue estresante
- Poco pair programming (mucho siloed)
- Documentación quedó para último

## Actionable for Sprint 2 🎯
1. **Standups:** 15 min real (no 10), usamos para discutir riscos
   - Owner: Scrum Master, revisará en Sprint 2
   
2. **Tests:** TDD desde el inicio
   - Por cada feature, escribir test ANTES de código
   - Owner: Dev1 guía, explicará TDD a equipo

3. **Pair Programming:** 2h/semana mínimo
   - Lunes 18:00-20:00: algún par programa junto
   - Owner: SM coordina parejas

4. **Documentación:** Paralelo con código
   - Docstring mientras escribo (no después)
   - Owner: Dev2 hace check-in viernes

## Velocity Trend
- Sprint 1: 13 pt ✅
- Sprint 2 estimate: 12 pt (similar, esperar)

## Next Retro
Sprint 2 Retrospective: Viernes, Semana 13
```

## Actividad Práctica

1. **Escribir tests de integración (durante Sprint 1-2):**
   ```python
   # tests/test_integration_ocr_nlp.py
   def test_ocr_to_nlp_flow():
       """Verificar OCR + NLP comunican correctamente"""
       # Setup
       image = load_test_image("invoice.png")
       
       # Execute
       text = ocr.process(image)
       intent = nlp.understand(text)
       
       # Assert
       assert isinstance(intent, Intent)
       assert intent.type in ["measurement", "query", ...]
   ```

2. **Ejecutar Sprint Review (Viernes, Semana 11):**
   - Demo vivo de funcionalidades completadas
   - Métricas: velocity, cobertura, commits
   - Feedback de PO

3. **Ejecutar Sprint Retrospective (Viernes, Semana 11):**
   - 3 preguntas: "qué salió bien", "qué mejorar", "1 acción"
   - Documentar en `SPRINT_1_RETRO.md`
   - Comprometerse a 1-2 mejoras concretas para Sprint 2

4. **Documentar:** `SPRINT_1_DEMO.md` + `SPRINT_1_RETRO.md`

## Palabras clave

Testing de integración, Sprint Review, Demo, Retrospective, Velocity, Actionable, Continuous improvement

## Referencias

- spec § Testing de Integración
- Scrum Guide (Ceremonies)
- Agile Retrospectives: Making Good Teams Great
