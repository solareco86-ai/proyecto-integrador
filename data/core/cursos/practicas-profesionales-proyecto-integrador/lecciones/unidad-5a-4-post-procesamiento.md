# 5A.4 Post-procesamiento, Visualización y Mantenimiento: Sostenibilidad

## Objetivo

Entender que un **modelo entrenado NO es el fin**. Es el comienzo. El proyecto debe ser **sostenible**: los datos actualizan, el modelo se retrained, la visualización informa, el usuario toma decisiones.

## Referencia

**Plan Oficial § c:** "Post procesamiento de las estructuras descubiertas, de la visualización y de la actualización en línea."

**MLOps:** Machine Learning Operations (modelo no es artefacto estático, es servicio vivo)

## Contenidos

### 1. ¿Qué es Post-procesamiento?

Post-procesamiento = **transformar output crudo del modelo en decisión accionable**.

**Ejemplo 1 (Energy-ML):**
```
Modelo entrenado predice: 52.3 kWh para próxima hora
Post-procesamiento: 
  - Compara vs consumo promedio (45 kWh)
  - Diferencia: +16%
  - Decisión: ¿Anómala? Criterio: si > 20%, sí
  - Output: "Consumo esperado 52 kWh. Alerta: +16% sobre promedio"
```

Sin post-procesamiento: "52.3" (número sin contexto, usuario no sabe qué hacer).
Con post-procesamiento: Alerta clara para operador tomar acción (revisar máquinas, preparar presupuesto).

**Ejemplo 2 (Portal):**
```
Modelo ML retorna: score de similitud [0.8, 0.6, 0.4] para [CienciaDatos, Mecatrónica, Logística]
Post-procesamiento:
  - Convierte scores a "recomendación" (top 3 carreras)
  - Agrega contexto: "Recomendamos Ciencia de Datos porque coincide con tu interés en programación"
  - Agrega links: página carrera, requisitos, docentes
  - Output: Respuesta amigable en chat
```

Sin post-procesamiento: números (usuario confundido).
Con post-procesamiento: respuesta profesional (usuario entiende y actúa).

### 2. Visualización: No es Cosmética

Visualización es **comunicación clara de información**. NO es "hacer gráficos bonitos".

**Principios:**
- **Veracidad:** El gráfico NO distorsiona datos (ej: ejes escalados engañosamente)
- **Claridad:** Usuario entiende de primera sin leyenda de 10 puntos
- **Accesibilidad:** Alto contraste, tamaño de fuente suficiente, alternativa textual

**Ejemplo Energy-ML:**

**MALO (visual bonito pero confuso):**
```
[Gráfico 3D con perspectiva, colores gradiente, sin eje Y claro]
Usuario: "¿Es 50 kWh o 50 MW?"
```

**BUENO (funcional, accesible):**
```
Consumo Real vs Predicción (Última 24h)
┌─────────────────────────────┐
│ 60 kWh │        ╱╲          │
│ 50 kWh │  ╱╲  ╱  ╲  ╱─────  │ Real (azul)
│ 40 kWh │╱    ╲    ╲╱        │ Predicción (naranja)
│ 30 kWh │              ╲ ╱   │
└─────────────────────────────┘
  0h   6h  12h  18h  24h

⚠️ Alerta: Consumo 20% sobre predicción entre 10h-14h
Causa posible: Sistema AC trabajó en picos
```

Ventajas:
- Usuario ve de un vistazo
- Entiende por qué alerta
- Puede actuar (revisar AC)

**Ejemplo Portal:**

**Recomendador Visual:**
```
Afinidad con Carreras Técnicas

                      Alta afinidad
                           ▲
                           │    Ciencia Datos
                           │    ⭐⭐⭐⭐⭐
                           │    (Lógica + Datos)
            Mecatrónica    │
            ⭐⭐⭐⭐         │
            (Electrónica)  │
                           │
                           │
                    Logística
                    ⭐⭐
                    (Gestión)
────────────────────────────────────────►
              Baja              Alta
            afinidad          afinidad

📊 Tu perfil encaja bien con Ciencia de Datos
→ Ver plan de estudios
→ Hablar con egresado
```

### 3. Actualización en Línea: Modelo NO es Estático

Un modelo entrenado con datos de Enero no debe seguir prediciendo en Noviembre (datos cambiaron).

**Necesidad de Retraining:**

**Caso Energy-ML:**
- Enero: Consumo promedio 45 kWh. Modelo entrenado.
- Julio: Verano, consumo sube a 60 kWh. Modelo predice 45 (WRONG).
- Solución: Retrain cada mes con datos nuevos.

**Caso Portal:**
- Agosto: 5 carreras vigentes. Modelo entrenado.
- Enero: Carrera nueva "Astrofísica" se ofrece. Modelo no sabe.
- Solución: Retrain cuando hay cambios de curriculum.

**Estrategia de Retraining:**
```
Energy-ML:
├─ Trigger: Semanal (datos cambian frecuentemente)
├─ Ventana de datos: Últimas 12 semanas (reciente, no antiguo)
├─ Proceso: Automatizado (script ejecuta cada viernes 23:00)
├─ Versioning: Guardar modelo anterior (rollback si nuevo es worse)
└─ Monitoreo: Métrica RMSE semana anterior vs semana actual

Portal:
├─ Trigger: Manual o anual (cambios curriculum son raros)
├─ Ventana de datos: Últimos 2 años (estable)
├─ Proceso: Docente ejecuta manualmente
├─ Versioning: Una versión anterior siempre disponible
└─ Monitoreo: Precision/Recall cada semestre
```

### 4. Versionado y Rollback

Cambiar modelo en producción es arriesgado. ¿Qué pasa si nuevo modelo es peor?

**Estrategia:**
```
Modelos en Producción:

├─ ACTIVE: modelo_v2.pkl
│  └─ Métricas: RMSE=8.2%, Accuracy=92%
│  └─ Fecha entrenamiento: 2026-10-01
│  └─ Serving: 100% de tráfico
│
└─ STANDBY: modelo_v1.pkl (anterior)
   └─ Métricas: RMSE=9.1%, Accuracy=90%
   └─ En caso de problema con v2: "rollback a v1"
   └─ Tiempo de rollback: < 1 min
```

Si modelo_v2 tiene bug o degrada:
1. Dashboard alertar: "v2 RMSE subió a 15%!"
2. Ingeniero ejecuta: `rollback_model(modelo_v2.pkl, modelo_v1.pkl)`
3. En < 1 min, sistema vuelve a v1
4. Usuarios no ven diferencia

**Sin versionado:** "No sé qué está mal. Servicio roto 6 horas hasta fix."

### 5. Monitoreo: ¿Cómo Sé que Modelo Está "Sano"?

Métricas de monitoreo:

**Energy-ML:**
```
Diario:
├─ RMSE (error promedio): ¿< 10%? Sí ✅ / No ⚠️
├─ Coverage (% de predicciones exitosas): ¿> 99%? Sí ✅
├─ Latencia (tiempo predicción): ¿< 500ms? Sí ✅

Semanal:
├─ Drift (¿datos cambiaron estructura?): Gráfico de comparación
├─ Performance en clases extremas (noche vs día)
└─ Errores sistemáticos (predice siempre alto/bajo)

Si alguno falla:
└─ Alert a ingeniero → Investigar → Retrain o fix
```

**Portal:**
```
Mensual:
├─ Precision@1: ¿Primera recomendación es relevante? ¿> 85%?
├─ Diversity: ¿Modelo recomienda variedad de carreras o siempre la misma?
├─ Satisfaction: ¿Usuarios adsecuados eligen carrera recomendada? Survey

Si degrada:
└─ Revisar: ¿Cambios en curriculum? ¿Sesgo en training data? → Retrain
```

### 6. Escalabilidad: ¿Qué Pasa Si Datos Crecen 10x?

Problema típico: "Funciona con 1000 datos. Pero ¿con 100,000?"

**Decisiones tempranas:**
```
Energy-ML:
├─ Base de datos: ¿SQLite local (OK para demo, falla en producción)?
│  └─ Mejor: PostgreSQL en servidor, índices en (timestamp, value)
├─ Modelo: ¿Entrenamiento toma 2h ahora, 20h con 10x datos?
│  └─ Mejor: Incremental learning o batch processing (entrenar de noche)
└─ API: ¿Responde en 100ms? ¿100x datos → 1000ms (timeout)?
   └─ Mejor: Caché predicciones, request batching
```

**Plan de escalabilidad:** Documentar en `SCALABILITY.md`.

### 7. Deuda Técnica y Roadmap Futuro

Después de 2 sprints, habrá:
- Optimizaciones pospuestas ("model inference está lento pero funciona")
- Refactors necesarios ("código de post-procesamiento es enmaraña")
- Features deseadas ("sería bueno tener alertas por Telegram")

**Documentar en `TECHNICAL_DEBT.md`:**
```markdown
# Deuda Técnica - energy-ml

## Urgente (Próximo trimestre)
- [ ] Refactor post-procesamiento (8h, code smell)
- [ ] Optimizar query de datos históricos (4h, está lento)

## Importante (Próximo año)
- [ ] Integración Telegram para alertas
- [ ] Dashboard con histórico de anomalías

## Nice-to-have (Futuro)
- [ ] ML de clustering para detectar nuevos patrones
- [ ] Simulador "¿qué pasa si bajamos temperatura 2°C?"
```

## Actividad Práctica

1. **Diseña ciclo de vida del modelo (Semana 9):**
   ```markdown
   # Ciclo de Vida del Modelo

   ## 1. Entrada de Datos
   - Fuente: [de dónde vienen datos]
   - Frecuencia: [cada 5 min, diario, etc.]
   - Volumen estimado: [X MB/mes]

   ## 2. Entrenamiento
   - Trigger: [cuándo retrainear]
   - Ventana de datos: [últimas X semanas]
   - Tiempo estimado: [X minutos]
   - Proceso: [automatizado/manual]

   ## 3. Post-procesamiento
   - Transformaciones: [lista]
   - Lógica de decisión: [si X entonces Y]
   - Ejemplos: [3-5 casos reales]

   ## 4. Visualización
   - Gráficos: [qué se muestra]
   - Accesibilidad: [contraste, alternativa textual]
   - Sketches: [ASCII art o descripción]

   ## 5. Monitoreo
   - Métricas: [qué monitoreamos]
   - Umbrales: [qué es "bien", qué es "problema"]
   - Frecuencia: [diario/semanal/mensual]
   - Alertas: [quién se notifica si algo falla]

   ## 6. Versionado
   - Modelos guardados: [dónde]
   - Rollback: [cómo revertir]
   - Tiempo de rollback: [< X minutos]

   ## 7. Escalabilidad
   - Bottlenecks: [identificados]
   - Plan: [cómo escalar si datos 10x]
   ```

2. **Documentar post-procesamiento:**
   ```markdown
   # Post-procesamiento: energy-ml

   ## Input (del modelo ML)
   Predicción: `{timestamp, predicted_kw, confidence}`

   ## Transformaciones
   1. Comparar vs promedio histórico
   2. Calcular diferencia porcentual
   3. Evaluar: ¿diferencia > 20%?

   ## Output (para usuario final)
   ```
   {
     "timestamp": "2026-10-04 18:00",
     "predicted_kw": 52,
     "alert": "⚠️ +20% sobre promedio",
     "recommendation": "Revisar sistema AC"
   }
   ```
   ```

3. **Sketches de visualización:**
   - Dibuja cómo se vería dashboard/recomendación en pantalla
   - Describe accesibilidad (contraste, zoom, alternativas)
   - Documenta en `VISUALIZATION_DESIGN.md`

## Palabras clave

Post-procesamiento, Visualización, Retraining, Versionado, Rollback, Monitoreo, Drift, Escalabilidad, Sostenibilidad, MLOps

## Referencias

- MLOps.community: https://mlops.community/
- Google, "Hidden Technical Debt in ML Systems" (NIPS 2015)
- Plan Oficial § c
