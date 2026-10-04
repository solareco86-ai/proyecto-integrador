# 6.3 Validación de Requisitos: Traceability Matrix y UAT

## Objetivo

Verificar que **cada requisito especificado en SRS (Unidad 2) está implementado y funciona**. NO es "ejecutar tests random"; es validar que **cada FR y NFR tiene evidencia de cumplimiento**.

## Referencia

**spec § 5.5:** Validación de Requisitos (parte de la matriz)

**Plan Oficial § Referenciales para la evaluación:** Coherencia entre hipótesis, datos y conclusiones

## Contenidos

### 1. ¿Qué es Validación de Requisitos?

En Unidad 2 escribimos SRS (Especificación de Requisitos). Ahora verificamos:

| Requisito | Implementado? | Testeado? | Aprobado? |
|-----------|---------------|-----------|-----------|
| FR-01: Lectura MQTT | ✅ Sí | ✅ Test #42 | ✅ Sí |
| FR-02: Dashboard | ✅ Sí | ✅ Test #50 | ✅ Sí |
| NFR-01: Latencia < 1s | ⚠️ 1.2s | ✅ Test #55 | ❌ NO |
| NFR-02: 99% uptime | ✅ Sí | ⚠️ Difícil de testear | ⚠️ Parcial |

**Outcome:** Si hay gaps, priorizamos en Unidad 7-8.

### 2. Traceability Matrix (RTM)

Una tabla que conecta:
```
Requisito SRS → Test Unitario/Integración → Aceptación
```

**Estructura:**

```markdown
# Traceability Matrix - energy-ml

| Req ID | Descripción | Test Case | Test Status | Demo | UAT | Notes |
|--------|-------------|-----------|-------------|------|-----|-------|
| FR-01 | Lectura sensores MQTT | TC-01 (test_mqtt_read) | ✅ PASS | ✅ Works | ✅ OK | - |
| FR-02 | Dashboard tiempo real | TC-02 (test_dashboard_updates) | ✅ PASS | ✅ Works | ✅ OK | Latencia 800ms |
| FR-03 | Alertas si anomalía | TC-03 (test_anomaly_alert) | ✅ PASS | ✅ Works | ⚠️ REVIEW | PO quiere más tests |
| NFR-01 | Latencia < 1s | TC-04 (test_latency_dashboard) | ⚠️ MARGIN | ❌ Fails | ❌ FAIL | 1.2s, fuera spec |
| NFR-02 | 99% uptime | TC-05 (test_fault_tolerance) | ✅ PASS | ⚠️ Simul. | ⚠️ TBD | Necesita monitoring real |
| NFR-03 | Datos encriptados | TC-06 (test_encryption) | ✅ PASS | ✅ Works | ✅ OK | - |

## Resumen
- **Implementados:** 6/6 ✅
- **Testeados:** 6/6 ✅
- **UAT Aprobados:** 4/6 ⚠️
- **Bloqueadores:** FR-03 (revisión), NFR-01 (latencia)
```

### 3. Test Cases (TC) Específicos para Requisitos

**Cada requisito → 1+ test case:**

```python
# tests/test_traceability.py

class TestFunctionalRequirements:
    """Mapping: FR → TC"""
    
    # FR-01: Sistema recibe telemetría de sensores MQTT
    def test_FR01_mqtt_receives_sensor_data(self):
        """TC-01: MQTT recibe JSON de sensores válido"""
        # Arrange
        mqtt_broker = setup_mqtt_broker()
        
        # Act
        mqtt_broker.publish("sensors/power", '{"kw": 52.3}')
        received_message = wait_for_message(timeout=2)
        
        # Assert
        assert received_message is not None
        assert received_message["kw"] == 52.3
    
    # FR-02: Dashboard muestra consumo en tiempo real
    def test_FR02_dashboard_updates_in_realtime(self):
        """TC-02: Dashboard actualiza c/1 min con datos nuevos"""
        # Arrange
        dashboard = DashboardPage()
        timestamp_1 = dashboard.last_update
        
        # Act: Esperar dato nuevo
        mqtt.publish("sensors/power", '{"kw": 55}')
        wait_for_update(dashboard)
        
        # Assert
        assert dashboard.current_kw == 55
        assert dashboard.last_update > timestamp_1

class TestNonFunctionalRequirements:
    """Mapping: NFR → TC"""
    
    # NFR-01: Latencia de dashboard < 1 segundo
    def test_NFR01_dashboard_latency_under_1s(self):
        """TC-04: Dato entra a MQTT, aparece en dashboard en < 1s"""
        # Arrange
        mqtt = setup_mqtt()
        dashboard = DashboardPage()
        
        # Act
        start = time.time()
        mqtt.publish("sensors/power", '{"kw": 60}')
        dashboard.wait_for_value(60, timeout=1)
        elapsed = time.time() - start
        
        # Assert
        assert elapsed < 1.0, f"Latencia {elapsed}s > 1s, FALLA NFR-01"
    
    # NFR-02: Sistema disponible 99% del tiempo
    def test_NFR02_system_uptime_99percent(self):
        """TC-05: Simular 100 requests, 99+ deben ser exitosos"""
        # Arrange
        api = APIClient()
        success_count = 0
        
        # Act
        for i in range(100):
            try:
                response = api.get_dashboard()
                if response.status == 200:
                    success_count += 1
            except TimeoutError:
                pass  # Falla, no cuenta
        
        # Assert
        uptime_percent = (success_count / 100) * 100
        assert uptime_percent >= 99, f"Uptime {uptime_percent}% < 99%"
```

### 4. User Acceptance Testing (UAT)

**UAT = Usuario real prueba y acepta ("done").**

No es técnico. Es: "¿Esto resuelve el problema que me sacaba?"

**Ejemplo Energy-ML:**

```markdown
# UAT Plan - energy-ml

## Stakeholder: Operador de Institución Energética

### Test 1: ¿Veo consumo en tiempo real?
Operador abre dashboard.
- ✅ Dashboard carga
- ✅ Muestra consumo actual (52.3 kWh)
- ✅ Muestra histórico de hoy
- ✅ Entiende qué significan los números

**Resultado:** ✅ APROBADO

### Test 2: ¿Me alerta si hay anomalía?
Simulamos consumo alto.
- ✅ Dashboard muestra alerta roja
- ✅ Alerta dice "Consumo 20% sobre promedio"
- ⚠️ Operador dice: "Recomendación: ¿de quién es la máquina que consume más?"

**Resultado:** ⚠️ APROBADO CON FEEDBACK

### Test 3: ¿Es rápido?
Operador mide: dato entra → aparece en dashboard
- ⚠️ Toma 1.2 segundos (spec dice < 1s)
- Operador: "Para mí está bien, pero verifica si spec lo requiere"

**Resultado:** ⚠️ PASS TÉCNICAMENTE, PERO FUERA SPEC
```

**Acta de UAT:**

```markdown
# UAT Sign-Off - energy-ml

**Fecha:** 2026-10-15
**Lugar:** Institución Energética XXXX
**Participantes:** Operador (PO real), Dev Team, Docente

## Requisitos Testeados

| FR/NFR | Test | Resultado | Comentario |
|--------|------|-----------|-----------|
| FR-01 | MQTT recibirá datos | ✅ PASS | Funcionando |
| FR-02 | Dashboard muestra datos | ✅ PASS | Rápido y claro |
| FR-03 | Alertas funcionan | ⚠️ PASS+FEEDBACK | Bien, pero agregar recomendación |
| NFR-01 | Latencia < 1s | ⚠️ FAIL | 1.2s, PO no lo considera bloqueador |
| NFR-02 | 99% uptime | ✅ PASS | Probado 100 requests sin caídas |

## Sign-Off
- Operador aprueba deployment a producción: **✅ SÍ**
- Feedback para mejoras: "Agregar recomendación de máquina problemática en alertas"

**Firmado:** Operador, Dev Lead, Docente
**Fecha:** 2026-10-15
```

### 5. Gaps: ¿Qué Falta?

Si hay requisito sin evidencia:

```markdown
# Gaps Identificados - Unidad 6

## Gap 1: NFR-01 Latencia
- Requisito: Latencia < 1s
- Medición: 1.2s
- Causa: Query de histórico es lenta
- Plan: Optimizar índice BD (Unidad 7 o futuro)
- Impacto: Operador dice "no es crítico para fase 1"

## Gap 2: FR-03 Detalle de Anomalía
- Requisito: Sistema alerta si consumo > 20% promedio
- Implementado: Sí, pero sin "cuál es la máquina"
- Feedback UAT: "Necesito saber de dónde viene el consumo"
- Plan: Agregar análisis de subcircuitos (Sprint 3)
- Impacto: Bloqueador para UAT formal

## Decisión
- Deployas FR-01, FR-02, NFR-02, NFR-03: ✅
- Pospones FR-03 detail y NFR-01 latency: Roadmap futuro
```

### 6. Matriz Final (Ejemplos: Portal)

```markdown
# Traceability Matrix - portal

| Req ID | Descripción | Test | Status | Demo | UAT | Owner |
|--------|-------------|------|--------|------|-----|-------|
| FR-01 | Listar 6 carreras | TC-01 | ✅ | ✅ | ✅ | Dev1 |
| FR-02 | Bot NLP responde | TC-02 | ✅ | ✅ | ⚠️ | Dev2 |
| FR-03 | Recomendador ML | TC-03 | ⚠️ | ⚠️ | ❌ | Dev3 |
| NFR-01 | < 2s respuesta | TC-04 | ✅ | ✅ | ✅ | Dev1 |
| NFR-02 | Responsive mobile | TC-05 | ⚠️ | ✅ | ⚠️ | Dev2 |
| NFR-03 | 99.5% uptime | TC-06 | ✅ | ⚠️ | TBD | Dev3 |

**Resumen:**
- ✅ PASS: 4
- ⚠️ CONDITIONAL: 2
- ❌ FAIL: 1

**Plan:** 
- Priorizar FR-03 (recomendador)
- Mobile responsive (minor)
- Uptime en producción
```

## Actividad Práctica

1. **Crear Traceability Matrix (Semana 14):**
   - Listar cada FR del SRS (Unidad 2)
   - Listar cada NFR
   - Para cada uno, mapear: Test case, status, demo, UAT

2. **Ejecutar UAT (Semana 14-15):**
   ```markdown
   # UAT Sign-Off Sheet
   
   **Proyecto:** [Tu proyecto]
   **Fecha:** [fecha]
   **PO Real:** [docente o stakeholder]
   **Dev Team:** [nombres]
   
   ## Requisitos
   [Tabla con FR/NFR y resultados]
   
   ## Sign-Off
   - ¿Aprueban deployment? SÍ / NO / CONDICIONAL
   - Comentarios / Feedback
   - Próximos pasos
   
   **Firmado por:** ...
   ```

3. **Documentar gaps en `VALIDATION_GAPS.md`:**
   - Qué falta
   - Por qué
   - Plan para resolver
   - Impacto en deployment

## Palabras clave

Traceability, Requirements Validation, Test Cases, UAT, User Acceptance, Sign-Off, Gap Analysis, FR, NFR

## Referencias

- spec § 5.5 (Validación)
- Plan Oficial § Referenciales (coherencia requisitos-conclusiones)
- IEEE Standard 829 (Test Documentation)
