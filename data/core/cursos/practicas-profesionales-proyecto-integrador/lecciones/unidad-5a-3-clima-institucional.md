# 5A.3 Clima Institucional: Género, Inclusión, Diversidad y Horizontalidad

## Objetivo

Establecer **principios de clima institucional** que guíen cada interacción del equipo. NO es "lo políticamente correcto"; es que **educación técnica forma profesionales que respetan dignidad humana** y producen mejor software cuando hay confianza, perspectivas diversas y liderazgo distribuido.

## Referencia

**Plan Oficial § f:** "Entorno de aprendizaje... dimensión vinculada al clima institucional... procesos más inclusivos donde se reconozca y respete las diversidades... horizontalidad en las relaciones... vínculos entre géneros libres de violencias y discriminación."

## Contenidos

### 1. ¿Qué es Clima Institucional?

Clima = la atmósfera psicológica del equipo. Impacta:
- **Creatividad:** ¿Alguien propone idea loca sin miedo a burla?
- **Confianza:** ¿Puedo decir "no sé" sin perder credibilidad?
- **Inclusión:** ¿Mi voz importa aunque sea mujer/minoría/neurodiverso?
- **Calidad:** Equipos inclusivos = mejor código (más perspectivas = menos bugs)

**Dato:** McKinsey 2020 mostró que empresas con diversidad de género/raza tienen 25% menos turnover y mejor innovación.

En educación técnica: Un equipo donde todos se sienten valorados produce software mejor.

### 2. Dimensiones del Clima Institucional

#### A. Género y Equidad

**Problema histórico:** Técnica → "cosa de hombres". Resulta: educación técnica pierde 50% del talento; equipos homogéneos tienen sesgos.

**¿Qué hacemos?**
- **Equidad en tiempos de habla:** En reuniones, medir: ¿todos hablan? ¿O 1 persona monopoliza?
- **Equidad en tareas:** NO asignar "documentación" a mujer, "código" a varón
- **Reconocimiento explícito:** "Ana descubrió el bug en la integración OCR. Buena observación."
- **Revisión de lenguaje:** "Ejecutar" no es "atacar". "Proponer mejora" no es "criticar"

**Métrica:** En retros, anotar quién habló cuánto. Si una persona monopoliza, facilitador interviene.

#### B. Inclusión y Accesibilidad

Inclusión NO significa "tolerar diferencias". Significa "diseñar para que todos puedan participar plenamente".

**Ejemplos prácticos:**
- **Neurodivergencia:** Si alguien tiene TDAH, no significa "perezoso". Significa: ¿Agendemos reuniones con 24h anticipación? ¿No hacemos cambios last-minute?
- **Discapacidad visual:** Si alguien es ciego, ¿nuestro código es accesible? (Variables bien nombradas, documentación clara)
- **Responsabilidades de cuidado:** Si alguien cuida a familiar enfermo, ¿flexible con horarios?
- **Lenguaje:** ¿Hablamos en español claro? ¿Explicamos jerga técnica?

**No es "acomodación"**: Es diseñar para humanos reales, no humanos promedio ficticio.

#### C. Diversidad de Perspectivas

Un equipo homogéneo (3 varones, misma edad, misma escuela) tiene "puntos ciegos". Un equipo diverso ve problemas desde ángulos distintos.

**Ejemplos:**
- Mujer propone: "Este formulario es confuso para usuario no-técnico" (varón técnico no lo vio)
- Persona no-ciencia de datos propone: "Modelo es muy lento, usuario se cansa" (científico optimizó accuracy, no UX)
- Persona ajena al proyecto propone: "¿Por qué no usan librería X?" (perspectiva externa)

**Práctica:** En retros, explícitamente pedir perspectivas de quien menos habló.

#### D. Horizontalidad

"Horizontalidad" NO significa "sin estructura" (sería caos). Significa:
- Liderazgo rotativo (no un "jefe" siempre)
- Decisiones compartidas (no top-down)
- Todos pueden proponer (no solo senior)
- Errores se revisan juntos (no culpa individual)

**Ejemplo malo (vertical):**
```
Estudiante 1: "Propongo cambiar arquitectura"
Estudiante 2: "Estudiante 1 no decide, solo docente decide"
Resultado: Apatía, solo uno contribuye
```

**Ejemplo bueno (horizontal):**
```
Estudiante 1: "Propongo cambiar arquitectura porque X"
Estudiante 2: "Interesante, pero ¿qué pasa con Y?"
Estudiante 3: "Yo apoyo, además Z"
Docente: "Sí, data es convincente. Votemos?"
Resultado: Todos se sienten escuchados
```

#### E. Violencia Cero

"Violencia" NO es solo física. Incluye:
- **Verbal:** "Eres un idiota" (en code review)
- **Discriminación:** "¿Mujer programadora? Raro" (comentario pasivo-agresivo)
- **Exclusión:** "El equipo sale a tomar, pero nadie invita a la mujer"
- **Acoso:** Mensajes inapropiados, presión sexual

**Protocolo:** Si alguien se siente acosado/discriminado:
1. Reporta a docente
2. Docente escalada a ISFT
3. Intervención (capacitación, cambio de equipo si es grave)
4. Seguimiento

### 3. Prácticas Concretas para Clima Positivo

#### En Standups
- SM facilita: "¿Cada uno habla máximo 5 min? ¿Todos hablaron?"
- Si alguien no contribuye: SM pregunta directamente "X, ¿hoy trabajaste en algo?"

#### En Code Review
```
MALO: "Este código es un desastre. No sabes programar."
BUENO: "¿Podemos separar esta función en 2? Así es más testeable."
```

Diferencia: Malo = juzga a la persona. Bueno = cuestiona el código.

#### En Pair Programming
- Rol rotativo: no un "driver" (quien escribe) siempre
- Pausas: "¿Cansancio visual? Descansemos 5 min"
- Feedback: "Me gustó cómo hiciste X. ¿Por qué elegiste esa librería?"

#### En Retros
- "De ánimo anónimo" si hay tensiones: formulario anónimo "¿Cómo te sentiste?"
- Celebrar: "¿Qué salió bien?" ANTES de "qué mejorar"
- Acción concreta: no "mejorar comunicación" vago. SÍ "los próximos 3 standups, cada uno tiene 3 min max"

### 4. Evaluación: Rubric de Clima

El equipo NO se evalúa solo en código. También en **cómo trabajaron juntos**.

```markdown
# Rubric: Clima Institucional

## Criterio 1: Equidad de Género
**Excepcional (5):** Todos hablan cantidad similar. Sin sesgos en asignación de tareas.
**Bueno (4):** La mayoría habla. Pocos sesgos.
**Aceptable (3):** Algunas voces dominan. Algunos sesgos.
**Necesita mejora (2):** Una voz monopoliza. Sesgos claros.

## Criterio 2: Inclusión
**Excepcional (5):** Código/comunicación accesible. Horarios flexibles. Nadie se siente excluido.
**Bueno (4):** Mayormente inclusivo.
**Aceptable (3):** Esfuerzos, pero hay gaps.
**Necesita mejora (2):** Barreras claras.

## Criterio 3: Diversidad de Perspectivas
**Excepcional (5):** Perspectivas distintas valoradas. Se buscan outliers activamente.
**Bueno (4):** Perspectivas respetadas. Algunos outliers escuchados.
**Aceptable (3):** Tolerancia, pero no celebración.
**Necesita mejora (2):** Pensamiento único.

## Criterio 4: Horizontalidad
**Excepcional (5):** Liderazgo rotativo. Decisiones compartidas. Todos contribuyen.
**Bueno (4):** Liderazgo mayormente compartido.
**Aceptable (3):** Estructura pero con voz.
**Necesita mejora (2):** Vertical, top-down.

## Criterio 5: Seguridad Psicológica (Violencia Cero)
**Excepcional (5):** Confianza total. Nadie teme hablar. Sin acoso.
**Bueno (4):** Mayormente seguro.
**Aceptable (3):** Algunos miedos.
**Necesita mejora (2):** Tensión, acoso, discriminación.
```

### 5. Código de Conducta del Equipo

Cada equipo escribe su propio "Código de Conducta" (1 pág). Ejemplo:

```markdown
# Código de Conducta: Equipo Energy-ML

## Compromiso
Trabajamos con respeto, inclusión y seguridad psicológica.

## Prácticas
1. **Standups:** Máximo 5 min por persona. Facilitador asegura que todos hablan.
2. **Code Review:** Preguntas sobre código, no juzgar personas. "¿Por qué elegiste X?" no "X es mal"
3. **Decisiones:** Votamos. Si desacuerdo, facilitador (docente) decide, pero escuchó todos.
4. **Errores:** "Aprender, no culpar." Si alguien comete error, analizamos juntos.
5. **Lenguaje:** Español claro, sin jerga. Si alguien no entiende, se explica.
6. **Horarios:** Flexible. Si alguien no puede cierto horario, buscar alternativa.
7. **Acoso:** Cero tolerancia. Cualquiera que sienta acosado reporta a docente.

## Revisión
Revisamos este código en cada retro. ¿Todavía aplica? ¿Necesita cambios?

Signed:
[Estudiante 1]
[Estudiante 2]
[Estudiante 3]
[Docente]
```

## Actividad Práctica

1. **Crear Código de Conducta del Equipo (Semana 9, taller grupal):**
   - Discutir: ¿Cómo queremos trabajar juntos?
   - Escribir compromisos concretos
   - Todos firman
   - Documentar en `TEAM_CODE_OF_CONDUCT.md`

2. **Monitoreo contínuo:**
   - En cada retro, pregunta: "¿Hemos mantenido nuestro código de conducta?"
   - Métrica simple: "¿Todos hablaron en standups esta semana?" (sí/no)

3. **Reflexión individual (parte de Learning Log):**
   ```markdown
   ## Clima Institucional en Mi Equipo
   
   - ¿Sentí que podía hablar sin miedo?
   - ¿Mis perspectivas fueron escuchadas?
   - ¿Hubo momentos donde sentí excluido/a?
   - ¿Qué mejoraría para próximo proyecto?
   ```

## Palabras clave

Género, Inclusión, Diversidad, Horizontalidad, Seguridad psicológica, Código de Conducta, Equidad

## Referencias

- Plan Oficial § f (Entorno de aprendizaje)
- Contributor Covenant: https://www.contributor-covenant.org/
- Amy Edmondson, "Psychological Safety and Learning in Organizations"
- McKinsey, "Diversity Wins: How Inclusion Matters"
