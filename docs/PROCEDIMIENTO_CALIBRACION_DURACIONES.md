# Procedimiento: Calibración de Duraciones de Lecciones

**Objetivo:** Ajustar los tiempos estimados (`duration: XX min` en YAML) basado en datos reales de estudiantes.

**Responsable:** Docente de PAA  
**Frecuencia:** Post-clase (inmediato) + compilación post-cohorte  

---

## 1. Registro en Clase (Inmediato)

### Paso 1.1: Marcar Hora de Inicio/Fin

```
Lección: cap-3-1-teorema-bayes-clasificacion.md
Duración planificada: 25 min

Hora inicio: 18:05
Hora fin: 18:33
Duración real: 28 min

Observaciones: 
- Estudiante A preguntó sobre Bayes 3 veces (confusión)
- Demoré 2 min extra en explicación
- Grupo rápido: podrían haber avanzado en 22 min
```

### Paso 1.2: Clasificar Grupo Objetivo

```
Velocidad del grupo (1-5):
  1 = muy lento (15%+ atrasados)
  3 = normal
  5 = muy rápido (avanza sin dudas)

Retroalimentación: 3 (normal, 1 pregunta de confusión)
```

### Paso 1.3: Notas de Mejora

```
Que no funcionó:
- Ejemplo de transformador fue confuso
- Notación matemática pequeña (projetor)

Que sí funcionó:
- Case study energy-ml: aclaró el concepto
- Analogía "firewall protege como Bayes" fue efectiva
```

---

## 2. Compilación Post-Cohorte

### Paso 2.1: Recolectar Datos

Crear tabla en `/docs/bitacora-paa-2026.md`:

```markdown
## Calibración de Duraciones — Cohorte 2026

| Lección | Planif. | Real | Grupo | Obs. |
|---|---|---|---|---|
| cap-3-1-bayes | 25m | 28m | Normal | Confusión en notación |
| cap-4-1-knn | 25m | 22m | Rápido | Avanzó bien |
| cap-5-5-comparacion | 40m | 45m | Lento | Demasiado contenido |
| **Promedio** | | **31.7m** | | |
```

### Paso 2.2: Calcular Ajuste

```
Si duraciones reales > planificadas:
  → Agregar 3–5 min al YAML (para próxima cohorte)

Si duraciones reales < planificadas:
  → Reducir 2–3 min (o agregar profundización)

Umbral de cambio: >10% diferencia respecto a lo planificado
```

**Ejemplo:**
```
cap-5-5-comparacion:
  Planificado: 40 min
  Real: 45 min (112.5% de lo planificado)
  Diferencia: +5 min > 10% threshold
  → Acción: Actualizar YAML a 45 min
```

---

## 3. Factores de Contexto

### 3.1 Grupo Poblacional

Diferentes grupos pueden necesitar duraciones distintas:

```
Grupo Rápido (Cohort 2025, TI previo):
  - cap-3-1-bayes: 22 min → YAML: 23 min

Grupo Lento (Cohort 2026, sin TI previo):
  - cap-3-1-bayes: 28 min → YAML: 30 min

Solución: Mantener un YAML flexible
  duration: "25-30 min (según cohort)"
  OR crear variantes por nivel
```

### 3.2 Hora del Día

Lecciones al final del turno vespertino (21:30–22:30) tienden a ser más lentas:
- Fatiga acumulada
- Concentración reducida

**Mitigación:**
```
Lecciones pesadas (mucha matemática) → 18:00–19:30 (inicio)
Lecciones prácticas (código) → 19:30–21:00 (medio)
Lecciones ligeras (reflexión) → 21:00–22:30 (fin)
```

---

## 4. Herramienta: Cronómetro de Clase

### 4.1 Formato Simple

Usar Google Sheets compartido:

```
Clase | Fecha | Lección | Planif. | Real | Grupo | Notas |
------|-------|---------|---------|------|-------|-------|
1     | Oct-2 | Cap 1.1 | 25m     | 23m  | Norm  | OK    |
2     | Oct-9 | Cap 1.2 | 25m     | 27m  | Norm  | + pre |
3     | Oct-16| Cap 2.0 | 35m     | 38m  | Lento | Ética |
```

### 4.2 Automatización (Opcional)

Si usas GitHub Issues:

```
[Cronómetro] cap-3-1-bayes
- Fecha: Oct 23, 2026
- Planificado: 25 min
- Real: 28 min
- Grupo: Normal
- Notas: Confusión en notación. Sugerir ejemplo visual.
- Acción: Aumentar a 30 min + agregar diagrama.

Label: calibration
```

---

## 5. Decisiones y Documentación

### 5.1 Cambios en YAML

Cuando decidas ajustar duración:

```yaml
# ANTES
- type: lesson
  id: les-paa-int-3-1
  slug: paa-int-teorema-bayes-clasificacion
  title: '3.1 Teorema de Bayes...'
  duration: 25 min
  content_file: cap-3-1-teorema-bayes-clasificacion.md

# DESPUÉS (con razón)
- type: lesson
  id: les-paa-int-3-1
  slug: paa-int-teorema-bayes-clasificacion
  title: '3.1 Teorema de Bayes...'
  duration: 30 min  # ← Ajustado post-calibración (Cohorte 2026: real 28–32 min)
  content_file: cap-3-1-teorema-bayes-clasificacion.md
```

### 5.2 Bitácora de Docente

Mantener archivo privado `/docs/bitacora-paa-2026.md`:

```markdown
## Lección Cap 3.1 — Calibración

**Fecha de dictado:** 23 de octubre, 2026  
**Grupo:** Normal (1 confusión, 1 pregunta extra)  
**Duración planificada:** 25 min  
**Duración real:** 28 min  
**Diferencia:** +3 min (112%)  

### Observaciones
- Confusión en notación P(A|B) — estudiante preguntó 3x
- Ejemplo energy-ml fue clarador
- Laboratorio práctico fue rápido (skipped algunos detalles)

### Cambios para próxima cohorte
- [ ] Agregar 5 min al YAML
- [ ] Ejemplificar más P(A|B) antes de introducir
- [ ] Simplificar tabla de 4 términos bayesianos

### Feedback estudiantes
- "Claro pero rápido" (3 votos)
- "Necesito más ejemplos" (2 votos)
- "Bien estructurado" (5 votos)

**Decisión:** Ampliar a 30 min + agregar 1 ejemplo visual.
```

---

## 6. Ciclo Anual de Mejora

```
Año 1 (Cohorte 2026)
├─ Octubre: Recolectar duraciones Cap 1–2
├─ Noviembre: Recolectar duraciones Cap 3–5
├─ Diciembre: Compilar datos + análisis
├─ Enero 2027: Actualizar YAML para Cohorte 2027
└─ Objetivo: 70–80% de lecciones con ±5% de diferencia

Año 2 (Cohorte 2027)
├─ Validar ajustes (¿mejoraron?)
├─ Agregar lecciones nuevas + calibrarlas
├─ Recolectar nuevo feedback
└─ Iterar...
```

---

## 7. Reglas Simples

| Caso | Acción |
|---|---|
| Real < Planif. (p. ej. 22 min vs. 25 min) | Reducir 2–3 min O agregar actividad |
| Real = Planif. ± 3 min | Mantener, sin cambios |
| Real > Planif. + 5 min | Aumentar duración Y revisar contenido |
| Real >> Planif. + 15 min | Problema: contenido es denso. Partir en 2 lecciones. |

---

## 8. Responsabilidad

- **Docente:** Cronometrar + anotar observaciones (inmediato)
- **Coordinador de carrera:** Revisar datos post-cohorte (enero)
- **Comité curricular:** Aprobar cambios en YAML para próxima cohorte (febrero)

---

## Plantilla Quick Reference

```
FECHA: _______________
LECCIÓN: _______________
PLANIFICADO: _____ min
REAL: _____ min
GRUPO: 1 2 3 4 5 (círcular)
OBSERVACIONES:
□ Confusión (dónde: ________________)
□ Estudiante lento
□ Estudiante rápido
□ Proyecto funcionó bien
□ Proyecto falló
□ Necesito ajustar contenido

ACCIÓN RECOMENDADA:
□ Aumentar duración
□ Reducir duración
□ Agregar ejemplo
□ Partir en 2 lecciones
□ Cambiar orden
□ Nada (mantener)
```

---

**Versión:** 1.0  
**Aprobado por:** Agustín Bustos (Docente PAA)  
**Fecha de entrada en vigencia:** Cohorte 2026
