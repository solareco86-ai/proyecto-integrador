# 4.2 User Stories y Planning Poker: Estimación de Trabajo

## Objetivo

Convertir requisitos funcionales (FR) en User Stories. Estimar complejidad relativa con Planning Poker. Entender qué hace una buena historia.

## Referencia

**spec:** § Product Backlog (formato de US, criterios de aceptación)

**Plan Oficial:** § Análisis de requisitos, clasificación de requerimientos

## Contenidos

### 1. Formato de User Story (US)

Una User Story NO es un requisito técnico; es **un compromiso de valor para un usuario**.

**Plantilla estándar:**
```
Como [rol/actor]
Quiero [funcionalidad]
Para [beneficio/por qué]

Criterios de Aceptación (CA):
- CA1: [Condición específica]
- CA2: [Otra condición]
- CA3: [Caso límite]

Notas:
- Dependencias (si necesita otra US)
- Datos de ejemplo
```

**Ejemplo 1 (energy-ml):**
```
Como operador de institución
Quiero ver consumo eléctrico en tiempo real en dashboard
Para detectar anomalías y evitar facturas sorpresa

CA:
- Dashboard actualiza cada 1 minuto
- Muestra kW actual vs promedio histórico
- Alerta si consumo > 20% del promedio
- Soporta 3+ años de datos históricos

Notas:
- Depende de: US-02 (integración con sensores MQTT)
- Datos de ejemplo: consumo promedio = 50 kW
```

**Ejemplo 2 (portal ISFT):**
```
Como alumno
Quiero ver listado de carreras disponibles con descripción
Para elegir la carrera que mejor se ajuste a mí

CA:
- Listar 6 carreras (Ciencia de Datos, Mecatrónica, Logística, HST, RRHH, Turismo)
- Cada carrera: nombre, duración, requisitos de ingreso, % de inserción laboral
- Filtro por área (técnica, humanística)
- Responsive en celular

Notas:
- No depende de nada, puede ser Sprint 1
```

### 2. Story Points vs Horas

**NO estimamos en horas.** Estimamos en "complejidad relativa" con **Story Points** (Fibonacci: 1, 2, 3, 5, 8, 13, 21, 40).

**¿Por qué?**
- Horas son imprecisas: "¿8 horas? Suena bien, pero qué pasa si hay sorpresas?"
- Story Points reflejan: complejidad + incertidumbre + dependencias
- Ejemplo:
  - "Agregar campo email" = 2 puntos (simple, predecible)
  - "Validar email con confirmación" = 5 puntos (lógica de validación, email send, retries)
  - "Entrenar modelo de ML" = 13 puntos (data prep, training, tuning, evaluación)

**Escala Fibonacci:**
- 1 pt: trivial (30 min max)
- 2 pt: simple (< 1 día)
- 3 pt: pequeña (1 día)
- 5 pt: media (2-3 días)
- 8 pt: grande (1 semana)
- 13 pt: muy grande (dividir en historias más pequeñas)
- 21+ pt: demasiado grande, DEBE dividirse

### 3. Planning Poker: Ceremonia de Estimación

**Participantes:** PO + Team

**Proceso (30 min para ~10 historias):**

1. **PO presenta historia:** Lee la US, responde preguntas (5 min)
   - "¿Qué es el 20% de anomalía?"
   - "¿Qué pasa si sensor está offline?"

2. **Team piensa en silencio:** ¿Qué complejidad? (2 min)

3. **Revelar simultáneamente:** Cada uno muestra su carta
   - Ejemplo: SM=5, Dev1=3, Dev2=8
   - Si hay outliers (5 y 8), los extremos explican (2 min)

4. **Re-estimar si fue diferente:** Después de explicar, revelan de nuevo
   - Típicamente convergen a 5 o 8

5. **Documentar:** Histora + puntos + fecha

**Ejemplo Planning Poker (energy-ml):**

```
US-01: Ver consumo en tiempo real
PO: "Operador ve dashboard con consumo ahora vs promedio"

Team piensa...

SM: 5 (simple, backend ya existe)
Dev1: 8 (no sé cuánto toma integrar MQTT)
Dev2: 5 (similar a otras dashboards)

SM explica: "Backend solo retorna JSON, UI lo dibuja"
Dev1 explica: "¿Quién maneja la conexión MQTT? ¿Nosotros o docente?"

PO aclara: "Sensores ya están configurados. Ustedes reciben JSON."

Nueva estimación: Dev1 cambia a 5.
Resultado: 5 puntos
```

### 4. Ejemplos: Energy-ML

| US-ID | Descripción | CA | Puntos |
|-------|-------------|----|----|
| US-01 | Ver consumo real en dashboard | Actualiza c/1 min, alertas | 5 |
| US-02 | Integrar sensores MQTT | Recibe JSON, loguea, almacena | 8 |
| US-03 | Entrenar modelo predicción | RMSE < 10%, retraining semanal | 13 |
| US-04 | Detectar anomalías | Compara predicción vs real, alerta | 8 |
| US-05 | Exportar reportes (CSV) | Descarga datos últimos 3 meses | 5 |

**Total Sprint 1:** 5 + 8 = 13 puntos (US-01, US-02)
**Total Sprint 2:** 13 + 8 + 5 = 26 puntos (pero solo hacemos ~12, priorizamos US-03 + US-04)

### 5. Ejemplos: Portal Institucional

| US-ID | Descripción | CA | Puntos |
|-------|-------------|----|----|
| US-01 | Listar carreras | 6 carreras, filtro área, responsive | 3 |
| US-02 | Bot de consultas NLP | Entiende intención, responde | 13 |
| US-03 | Recomendador de carrera | ML sugiere carrera por perfil | 13 |
| US-04 | Mostrar plan de estudios | Materias por cuatrimestre, correlatividades | 8 |
| US-05 | Sistema de login | Alumno se autentica, accede a datos | 8 |

**Total Sprint 1:** 3 + 8 = 11 puntos (US-01, US-05: setup básico)
**Total Sprint 2:** 13 + 13 = 26 puntos (pero solo 12, priorizamos US-02 + parte de US-03)

### 6. Buena Historia vs Mala Historia

**MALA:** "Hacer OCR"
- ¿Quién se beneficia?
- ¿Por qué lo quiere?
- ¿Cuándo está "hecho"?

**BUENA:** "Como operador quiero extraer números de facturas escaneadas para validar contra medidor, para detectar discrepancias. CA: OCR extrae 95%+ de números correctos, maneja PDFs de 10 años atrás."

## Actividad Práctica

1. **Convertir FR de Unidad 2 en US:**
   - Tomar cada requisito funcional (ej: FR-01, FR-02...)
   - Escribir formato completo de US con CA

2. **Estimar con Planning Poker:**
   - Equipo reúne 20-30 historias
   - Facilitar Planning Poker (SM dirige)
   - Documentar en `USER_STORIES.md`:
   ```markdown
   # Product Backlog - User Stories

   ## US-01: Ver consumo real en tiempo real
   **Como** operador de institución
   **Quiero** ver consumo eléctrico en dashboard
   **Para** detectar anomalías

   **Criterios de Aceptación:**
   - [ ] Dashboard actualiza c/1 min
   - [ ] Muestra kW actual vs promedio histórico
   - [ ] Alerta si consumo > 20% del promedio

   **Story Points:** 5
   **Prioridad:** Must Have
   **Sprint:** Sprint 1
   ```

3. **Priorizar con MoSCoW:** (veremos en 4.3)

## Palabras clave

User Story, Planning Poker, Story Points, Criterios de Aceptación, Fibonacci, Estimación relativa

## Referencias

- Mike Cohn, "User Stories Applied"
- Mountain Goat Software: Planning Poker
- spec § Product Backlog
