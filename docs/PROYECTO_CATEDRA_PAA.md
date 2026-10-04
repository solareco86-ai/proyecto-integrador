# Proyecto de Cátedra: Procesamiento de Aprendizaje Automático (PAA)
## Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial — ISFT N° 199

**Docente:** Agustín Bustos  
**Asignatura:** Procesamiento de Aprendizaje Automático (PAA)  
**Resolución de Aprobación:** DGCyE N° 273/22  
**Año de Dictado:** 2do año de carrera  
**Régimen:** Cuatrimestral (16 semanas)  
**Carga Horaria:** 64 horas reloj (4 horas semanales)  
**Modalidad:** Presencial, Turno Vespertino (18:00–22:30)  

**Fecha de Presentación:** 2 de octubre de 2026  
**Versión:** 1.0 (Alineada a Anexo 1 DGCyE + GitHub)

---

## 1. Fundamentación Pedagógica

### 1.1 Contexto Institucional

La Tecnicatura en Ciencia de Datos e IA forma profesionales capacitados para "liderar el ciclo de vida de los datos: desde extracción, limpieza e ingeniería de características, hasta modelado predictivo, visualización ejecutiva y puesta en producción (MLOps) de soluciones basadas en IA" (Anexo 1, perfil de egreso).

PAA es la materia que **cierra la transición de programación fundamental (Año 1) hacia especialización en ML (Año 2–3)**. Su ubicación en el 2do año asume que estudiantes ya dominan:
- Álgebra lineal (matrices, vectores, sistemas de ecuaciones)
- Probabilidad y estadística (distribuciones, Teorema de Bayes)
- Programación en Python (funciones, estructuras de datos, testing)

### 1.2 Enfoque Pedagógico: Contextualización con Caso Real

Toda enseñanza en PAA está anclada en **energy-ml** (https://github.com/datamaq-automation/energy-ml), un sistema real de monitoreo no intrusivo de cargas eléctricas (NILM). 

**Beneficios:**
- Estudiantes ven relevancia inmediata ("esto se usa en producción")
- Problemas son auténticos, no juguetes académicos
- Código escrito en laboratorio es reutilizable en proyecto final (PP)

### 1.3 Filosofía: Pedagogía Sobre Tecnología

Las herramientas de IA agéntica (OpenCode, Aider, Claude Code, etc.) son **medios, no fines**. La enseñanza prioriza:
1. **Conceptos profundos** (probabilidad, geometría, lógica) antes de sintaxis
2. **Rigor matemático** (¿por qué funciona Bayes?) antes de "copy-paste"
3. **Responsabilidad ética** (sesgo, privacidad) integrada, no marginal
4. **Autonomía del estudiante** (sé crítico con IA, no confíes ciegamente)

---

## 2. Estructura Curricular

### 2.1 Unidades y Horas

| Unidad | Nombre | Horas | Semanas | Descripción |
|---|---|---|---|---|
| **Unidad 0** | Diagnóstico de Correlatividades | 2 | 1 sem. | Autoevaluación de requisitos previos (Año 1) |
| **Unidad 1** | Fundamentos (Terminal, Git, APIs) | 22 | 5–6 sem. | Entorno profesional, control de versiones, FastAPI |
| **Unidad 2, Parte I** | Inferencia Estadística (Bayes, k-NN) | 20 | 5 sem. | Probabilidad, algoritmos clásicos, evaluación |
| **Unidad 2, Parte II** | Inteligencia Neuro-Simbólica (CART, MCP) | 16 | 4 sem. | Árboles, reglas formales, servidores MCP |
| **Evaluación + Ajuste** | Recuperaciones, finales | 4 | 1 sem. | Buffers para reprogramaciones |
| **TOTAL** | | 64 h | 16 sem. | |

### 2.2 Distribución de Horas por Tipo

```
Horas Totales: 64 reloj
├─ Lectura/Exposición (teórica): ~12h (19%)
├─ Laboratorio práctico (código): ~32h (50%)
├─ Evaluación formativa (quizzes, autoevaluación): ~10h (16%)
├─ Evaluación sumativa (parciales, final): ~6h (9%)
└─ Espacios flexibles (dudas, repasos, recuperación): ~4h (6%)
```

---

## 3. Decisiones Micro-Didácticas Fundamentadas

### 3.1 Duración de Lecciones (25–50 min)

**Decisión:** Cada lección dura 25–50 minutos (cronometrada con estudiantes reales).

**Fundamentación (Cognitive Load Theory, Sweller):**
- Ventana de atención sostenida: 20–25 minutos
- Lecciones < 20 min: fragmentación innecesaria
- Lecciones > 50 min: sobrecarga cognitiva
- Mix de duraciones evita monotonía

**Procedimiento de Calibración:**
- Dictar lección con cronómetro
- Registrar en YAML: `duration: 25 min`
- Encuesta post-lección: "¿fue suficiente? ¿quedó clara?"
- Ajustar próxima cohort basado en feedback

### 3.2 Orden de Enseñanza: Desde Herramientas Hacia Conceptos

**Decisión:** Unidad 1 (Fundamentos técnicos) ANTES de Unidad 2 (Matemática).

**Fundamentación (Constructivismo):**
- Estudiantes necesitan **entorno seguro** (Git, testing) antes de arriesgar código en experimentos
- Herramientas son scaffolds (andamios) que permiten praxis
- Detrás: filosofía "learn by doing" (Dewey)

**Potencial Crítica:** "¿Por qué enseñar OpenCode/Aider antes de Bayes?"  
**Respuesta:** Porque en 2do año, estudiantes programan con asistentes de IA. Es realidad del mercado laboral. Enseñar sin contexto de herramientas es anacrónico.

### 3.3 Mapa Conceptual Previo a Algoritmos Aislados

**Decisión:** Capítulo introductorio en Unidad 2 presenta "Mapa de Bayes → k-NN → CART".

**Fundamentación (Teoría de Ausubel - Aprendizaje Significativo):**
- Antes de aprender A, establece cómo A se conecta con B, C, D
- Evita "islas de conocimiento" desconectadas
- Reduce carga cognitiva posterior

---

## 4. Estrategia de Evaluación Formativa

### 4.1 Autoevaluaciones Integradas en Lecciones

**Decisión:** Cada lección tiene 3–5 preguntas conceptuales al cierre + "Code Review Inverso".

**Fundamentación (Formative Assessment, Black & Wiliam):**
- Feedback frecuente (no esperar al parcial)
- Estudiantes auto-regulan: "¿Entendí?"
- Baja ansiedad (no calificadas)

**Ejemplo (cap-3-1-bayes):**
```
## Autoevaluación Formativa
1. ¿Por qué Bayes es especialmente útil para diagnóstico 
   de fallas frente a otros algoritmos?
   → Respuesta comentada en lección

2. Caza de Código Alucinado: [Código erróneo de IA]
   → Identifica el error (falta divisor de Bayes)
```

### 4.2 Parciales y Finales

**Decisión:** 
- 1 parcial acumulativo (Unidad 1–2 Parte I)
- 1 final integrador (Unidad 1–2 completa)
- Ambos 80% código práctico, 20% teórico

**Formato:**
- Presencial, 2 horas
- Laptop permitida (simula realidad profesional)
- Tema: extender energy-ml o nuevo dataset de energía
- Rúbrica: correctitud + claridad + documentación

---

## 5. Inclusión y Atención a Diversidad

### 5.1 Estudiantes con Ritmo Lento

**Acción:** 
- Diagnóstico inicial (Unidad 0) detecta brechas
- Rutas de recuperación: "Si no entiendes X, repasa [recurso]"
- Tutorías extra (martes 15:00, previa coordinación)
- Extensión de plazos con justificación

**Fundamento:** Inclusión no es "bajar exigencia", es "proporcionar andamios".

### 5.2 Estudiantes con Ritmo Rápido

**Acción:**
- Extensiones (lección 5.5 Comparación de Modelos es "avanzada")
- Proyectos paralelos: implementar 5to algoritmo (SVM, Random Forest)
- Investigación: "¿Cómo funcionan agentes de IA?" (Cap 4.x)

### 5.3 Diversidad de Géneros

**Acción:**
- Ejemplos en energy-ml no asumen género (ninguno)
- Caso de estudio en ética: sesgo de género en ML (lección 2.0)
- Clase inclusiva: lenguaje neutro ("Técnico/a", "estudiante")

### 5.4 Accesibilidad Digital

**Acción (a mejorar):**
- Todas las lecciones markdown → fácil screen reader
- Videos (si hubiera) tendrían subtítulos
- Código con comentarios claros, no "críptico"

---

## 6. Articulación con Otros Espacios

### 6.1 Con Año 1

**Técnicas de Programación** enseña testing (pytest).  
**Elementos de Análisis Matemático** enseña matrices.  
**Estadística y Probabilidades** enseña Bayes.

→ PAA asume dominio. No re-enseña. Construye sobre base.

### 6.2 Con Año 2–3 (Vertical)

**PAA Unidad 2** prepara para:
- **Procesamiento Digital de Imágenes** (3er año): OCR + modelos visuales
- **Prácticas Profesionales** (3er año): Proyecto integrador con Bayes/k-NN
- **Seminario de Actualización** (3er año): MLOps, Docker, CI/CD

### 6.3 Con "Ciencia de Datos" (Trayecto G)

**Ciencia de Datos** enseña ética, privacidad, gobernanza (Trayecto G, 2do año).  
**PAA** integra ética desde Cap 2.0.

→ Convergencia intencional, no duplicación.

---

## 7. Criterios de Evaluación (Referenciales DGCyE)

El Anexo 1 exige que graduados demuestren:

| Referencial | Evidencia en PAA |
|---|---|
| "Aplicación de técnicas de aprendizaje automático" | Laboratorios Cap 3–5: implementar Bayes, k-NN, CART en energy-ml |
| "Validación y verificación de modelos" | Unidad 2 Cap 5: matriz de confusión, F1-score, cross-validation |
| "Comparación y selección de modelos" | Lección 5.5: tabla comparativa, criterios por contexto |
| "Interpretabilidad y explicabilidad" | Lección 2.0 (ética) + 5.5 (reglas de CART) |
| "Responsabilidad ética y privacidad" | Lección 2.0: sesgo, consentimiento, differential privacy |

---

## 8. Uso Responsable de IA Agéntica

### 8.1 Herramientas Permitidas

- **OpenCode** (gratuito): asistencia de código
- **Aider** ($5/mes estudiantil): pair programming
- **Claude Code** (corporativo): si institución da acceso
- **ChatGPT / Claude** (APIs): para investigación

### 8.2 Límites Éticos

**Prohibido:**
- ❌ Copiar soluciones de IA sin entender
- ❌ Usar IA para cometer fraude académico
- ❌ Confiar ciegamente en salida de modelo

**Esperado:**
- ✅ Leer código generado, cambiar, debuggear
- ✅ Entender POR QUÉ funciona/no funciona
- ✅ "Code review inverso": auditar propuestas de IA
- ✅ Citar fuente: "Este código fue generado con Aider, luego ajusté..."

### 8.3 Lección Explícita: "Caza de Código Alucinado"

**Cap 2 (en Unidad 1):** Cada lección práctica incluye "Código Erróneo Propuesto por IA". Estudiantes deben:
1. Ejecutar código (¿falla?)
2. Leer línea por línea (¿qué está mal?)
3. Proponer corrección
4. Entender por qué IA alucinó

**Beneficio:** Estudiantes son críticos, no dóciles con IA.

---

## 9. Documentación y Registro de Mejoras

### 9.1 Bitácora de Clase

Después de cada clase, registrar:
- ¿Qué funcionó bien?
- ¿Qué fue confuso?
- ¿Cuánto tiempo tomó realmente (vs. planeado)?
- Cambios recomendados

**Archivo:** `/docs/bitacora-paa-2026.md` (privado del docente)

### 9.2 Feedback de Estudiantes

- Encuesta anónima: "¿Claridad de lección?" (1–5)
- Pregunta abierta: "¿Qué no entendiste?"
- Reuniones 1-1: estudiantes con dificultades

### 9.3 Mejora Continua

Cada ciclo lectivo:
1. Compilar feedback + bitácora
2. Ajustar duraciones de lecciones
3. Reescribir lecciones confusas
4. Agregar nuevos casos de estudio

---

## 10. Recursos y Dependencias

### 10.1 Tecnológicos

- **Laptop:** 1 por estudiante (Python 3.12+)
- **Internet:** Estable para descargar librerías
- **GitHub:** Cuenta para repositorio de laboratorios
- **Editor:** VS Code / PyCharm (libres)
- **Bibliotecas:** NumPy, Scikit-Learn, Pandas (pip install)

### 10.2 Humanos

- **Docente PAA:** 1 (el suscripto)
- **Jtp/Ayudante:** Deseable (no disponible actualmente)
- **Tutorías:** Profesor en horario extra (martes 15:00)

### 10.3 Espacios

- **Aula:** Equipada con proyector + WiFi
- **Laboratorio:** Aula normal con sillas movibles
- **Oficina de consulta:** Aula 12 (martes)

---

## 11. Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|---|---|---|---|
| Estudiantes sin laptop | Media | Alta | Sala de PC acceso fuera horario |
| Falta de correlatividades (Año 1) | Media | Alta | Unidad 0: diagnóstico + recuperación |
| Sobrecarga con herramientas de IA | Media | Media | Lección 2.0 (Cap 2): reflexión crítica |
| Cobertura de 64h insuficiente | Baja | Media | Seminario de Actualización cubre "nuevas técnicas" |
| Equipo débil (lag, desconexiones) | Media | Baja | Repositorio GitHub local es backup |

---

## 12. Evaluación de Este Proyecto de Cátedra

**Este documento será revisado:**
- Fin de octubre 2026 (post-parcial)
- Fin de diciembre 2026 (post-final)
- Próxima cohorte (2027): ajustes implementados

**Criterios de éxito:**
- ✅ >= 85% de estudiantes aprueban PAA
- ✅ Feedback promedio de claridad >= 4/5
- ✅ Estudiantes pueden explicar por qué Bayes != k-NN
- ✅ Proyecto integrador (PP) usa técnicas de PAA

---

## Firma y Aprobación

**Elaborado por:** Agustín Bustos, Docente PAA  
**Fecha:** 2 de octubre de 2026  
**Versión:** 1.0

Según Anexo 1 DGCyE, cada docente debe presentar proyecto de cátedra al concursar. Este documento funda la cátedra de PAA en base a:
- ✅ Análisis de diseño curricular oficial
- ✅ Experiencia pedagógica (Bloom, Ausubel, Sweller)
- ✅ Prácticas de educación superior argentina
- ✅ Realidad del mercado laboral en ciencia de datos

---

**Anexos (referencias):**
- Anexo 1: Diseño Curricular DGCyE Resolución N° 273/22
- Anexo 2: Syllabus detallado (lecciones por semana)
- Anexo 3: Rúbricas de evaluación (Prácticas Profesionales)
- Anexo 4: Bitácora de clase (2026)
