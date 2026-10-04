# 7.3 Storytelling y Slides: Presentación Oral de 20-30 min

## Objetivo

Aprender a **contar la historia** del proyecto en 20-30 minutos. NO es "mostrar toda la técnica"; es "conmover y convencer" a la audiencia.

## Referencia

**Plan Oficial § Referenciales:** Presentación y defensa del proyecto

## Contenidos

### 1. Estructura de Storytelling

**Regla: 5 actos**

```
Acto 1 (2 min): Hook - Captar atención
  ↓
Acto 2 (3 min): Contexto - Qué es el problema
  ↓
Acto 3 (8 min): Solución - Qué hicimos
  ↓
Acto 4 (5 min): Impacto - Qué conseguimos
  ↓
Acto 5 (2 min): Cierre - Reflexión + Call to Action
```

### 2. Acto 1: Hook (2 min)

**Objetivo:** Hacer que el público QUIERA escuchar.

**NO hagas:**
```
"Hola, nos llama Dev Team. Vamos a hablar sobre un proyecto de monitoreo..."
(los pierdes en 10 segundos)
```

**SÍ haz:**
```
"Imagina que administras una institución. Llega la factura de electricidad.
50% más caro que el mes anterior. No sabes por qué.
[pausa]
¿No estaría mejor tener eso en tiempo real?"

[Muestras dashboard en pantalla]

"Eso es lo que construimos en 4 semanas."
```

**Técnicas:**
- Pregunta retórica ("¿Qué harían ustedes?")
- Estadística impactante ("$50k/año en sorpresas de factura")
- Escena corta ("Imagina que...")
- Demostración visual inmediata

### 3. Acto 2: Contexto (3 min)

**Objetivo:** Que entienda el problema real.

```
Problema (1 min):
- Instituto tiene sensores MQTT
- Pero datos NO se ven en tiempo real
- Operador reacciona DESPUÉS de que pasó (demasiado tarde)

Stakeholders (1 min):
- Operador (urgente: visibilidad)
- Rector (económico: optimizar costos)
- Dev Team (técnico: arquitectura limpia)

Alcance (1 min):
- ¿Qué ENTRA? Dashboard tiempo real, alertas, predicción
- ¿Qué NO? Instalación de sensores, integración con facturador
```

**Visual:** Mapa mental o tabla de stakeholders

### 4. Acto 3: Solución (8 min)

**Objetivo:** Cómo lo resolvieron.

```
Metodología (2 min):
- Spec-Driven Development
- 2 sprints de 2 semanas
- 64 horas de trabajo
- Equipo: 3 estudiantes

Arquitectura (2 min):
- 4 capas (Clean Architecture)
[DIAGRAM: Domain → Application → Adapters → Infrastructure]
- Integración OCR+NLP+ML
- Testing: 87% cobertura

Demo (4 min):
- Mostrar dashboard funcionando
- Cambiar consumo simulado, ver alerta
- Mostrar código limpio (1-2 snippets)
- Q&A rápidas
```

**Visual:**
- Diagramas de flujo (no de código)
- Screenshots del dashboard
- Gráficos de cobertura/velocidad

### 5. Acto 4: Impacto (5 min)

**Objetivo:** Qué lograron, qué sigue.

```
Resultados (2 min):
- 6 requisitos funcionales (5 implementados)
- 87% cobertura de tests
- Dashboard live
- UAT aprobado por operador real

Lecciones Aprendidas (2 min):
- Trabajo en campo fue clave (descubrimos suposiciones incorrectas)
- Arquitectura limpia payoff (refactors sin miedo)
- Team climate importa (inclusión, horizontalidad)

Próximos Pasos (1 min):
- Monitor en producción 6 meses
- Agregar análisis de subcircuitos
- Optimizar latencia
```

**Visual:** Timeline o roadmap visual

### 6. Acto 5: Cierre (2 min)

**Objetivo:** Que se lleve un mensaje.

```
Reflexión (1 min):
"Aprendimos que la arquitectura NO es overhead.
Es FOUNDATIONAL. Te permite iterar rápido, 
mantener largo plazo, confiar en código."

Call to Action (1 min):
"El código está en GitHub, abierto a todos.
Si alguien quiere mejorar latencia, está el issue #42.
Gracias."

[Final slide: Contacto, preguntas]
```

### 7. Slides: Principios de Diseño

**Regla de Oro:** 1 idea = 1 slide. Máx 20 slides para 25 min.

**NO HAGAS:**
- Texto chiquito (< 24pt)
- Párrafos largos
- Más de 5 líneas por slide
- Fondo con patrón (distrae)
- Comic Sans, Impact o fuentes raras

**SÍ HAZA:**
- 1 imagen grande + 2-3 líneas de texto
- Sans-serif (Arial, Helvetica, Calibri)
- Contraste alto (fondo claro, texto oscuro o viceversa)
- Números grandes (40pt+)

**Ejemplo slide "Problema":**
```
┌─────────────────────────────────────┐
│  El Problema                        │
│                                     │
│  Factura de electricidad: 50% ↑    │
│                                     │
│  ¿Cuál es la causa?                │
│  → Sin visibilidad en tiempo real   │
│                                     │
│  [Imagen: operador confundido]      │
└─────────────────────────────────────┘
```

**Ejemplo slide "Arquitectura":**
```
┌─────────────────────────────────────┐
│  Arquitectura Limpia (4 Capas)      │
│                                     │
│  ┌──────────────────────────────┐  │
│  │ FastAPI Routes / REST API    │  │
│  ├──────────────────────────────┤  │
│  │ Services / DTOs              │  │
│  ├──────────────────────────────┤  │
│  │ Domain Entities / Logic      │  │
│  ├──────────────────────────────┤  │
│  │ PostgreSQL / MQTT            │  │
│  └──────────────────────────────┘  │
│                                     │
│  ✅ Clean, testeable, escalable    │
└─────────────────────────────────────┘
```

### 8. Entrega: Timing y Nervios

```
Práctica (hacer 3 veces):
- Cronometrar exacto
- Frente a espejo o amigos
- Grabar para ver gestos

Día de presentación:
- Llegar 15 min antes
- Revisar tech (proyector, audio)
- Respira profundo (Wim Hof: 4-7-8)
- Habla LENTO (nervios aceleran)
- Haz eye contact
- Sonríe (ya eres experto, ¡disfruta!)

Si se congela:
- "Un segundo mientras busco el slide"
- Agua, respira
- El público espera pacientemente
```

### 9. Q&A: Manejo de Preguntas

```
Pregunta técnica difícil:
P: "¿Cómo maneja 1M de eventos por segundo?"
R: "Buena pregunta. Actualmente preparamos 
    100k eventos/seg sin problema. Para 1M, 
    necesitaríamos Redis + async tasks. Está 
    en roadmap."

Pregunta que te deja en blanco:
P: "¿Por qué eligieron PostgreSQL?"
R: "Excelente pregunta. Porque...
    [5 segundos de silencio está OK]
    ...necesitábamos transacciones ACID 
    y PostgreSQL es el estándar en Python."

Pregunta sobre algo NO cubierto:
P: "¿Cómo integran con Salesforce?"
R: "No lo abordamos en este proyecto, 
    pero es un caso de uso válido. 
    Te paso el issue en GitHub."
```

## Actividad Práctica

1. **Estructura tu presentación (30 min):**
   - Acto 1: Hook (escribe 2-3 versiones, elige la mejor)
   - Acto 2-5: Outline con tiempos
   - Practica una vez, cronometra

2. **Crea slides en Canva o Google Slides (1h):**
   - 15-20 slides máximo
   - 1 imagen + 2-3 líneas por slide
   - Colores consistentes

3. **Practica 3 veces antes de defensa (1.5h):**
   - Cronometra (objetivo 25 min)
   - Graba y mira
   - Pide feedback a amigos

4. **Documenta en `PRESENTATION_NOTES.md`:**
   - Texto de cada slide (para practicar)
   - Timing por acto
   - 5 preguntas anticipadas + respuestas

## Palabras clave

Storytelling, Presentation, Slides, Public Speaking, Hook, Call to Action, Timing

## Referencias

- TED Talks (referencia: cómo contar historias)
- Presentation Zen (diseño de slides)
- Nancy Duarte, "Resonate" (storytelling en presentaciones)
