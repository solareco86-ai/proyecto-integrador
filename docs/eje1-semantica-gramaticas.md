# Eje 1.3 — Análisis semántico, léxico institucional y gramáticas formales

## Objetivo

Detectar la **intención principal** de la consulta del usuario y extraer
**entidades clave** (carrera, trámite, atributo) a partir de un **léxico
controlado** del dominio institucional y de **reglas gramaticales formales**
(CFG / DCG).

---

## Léxico controlado (`data/chat/lexico.yaml`)

El léxico define el vocabulario del dominio institucional:

| Categoría | Ejemplos |
|-----------|----------|
| **Carreras** | 6 tecnicaturas con sinónimos (ej. `ia` → Ciencia de Datos e IA) |
| **Trámites** | inscripción, anotarme, requisitos, documentación |
| **Horarios** | horario, turno, vespertino, noche |
| **Ubicación** | dirección, donde, sede, Talar, Tigre |
| **Contacto** | teléfono, mail, whatsapp, secretaría |

Las carreras se toman de `data/content/carreras.yaml` como fuente de verdad,
sin duplicar ni inventar nombres (AGENTS.md §7.5).

---

## Intenciones (`data/chat/intenciones.yaml`)

Se definen **14 intenciones** con sus patrones, respuesta y confianza:

| Intención | Ejemplo de frase | Confianza |
|-----------|-----------------|-----------|
| `consulta_carreras` | "¿Qué carreras tienen?" | 0.9 |
| `info_carrera` | "Info de logística" | 0.85 |
| `inscripcion` | "Quiero inscribirme" | 0.9 |
| `horarios` | "¿A qué hora se cursa?" | 0.9 |
| `ubicacion` | "¿Dónde queda?" | 0.95 |
| `contacto` | "¿Cuál es el mail?" | 0.9 |
| `modalidad` | "¿Es presencial?" | 0.9 |
| `duracion` | "¿Cuánto dura?" | 0.9 |
| `gratuidad` | "¿Cuánto cuesta?" | 0.95 |
| `saludo` | "Hola, buen día" | 1.0 |
| `correlatividades` | "¿Cuáles son las correlativas?" | 0.8 → Secretaría |
| `mesas_de_examen` | "¿Cuándo son los finales?" | 0.8 → Secretaría |
| `becas` | "¿Hay becas?" | 0.8 → Secretaría |

Las últimas 3 intenciones **derivan a Secretaría** (`isft199@abc.gob.ar`)
porque no hay datos disponibles en `data/` (cumplimiento de AGENTS.md §7.5).

---

## Gramática independiente del contexto (CFG)

La gramática formal que modela la estructura de las consultas:

```
S              → VERBO_CONSULTA ENTIDAD
S              → VERBO_CONSULTA ENTIDAD COMPLEMENTO
S              → SALUDO
ENTIDAD        → CARRERA | TRAMITE | ATRIBUTO
ATRIBUTO       → "horario" | "ubicacion" | "contacto" | "modalidad" | "duracion"
COMPLEMENTO    → PREP CARRERA | PREP ATRIBUTO | ε
VERBO_CONSULTA → "quiero" | "necesito" | "busco" | "que" | "como" | "donde"
PREP           → "de" | "en" | "sobre" | "para"
SALUDO         → "hola" | "buen dia" | "buenas tardes"
```

### Frases aceptadas por la gramática

| Frase | Derivación |
|-------|-----------|
| `quiero inscribirme` | S → VERBO(`quiero`) ENTIDAD/TRAMITE(`inscribirme`) |
| `quiero inscribirme en logística` | S → VERBO ENTIDAD COMPLEMENTO(PREP CARRERA) |
| `info de turismo` | S → VERBO(`info`) COMPLEMENTO(`de` CARRERA(`turismo`)) |
| `hola` | S → SALUDO |

### Frases rechazadas (→ fallback)

| Frase | Razón |
|-------|-------|
| `¿cómo está el clima?` | Sin ENTIDAD del dominio ni VERBO_CONSULTA relevante |
| `quiero pizza` | ENTIDAD no pertenece al léxico controlado |

---

## Gramática de cláusulas definidas (DCG)

Ejemplo formal en notación DCG (Prolog):

```prolog
% Regla principal: una consulta produce una intención.
consulta(Intent) --> verbo_consulta, entidad(E), { Intent = info(E) }.
consulta(Intent) --> verbo_consulta, entidad(E), complemento(C),
                     { Intent = info(E, C) }.

% Entidades del dominio
entidad(carrera(X))  --> [X], { es_carrera(X) }.
entidad(tramite(X))  --> [X], { es_tramite(X) }.

% Verbos de consulta
verbo_consulta --> [quiero].
verbo_consulta --> [necesito].
verbo_consulta --> [info].

% Complementos
complemento(carrera(X)) --> preposicion, [X], { es_carrera(X) }.
preposicion --> [de].
preposicion --> [en].

% Léxico (hechos)
es_carrera(logistica).
es_carrera(turismo).
es_carrera(hoteleria).
es_tramite(inscribirme).
es_tramite(anotarme).
```

### Ejemplo de derivación DCG

```
?- consulta(Intent, [info, de, turismo], []).
   Intent = info(carrera(turismo)).
```

---

## Arquitectura

```
data/chat/lexico.yaml          ← Léxico controlado
data/chat/intenciones.yaml      ← Intenciones + patrones + respuestas
        │
        ▼
IntentClassificationService     ← src/application/services/
  ├─ _detect_career()           ← Búsqueda en índice invertido del léxico
  ├─ _match_patterns()          ← Match de patrones de intenciones.yaml
  ├─ _cfg_analysis()            ← Análisis CFG: VERBO + ENTIDAD
  └─ get_response()             ← Genera respuesta con template
        │
        ▼
ProcessChatTextUseCase          ← src/application/use_cases/chat/
  1. Normalización (Eje 1.2)
  2. Clasificación de intención (Eje 1.3)
  3. Generación de respuesta real
```

---

## Pruebas

Las pruebas en `tests/test_chat_intent.py` cubren:

- **Detección de cada intención** (consulta_carreras, inscripción, horarios, etc.)
- **Extracción de entidades** (carrera por sinónimos del léxico)
- **Consulta fuera de dominio** → fallback
- **Derivación a Secretaría** (becas, mesas, correlatividades)
- **Gramática CFG** (estructura VERBO + ENTIDAD + COMPLEMENTO)
- **Ejemplo DCG** (consulta → info(carrera(turismo)))
