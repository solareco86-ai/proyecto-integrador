# 8.2 Q&A y Demo en Vivo: Manejo de Preguntas y Troubleshooting

## Objetivo

Responder preguntas sin pánico. Demostrar que conoces el proyecto (código + decisiones). Mantener control si algo falla en la demo.

## Referencia

**Plan Oficial § Referenciales:** Q&A y demo frente a partes interesadas

## Contenidos

### 1. Tipos de Preguntas (y Cómo Responder)

**Tipo 1: Técnica específica**
```
P: "¿Por qué Pyright en lugar de mypy?"
R: "Buena pregunta.
   [pausa 2 seg, demuestra que pensaste]
   Pyright es más estricto (strict mode nativo).
   Mypy es bueno, pero Pyright integra mejor con IDE.
   Para nuestro caso, Pyright fue la mejor opción."
```

**Tipo 2: Decisión de arquitectura**
```
P: "¿Por qué Clean Architecture en lugar de arquitectura hexagonal?"
R: "Excelente pregunta.
   [pausa]
   Ambas son similares. Clean Architecture es más conocida
   en la industria (Uncle Bob, el creador, escribió el libro).
   Para alcance de 64 horas, parecía la opción más pragmática."
```

**Tipo 3: Sobre limitaciones**
```
P: "¿El sistema aguanta 1 millón de eventos por segundo?"
R: "No, actualmente preparamos 100k eventos/seg.
   Para 1M, necesitaríamos Redis + async tasks.
   [ser honesto sobre límite]
   Pero para el caso de uso actual (institución con 50 medidores),
   100k es más que suficiente."
```

**Tipo 4: Fuera del alcance**
```
P: "¿Cómo integran con Salesforce?"
R: "Excelente idea. No lo cubrimos en este proyecto.
   [no inventas respuesta]
   Pero sería un add-on futuro. Abrimos issue en GitHub
   si quieren.
   [ofrece siguiente paso, no cierra puertas]"
```

**Tipo 5: El curveball**
```
P: "¿Qué pasa si MQTT broker se cae?"
R: "Buena pregunta.
   [tómate 3 segundos, está bien pensar]
   El sistema loguea el error y usa último valor válido
   como fallback. Así no falla cascada. En test_fault_tolerance
   lo verificamos."
```

### 2. Técnicas para No Parecer Perdido

**Cuando NO sabes la respuesta:**

```
❌ MALO:
- "Eh... no sé"
- Cambiar de tema abruptamente
- Inventar respuesta (te cazan después)

✅ BUENO:
P: "¿Cuál es el overhead de tipado estricto?"
R: "Buena pregunta. Típicamente Pyright adds
   [pausa mientras pienso]
   quizá 500ms de compilación. Pero lo probamos y
   en nuestro repo es < 100ms, así que minimal."
   [si no sé exacto, es OK: "sería 500-1000ms probablemente"]
```

**Compra tiempo:**
- "Buena pregunta..." (3 seg pausa)
- "Déjame poner eso en contexto..." (organizas pensamiento)
- "Eso es parte de... [recienta sección anterior]" (vuelves a seguro)

### 3. Demo en Vivo: El Acto Más Riesgoso

**Riesgos:**
- Internet cae
- Aplicación crashea
- Video no carga
- Sensores no conectan

**Preparación:**

```
Antes de defensa:
☐ Chequear conexión internet (¿WiFi o cable?)
☐ Tener backup: video pre-grabado de demo
☐ Tener backup: screenshot de dashboard
☐ Probar proyector con tu laptop (resolución, HDMI, audio)

Datos de demo:
☐ Dataset de prueba en BD (no depender de sensores reales)
☐ Script: "simulate_mqtt_data.py" que publica eventos
☐ Todo automático, no "esperar a que algo llegue"
```

**Estructura de Demo (5 min):**

```
0-1 min: Setup
- "Voy a simular datos de sensores"
- Ejecuta: python simulate_mqtt_data.py
- [datos empiezan a llegar]

1-3 min: Dashboard
- Abre dashboard
- Muestras consumo actualizado
- Dices: "Esto es en vivo. Cada 1 minuto actualiza"
- Presionas botón: "generar anomalía"
- [consume sube, alerta aparece]

3-4 min: Código rápido
- Abre editor
- Muestra 1 función: ReadingService.is_anomaly()
- Dice: "Esta lógica detecta si anomalía"
- NO lees código, solo señalas

4-5 min: Cierre
- "Preguntas sobre la demo?"
```

### 4. Si Algo Falla (Murphy's Law)

**Internet cae:**
```
"Parece que tuvimos desconexión. Tengo video de backup.
[ya tiene pre-grabado]
Veamos cómo se ve en tiempo real con datos simulados."
[plays video]
```

**Aplicación crashea:**
```
"Se nos cayó. [sin pánico]
Eso pasa, tenemos logs. [abre logs]
Aquí vemos: conexión rechazada a BD.
En producción, auto-reintenta. La lección: error handling.
[pivot a lección, no a culpa]"
```

**Proyector no funciona:**
```
"Creen que podemos arreglar el HDMI?
[mientras, pasamos laptops a audiencia para que vean de cerca]
O sigo sin proyector. [confianza]"
[demo sigue aunque más lenta]
```

### 5. Control de Ritmo

**Si alguien monopoliza con preguntas:**
```
P1: [pregunta larga]
P2: [pregunta sobre lo mismo]
P3: [pregunta sobre lo mismo]

TÚ: "Veo el patrón. Eso es importante.
     [reconoces, demuestras que escuchas]
     ¿Podemos abordar esto en la etapa final?
     Ahora quería mostrar X, luego hay espacio para esto."
     [guías el flujo sin ser rudo]
```

**Si hay tension:**
```
P: "Eso no tiene sentido. ¿Por qué hicieron eso?"
   [tone: un poco atacante]

TÚ: "Buena pregunta. Entiendo la preocupación.
     [validas el emotion, no la crítica]
     Cuando empezamos, no sabíamos X.
     Después de investigación, elegimos Y.
     ¿Qué parte específica no cierra?"
     [invitas a clarificar, mantienes respeto]
```

### 6. Errores Comunes (No Hagas)

```
❌ "Ese no es un buen pregunta" (condescending)
✅ "Buena pregunta, pero salimos del scope" (respetus)

❌ "Lo hicimos así porque... no sé, parecía bien" (weak)
✅ "Lo evaluamos entre X e Y. X ganó porque..." (confident)

❌ Lees directamente de las slides durante Q&A (boring)
✅ Contestas de memoria, slides son apoyo (expert)

❌ "Ahhh, nadie preguntó eso" cuando no sabes (caught)
✅ "Buena pregunta. [pausa] Típicamente..." (thoughtful)

❌ Defensiva ("El código está bien, punto") (blocks discussion)
✅ Abierta ("Vimos ese problema, aquí está cómo lo resolvimos") (collaborative)
```

### 7. Signal que Eres Experto

```
1. Cita tus propias métricas:
   "Cobertura fue 87%, específicamente..."
   (numbers demuestran preparación)

2. Anticipa follow-ups:
   "Podrían preguntar, ¿por qué 85% min?
   Porque industria estándar es 80%, nosotros quisimos estar arriba"
   (demuestras que pensaste en objeciones)

3. Conecta con experiencias:
   "Cuando en campo visitamos operador, vimos que..."
   (storytelling, no solo tech)

4. Honra las fuentes:
   "Como dice spec en § 5.2..." (demuestras que no inventaste)

5. Ofrece siguiente:
   "Si quieren, repo está abierto. Issue #42 es el próximo step"
   (demuestras que no es "fin del mundo", es "inicio")
```

## Actividad Práctica

1. **Prepara 10 preguntas probables:**
   ```markdown
   # Preguntas Anticipadas
   
   P1: ¿Por qué Pyright?
   R: [respuesta con números]
   
   P2: ¿Qué pasa si MQTT falla?
   R: [explicación + código referencia]
   
   ... (10 total)
   ```

2. **Practica demo 3 veces con fallos simulados:**
   - Demo 1: Internet cae
   - Demo 2: App crashea
   - Demo 3: Normal
   - Mide tiempo (target 5 min)

3. **Graba Q&A mock:**
   - Pide a amigos que hagan preguntas "difíciles"
   - Graba tus respuestas
   - Mira: ¿pausas? ¿claridad?

## Palabras clave

Q&A, Demo, Troubleshooting, Confidence, Control, Honesty, Expertise

## Referencias

- Toastmasters Q&A guidelines
- TED Talk Q&A sessions
- Improvisation principles (say "yes, and...")
