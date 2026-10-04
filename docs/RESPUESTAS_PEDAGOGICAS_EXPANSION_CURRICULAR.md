# Respuestas Pedagógicas — Expansión Curricular

**Documento Formal — Octubre 2026**

Este documento responde de manera sistemática y fundamentada los 6 bloques de interrogantes que surgieron durante la auditoría pedagógica de la carrera Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial (ISFT N° 199), en relación a la expansión curricular de 3 a 6 técnicas especializadas.

**Fuente Normativa Primaria:** Anexo I, Resolución 2730-22 (Dirección General de Cultura y Educación — Provincia de Buenos Aires)

---

## BLOQUE A: Secuenciación y Correlatividades

### A.1 Orden de Enseñanza de las 3 Técnicas

El orden es estrictamente secuencial y no simultáneo:

- **Técnicas de Procesamiento del Habla** → 2° Año, 1er Cuatrimestre
- **Técnicas de Procesamiento Digital de Imágenes** → 3er Año, 2do Cuatrimestre

Esto significa que los estudiantes aprenden procesamiento del habla un año y medio antes de aprender visión artificial, permitiendo una maduración progresiva en complejidad algorítmica y manejo de datos multidimensionales.

### A.2 Correlatividades entre Nuevas Materias

**Técnicas de Procesamiento del Habla** no tiene prerrequisitos formales exigidos en el diseño curricular. No requiere tener aprobado "Procesamiento de Aprendizaje Automático" (PAA); de hecho, ambas conforman el mismo **Trayecto F**:

| Trayecto F | Cuatrimestre | Materia | Horas |
|-----------|--------------|--------|-------|
| F-1 | 2° Año, Q1 | Técnicas de Procesamiento del Habla | 7h |
| F-2 | 2° Año, Q2 | Procesamiento de Aprendizaje Automático (PAA) | 7h |

Las únicas correlatividades formales para el 3er año aplican a las Prácticas Profesionalizantes:

- **PP: Modelizado de Sistemas de IA** requiere: "Desarrollo de Sistemas de Inteligencia Artificial"
- **PP: Proyecto Integrador** requiere: "PP: Análisis y Exploración de Datos" + "PP: Modelizado de Sistemas de IA"

### A.3 Seminario de Actualización en la Arquitectura Curricular

El **Seminario de Actualización** es OBLIGATORIO:

- **Carga horaria:** 7 horas semanales (no comparte ni resta horas a otras materias)
- **Ubicación:** 3er Año, 1er Cuatrimestre
- **Trayecto:** I (misma docente que dicta Imágenes en 2do cuatrimestre)

Pedagogía: El Seminario actúa como "puente de herramientas" — enseña MLOps, versionado, deployment y buenas prácticas de ingeniería antes de que los estudiantes apliquen esos conceptos en el procesamiento de imágenes.

---

## BLOQUE B: Convergencia de Técnicas en Práctica Profesionalizante

### B.1 Integración Explícita: ¿Quién Enseña Qué en PP?

Según el Anexo, el objetivo de **"PP: Proyecto Integrador"** es que los estudiantes:

> "elaboren un proyecto de carácter integrador que contemple todos los aprendizajes adquiridos previamente y su transferencia a un recorte concreto de la realidad"

**Punto crítico:** La PP no enseña las técnicas desde cero. Transfiere y articula conocimientos previos adquiridos en:
- Técnicas de Procesamiento del Habla (2° año)
- Procesamiento de Aprendizaje Automático (PAA, 2° año)
- Seminario de Actualización (3er año, Q1)
- Técnicas de Procesamiento Digital de Imágenes (3er año, Q2 — cursando simultáneamente)

### B.2 Dos Prácticas Profesionalizantes Obligatorias (no una)

Ambas coexisten en el 3er año y son secuenciales:

| Trayecto J | Cuatrimestre | Materia | Enfoque | Horas |
|-----------|--------------|--------|---------|-------|
| J-1 | 3er Año, Q1 | PP: Modelizado de Sistemas de IA | Arquitectónico/Conceptual | 4h |
| J-2 | 3er Año, Q2 | PP: Proyecto Integrador | Práctico/Aplicativo | 4h |

**PP: Modelizado** → Diseño de sistemas expertos, representación del conocimiento, grafos, árboles, razonamiento basado en reglas.

**PP: Proyecto Integrador** → Aplicación end-to-end, transferencia a caso real (ej. monitoreo de drones, procesamiento multimodal).

Mismo docente dicta ambas (Trayecto J).

---

## BLOQUE C: Cargas Horarias y Semestralización

### C.1 ¿Hay Espacio Horario para 6 Materias en 3er Año?

**Sí.** El cálculo es exacto. 3er Año = **480 horas reloj anuales = 15 horas semanales**.

**1er Cuatrimestre (15h/semana):**
- Gestión de Proyectos: 2h
- Seminario de Actualización: 7h
- PP: Modelizado de Sistemas de IA: 4h
- Tecnología y Ambiente: 2h
- **Total: 15h**

**2do Cuatrimestre (15h/semana):**
- Taller de Comunicación: 2h
- Técnicas de Procesamiento Digital de Imágenes: 7h
- PP: Proyecto Integrador: 4h
- Trabajo, Tecnología y Sociedad: 2h
- **Total: 15h**

### C.2 Régimen: Cuatrimestral (no anual)

Todas las materias de la carrera son estrictamente **cuatrimestrales**. La carrera se organiza en 11 "trayectos anuales", pero cada trayecto contiene "dos unidades curriculares que se cursan y acreditan cuatrimestralmente de manera independiente".

Implicación: Un estudiante puede aprobar Q1 y recursar Q2 sin perder lo aprendido en Q1.

---

## BLOQUE D: Criterios de Éxito y Evaluación

### D.1 ¿Qué Significa "Integración Exitosa"?

El Anexo **no impone una métrica dura** (ej. "uso obligatorio de CNN + LSTM + transformers"). Los referenciales de evaluación exigen:

> "presentación y defensa del proyecto llevado a cabo"

Criterios cualitativos y metodológicos:
1. **Originalidad** del trabajo
2. **Lógica del planteo** (problema bien definido)
3. **Metodología apropiada** (técnicas justificadas, no solo acumuladas)
4. **Calidad de elaboración** (código, documentación, testing)
5. **Coherencia** entre hipótesis, datos y conclusiones
6. **Documentación aportada** (reportes, análisis, lecciones)

### D.2 Evaluación Diferenciada: Modelizado vs. Proyecto Integrador

**En PP: Modelizado** (1er cuatrimestre):
- Evaluación **técnica y algorítmica**
- ¿Cómo representan el problema? (grafos, árboles, reglas)
- ¿Identifican limitaciones del sistema experto?
- ¿Seleccionan correctamente los procedimientos de búsqueda?
- Énfasis: diseño arquitectónico y formalización lógica

**En PP: Proyecto Integrador** (2do cuatrimestre):
- Evaluación **integradora y aplicativa**
- ¿Funciona end-to-end en un caso real?
- ¿Coherencia entre hipótesis y resultados?
- ¿Viabilidad frente a problemática real?
- ¿Responsabilidad legal, social y metodológica del proyecto?
- Énfasis: aplicación práctica, transferencia al contexto

---

## BLOQUE E: Riesgos Pedagógicos de la Expansión

### E.1 Equidad de Acceso a Recursos: Figura de "Trayecto"

En lugar de contratar 6 docentes especializados aislados, el Anexo estructura la cobertura por **Trayectos**:

| Trayecto | Q1 2° Año | Q2 2° Año | Q1 3° Año | Q2 3° Año |
|----------|-----------|-----------|-----------|-----------|
| **F** | Habla (7h) | PAA (7h) | — | — |
| **I** | — | — | Seminario (7h) | Imágenes (7h) |
| **J** | — | — | PP Modelizado (4h) | PP Integrador (4h) |

**Ventaja:** Continuidad pedagógica. El docente de Trayecto I que enseña MLOps en el Seminario es el mismo que luego exige su aplicación en Procesamiento de Imágenes.

### E.2 Sincronización Docente: Gobernanza Faltante

El Anexo **no formaliza una figura de "Coordinador de Carrera"** o "Junta de Cátedra". La coordinación interdisciplinaria se delega a:

1. **Trayectos (interno):** Un docente articula sus 2 materias (responsabilidad clara)
2. **Inter-trayectos:** "Acuerdos entre la/el docente y las autoridades de la institución educativa"

**Riesgo:** La sincronización entre Trayectos (ej. docente de Imágenes coordinando con docente de PP Integrador para casos de estudio multimodales) **depende exclusivamente de la gestión directiva del instituto**, no de un mecanismo formal.

**Mitigación recomendada:** Establecer una Coordinación de Carrera que facilite: reuniones cuatrimestrales, definición de proyectos integradores, compartición de laboratorios, cronograma de entregas.

---

## BLOQUE F: Transición Actual → Futuro

### F.1 y F.2: Obligatoriedad, No Expansión Futura

De acuerdo al documento normativo (Anexo I Res 2730-22):

> "los espacios de Habla, Seminario, PP Modelizado e Imágenes constituyen el plan de estudios obligatorio base de la carrera"

**Conclusión:** Estas **no son materias de expansión futura ni electivas**. Son parte del currículum normativo obligatorio sancionado por la Provincia de Buenos Aires (DGCyE, Región 6).

### F.2 Coexistencia Obligatoria de Ambas PP

**PP: Modelizado de Sistemas de IA** no reemplaza a **PP: Proyecto Integrador**; ambas:

- ✅ Coexisten obligatoriamente en 3er año
- ✅ Suman **128 horas totales de prácticas profesionalizantes** en ese ciclo (4h/semana × 16 semanas × 2 cuatrimestres)
- ✅ Pertenecen al mismo Trayecto (J), mismo docente

**Implicación crítica:** La ausencia de dictado de estas materias en una cohorte actual no representa una "transición pedagógica programada", sino un **recorte del diseño curricular obligatorio de la Provincia de Buenos Aires**.

---

## Anexos Complementarios

- **Procedimiento de Calibración de Duraciones:** `PROCEDIMIENTO_CALIBRACION_DURACIONES.md`
- **Proyecto de Cátedra PAA:** `PROYECTO_CATEDRA_PAA.md`
- **Estructura de Trayectos:** `estructura-trayectos.md`

---

**Documento Preparado:** Octubre 2026  
**Estado:** Formal — Referencial normativo para la institución
