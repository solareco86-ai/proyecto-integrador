# Estructura de Trayectos: Procesamiento de Aprendizaje Automático

## Descripción General

El curso **Procesamiento de Aprendizaje Automático** se organiza en **3 Unidades** y **2 Trayectos Paralelos**:

```
┌─────────────────────────────────────────────────────────────────┐
│              Unidad 1: Fundamentos (Semanas 1-2)                 │
│   Terminal, Git, Python, Auditoría de Código & Agentes IA        │
└────────────────┬────────────────────────────────────┬────────────┘
                 │                                    │
         ┌───────▼──────────────┐        ┌───────────▼──────────┐
         │  Trayecto I:         │        │  Trayecto II:        │
         │  Inferencia          │        │  Inteligencia        │
         │  Estadística         │        │  Neuro-Simbólica     │
         │  (Semanas 2-7)       │        │  (Semanas 8-12)      │
         │  25 horas            │        │  20 horas            │
         │  Nivel: Intermedio   │        │  Nivel: Avanzado     │
         └──────────────────────┘        └──────────────────────┘
```

---

## Unidad 1: Fundamentos (Obligatorio para ambos Trayectos)

**Duración:** ~12 horas  
**Nivel:** Inicial  
**Prerrequisitos:** Ninguno

### Contenido
- Terminal, Git, Python y entornos virtuales
- Auditoría de código (inspección crítica de IA)
- Configuración de agentes IA (OpenCode, Antigravity CLI, Claude Code)
- Protocolo HTTP/JSON y servidor FastAPI inicial
- Introducción a la mentalidad de Machine Learning

### Hito de Salida
Capacidad de clonar el repositorio `energy-ml`, navegar en terminal, inspeccionar diffs y ejecutar pytest.

---

## Trayecto I: Inferencia Estadística, Modelado y MLOps

**Duración:** 25 horas de cursada (~4-5 semanas)  
**Nivel:** Intermedio  
**Prerrequisito:** Unidad 1

### Objetivo
Dominar el ciclo completo de **Machine Learning estadístico**: preparación de datos, entrenamiento de modelos clásicos (Bayes, k-NN), evaluación rigurosa y construcción de APIs confiables.

### Temas Clave
1. **NumPy & Vectorización** (Semana 1)
   - Tensores, broadcasting, operaciones matriciales
   - Serialización de modelos (joblib)

2. **Validación de Datos** (Semana 2)
   - Pydantic: esquemas, restricciones, validaciones
   - FastAPI: lifespan, gestión de modelos cargados

3. **Data Leakage & Particionamiento** (Semana 3)
   - Partición cronológica (respeto a la flecha del tiempo)
   - Pipelines seguros con sklearn
   - Prevención de fugas en preprocesamiento

4. **Algoritmos Estadísticos** (Semana 4-5)
   - Naive Bayes: clasificación probabilística
   - k-NN: distancias, normalización, costos de inferencia
   - Construcción de endpoints REST

5. **Evaluación Rigurosa** (Semana 6-7)
   - Matriz de confusión (TP, FP, FN, TN)
   - Precisión, Recall, F1-Score
   - TDD con pytest
   - Observabilidad: exposición de métricas en tiempo real

### Criterios de Acreditación
- ✅ Completar 100% de 13 lecciones
- ✅ Responder ≥ 80% de preguntas de razonamiento conceptual
- ✅ Identificar bugs de IA en ≥ 80% de ejemplos de código alucinado
- ✅ Implementar ≥ 2 endpoints con ciclo TDD
- ✅ Exponer ≥ 4 métricas de rendimiento (TP, FP, FN, TN)
- ✅ Tests integrados con ≥ 85% de cobertura

### Certificado de Trayecto I
**Título:** Especialista en Machine Learning y MLOps (Nivel Intermedio)  
**Requiere:** ≥ 80% en evaluación formativa y caza de alucinaciones  
**Válido para:** Especialización en Data Science o ingeniería de modelos

---

## Trayecto II: Inteligencia Neuro-Simbólica y Orquestación con Agentes

**Duración:** 20 horas de cursada (~3-4 semanas)  
**Nivel:** Avanzado  
**Prerrequisito:** Trayecto I (completar primero Unidad 1 + Trayecto I)

### Objetivo
Integrar **razonamiento simbólico** (reglas lógicas, conceptos) con **modelos estadísticos**, y diseñar **servidores autónomos** (MCP) para que agentes IA invoquen herramientas de forma segura y auditable.

### Temas Clave
1. **Aprendizaje de Conceptos Interactivo** (Semana 8-9)
   - Algoritmo Candidate-Elimination
   - Refinamiento iterativo de hipótesis
   - Endpoint POST /version-space/step

2. **Inducción de Reglas Lógicas** (Semana 9-10)
   - Algoritmo AQ (cobertura secuencial)
   - Programación Lógica Inductiva (FOIL)
   - Extracción de reglas interpretables
   - Endpoint GET /rules con auditoría

3. **Árboles de Decisión Explicables** (Semana 10-11)
   - Entropía, Ganancia de Información, Impureza Gini
   - Poda y prevención de overfitting
   - Exportación JSON para auditoría
   - Endpoint GET /trees/{tree_id}

4. **Servidores Model Context Protocol (MCP)** (Semana 11-12)
   - AST (Árboles de Sintaxis Abstracta) y poda de contexto
   - Validación de esquemas de argumentos
   - Handshake MCP, listTools, callTool
   - Integración con agentes IA (OpenCode, Antigravity CLI, Claude Code)

5. **Orquestación de Agentes** (Semana 12)
   - Pipeline integrador con ≥ 3 endpoints
   - Ciclo reflexivo: predicción → auditoría → refinamiento
   - Manejo de decisiones fallidas y reconocimiento de límites del modelo

### Criterios de Acreditación
- ✅ Completar 100% de 10 lecciones
- ✅ Responder ≥ 80% de preguntas de razonamiento conceptual
- ✅ Identificar bugs de IA en ≥ 80% de ejemplos de código alucinado
- ✅ Extraer ≥ 1 conjunto de reglas (AQ o FOIL) con cobertura ≥ 70%
- ✅ Exportar árbol de decisión en JSON con ≥ 10 nodos
- ✅ Implementar servidor MCP con ≥ 2 herramientas
- ✅ Orquestar pipeline con agente invocando ≥ 3 endpoints
- ✅ Tests integrados con ≥ 85% de cobertura

### Certificado de Trayecto II
**Título:** Especialista en Inteligencia Neuro-Simbólica y Orquestación de Agentes  
**Requiere:** ≥ 80% en evaluación formativa y caza de alucinaciones  
**Válido para:** Liderazgo de proyectos de IA interpretable

---

## Flujos de Cursada Permitidos

### 1. Secuencial Completo (Recomendado)
```
Unidad 1 (2 semanas)
  ↓
Trayecto I (5 semanas)
  ↓
Trayecto II (4 semanas)
────────────────────────
Total: 8-10 semanas (60 horas)
```

**Beneficio:** Acumula conocimiento progresivamente. Ideal para estudiantes que desean especialización integral.

### 2. Trayectos Independientes (Parciales)
```
Unidad 1 (2 semanas) + Trayecto I (5 semanas) = 7 semanas
    O
Unidad 1 (2 semanas) + Trayecto II (4 semanas) = 6 semanas*

* Nota: Trayecto II requiere Trayecto I como prerrequisito
```

**Beneficio:** Certificación parcial. Ideal para profesionales con tiempo limitado.

---

## Certificaciones y Títulos

### Nivel 1: Certificado de Trayecto I
- **Requisitos:**
  - Completar 100% de Unidad 1 + Trayecto I
  - ≥ 80% en evaluación formativa
  - ≥ 80% en caza de alucinaciones
  - Tests de integración con ≥ 85% cobertura

- **Título:** Especialista en Machine Learning y MLOps (Nivel Intermedio)
- **Habilidades Certificadas:**
  - Validación de datos con Pydantic
  - Construcción de modelos (Bayes, k-NN)
  - Prevención de data leakage temporal
  - TDD en Machine Learning
  - Evaluación rigurosa de modelos

### Nivel 2: Certificado de Trayecto II
- **Requisitos:**
  - Completar 100% de Unidad 1 + Trayecto I + Trayecto II
  - ≥ 80% en evaluación formativa
  - ≥ 80% en caza de alucinaciones
  - Implementación de servidor MCP funcional
  - Tests de integración con ≥ 85% cobertura

- **Título:** Especialista en Inteligencia Neuro-Simbólica y Orquestación de Agentes
- **Habilidades Certificadas:**
  - Aprendizaje de conceptos interactivo
  - Inducción de reglas lógicas interpretables
  - Explicabilidad de árboles de decisión
  - Diseño de servidores MCP
  - Orquestación de agentes autónomos

### Nivel 3: Certificado Integral (Especialista)
- **Requisitos:**
  - Completar 100% de Unidad 1 + Trayecto I + Trayecto II
  - ≥ 85% en TODAS las evaluaciones formativas
  - ≥ 85% en caza de alucinaciones (todas las 21 lecciones)
  - Implementación completa de pipeline integrador
  - Suite de tests con ≥ 90% de cobertura

- **Título:** Especialista en Procesamiento de Aprendizaje Automático y Agentes IA
- **Reconocimiento:** Egresado del ISFT N° 199 con especialización en IA aplicada
- **Oportunidades de Empleo:** Posiciones en ML Engineering, Data Science, AI Systems Design

---

## Regímenes de Cursada

### Régimen Continuo (Recomendado)
- 1 semana = 1 capítulo (~5 horas)
- Clases semanales en modalidad vespertina (18:00-22:30)
- Evaluación semanal + formativa continua
- Duración total: 8-10 semanas

### Régimen Intensivo (Opcional, si disponibilidad de recursos)
- 3-4 capítulos por semana
- Duración total: 3-4 semanas
- Requiere disponibilidad de tutores y recursos de laboratorio

### Régimen Autodirigido (A ritmo propio)
- Los estudiantes avanzan según su disponibilidad
- Soporte asincrónico vía foros y documentación
- Evaluación al final de cada trayecto

---

## Recurso Caso de Estudio: energy-ml

Todos los laboratorios e implementaciones se realizan sobre el **caso de estudio real** `energy-ml`:
- **GitHub:** https://github.com/datamaq-automation/energy-ml
- **Propósito:** Identificación No Intrusiva de Cargas (NILM) — detección de electrodomésticos a partir de telemetría de energía
- **Endpoints Implementados en Trayectos:**
  - `POST /classify/bayes` (Trayecto I)
  - `POST /classify/knn` (Trayecto I)
  - `GET /metrics` (Trayecto I)
  - `POST /version-space/step` (Trayecto II)
  - `GET /rules` (Trayecto II)
  - `GET /trees/{tree_id}` (Trayecto II)
  - Servidor MCP (Trayecto II)

---

## Evaluación y Autoevaluación

Cada lección incluye **2 componentes de auditoría**:

1. **Autoevaluación Formativa**
   - 2 preguntas de razonamiento conceptual
   - Énfasis en "por qué" (no solo "qué")
   - Respuestas esperadas redactadas en la lección

2. **Caza de Código Alucinado**
   - Ejemplo real de código generado por IA con error
   - Diagnóstico del revisor humano (¿por qué está mal?)
   - Corrección recomendada en energy-ml
   - Entrena el ojo crítico antes de aceptar sugerencias de IA

---

## Notas Importantes

### Separación Pedagógica vs. Técnica
- Los trayectos están **separados pedagógicamente** (cronograma, prerrequisitos, certificaciones)
- En el repositorio, **coexisten en el mismo codebase** (energy-ml) — no hay bifurcación técnica
- Los endpoints se agregan progresivamente y acumulativamente

### Integración con Agentes IA
- Las lecciones **enseñan a desconfiar** de IA: "¿Qué estaría mal en este código generado por IA?"
- Se espera que estudiantes usen OpenCode/Antigravity CLI **bajo auditoría crítica**
- La "Caza de Código Alucinado" prepara para revisar propuestas de agentes en producción

### Requisitos de Ingreso
- Título secundario completo
- Aptitud para lógica matemática y programación
- Disponibilidad de 25-60 horas en ~8-10 semanas
- Acceso a terminal (Linux, WSL, macOS o Git Bash en Windows)

---

## Referencias Relacionadas
- [`curso.yaml`](curso.yaml): Estructura de capítulos, lecciones y duraciones
- [`trayectos.yaml`](trayectos.yaml): Definición formal de prerrequisitos, hitos, acreditación
- [AGENTS.md](/AGENTS.md): Principios de Clean Architecture y validaciones

---

**Última actualización:** 2026-10-04  
**Versión:** 2.0 (con separación formal de Trayectos I y II)
