# Cap 2.0: Ética, Sesgo y Privacidad en Machine Learning — Responsabilidad del Científico de Datos

**Asignatura:** Unidad 2 — Machine Learning (Nivel Intermedio)  
**Capítulo 2:** Tareas de Aprendizaje y Deducción vs. Inducción  
**Carga horaria:** 35 min (lectura reflexiva + caso práctico)  
**Prerequisitos:** Haber completado Cap 1 (arquitectura de inferencia).

---

## ¿Por Qué Ética en una Clase de ML?

> "Con gran poder viene gran responsabilidad." — Uncle Ben

Machine Learning no es neutral. Los algoritmos que diseñas toman decisiones que afectan a personas reales:
- **Diagnóstico de falla:** Si fallas, cae la energía de un hospital (vidas en riesgo)
- **Identificación de carga:** Si sesgado, ciertas industrias pagan más (inequidad económica)
- **Datos personales:** Si no proteges privacidad, expones información sensible de usuarios

**Esta lección es obligatoria**, no opcional.

---

## 1. Sesgo Algorítmico: El Problema Real

### Caso 1.1: Sesgo de Género en Diagnóstico Médico

Un hospital entrena un modelo para **predecir falla cardíaca** con datos históricos:
- Datos: 80% hombres, 20% mujeres
- Resultado: Modelo predice "riesgo alto" solo en hombres
- Consecuencia: **Mujeres con infarto silencioso no son diagnosticadas** (mueren)

**¿Dónde está el sesgo?**
- No en el algoritmo (Bayes, k-NN, CART son neutros)
- **En los datos:** Dataset desbalanceado heredó sesgo histórico

### Caso 1.2: Sesgo de Raza en Sistemas de Justicia (COMPAS)

El algoritmo COMPAS predicción "riesgo de reincidencia" en presos:
- Entrenado con datos históricos de arresto (que reflejan discriminación policial)
- Resultado: **Sobreestima riesgo en personas negras**, subreestima en blancas
- Consecuencia: Sentencias más largas injustas por predicción sesgada

**¿Dónde está el sesgo?**
- En los datos históricos: reflejan discriminación pasada
- **El modelo perpetúa y amplifica el sesgo**

### Caso 1.3: Sesgo en energy-ml (Nuestro Caso)

Imaginemos: Entrenas un modelo de **"riesgo de falla"** con datos de 10 años:
- Datos: 95% de subestaciones en zona urbana, 5% en rural
- Resultado: Modelo es excelente en urbano, falla en rural
- Consecuencia: **Pueblos rurales reciben mantenimiento peor** (inequidad de servicios)

**¿Cómo evitarlo?**
1. Recolectar datos balanceados (urbano + rural proporcionalmente)
2. Validar modelo en AMBAS subpoblaciones
3. Reportar disparidad: "Accuracy urbano: 95%, Accuracy rural: 60%"

---

## 2. Las Tres Fuentes de Sesgo

```
┌─────────────────────────────────────────────────────────────┐
│                    SESGO EN ML                              │
├─────────────────┬──────────────┬────────────────────────────┤
│ SESGO DE DATOS  │ SESGO DELDEL │ SESGO DE EVALUACIÓN       │
│                 │ ALGORITMO    │                            │
├─────────────────┼──────────────┼────────────────────────────┤
│ • Datos no      │ • Elección   │ • Métrica inadecuada      │
│   representat.  │   de features│ • Test set sesgado        │
│   (desbalanceo) │ • Hipotesis  │ • Confusion entre         │
│ • Faltan casos  │   del modelo │   grupos (ej: recall      │
│   minoritarios  │ • Algoritmo  │   diferente por raza)     │
│ • Etiquetado    │   hereda     │                            │
│   discrimin.    │   sesgos     │                            │
└─────────────────┴──────────────┴────────────────────────────┘
```

---

## 3. Privacidad: Proteger Datos de Personas

### Problema: Data Breach en energy-ml

Tu modelo de "identificación de carga" usa datos de consumo de usuarios:
```python
X = [
    [2300, 0.85, 15.2],  # Usuario A: potencia, FP, corriente
    [250,  0.92, 1.1],   # Usuario B: LED
    [3200, 0.72, 14.5]   # Usuario C: Motor
]
```

**Riesgo:** Si alguien hackea tu modelo/base de datos:
- Puede inferir "Usuario A tiene horno (consumo 2300W)" = privacidad económica comprometida
- "Usuario B usa LED de bajo consumo" = perfil de pobreza = discriminación

### Solución: Diferential Privacy

**Idea:** Entrenar el modelo agregando **ruido intencional** a los datos:
```python
# Sin privacidad: datos reales
X_real = [[2300, 0.85], [3200, 0.72]]

# Con privacidad: ruido gaussiano agregado
epsilon = 0.1  # Parámetro de privacidad (menor = más ruido, más privado)
X_privado = X_real + np.random.normal(0, 1/epsilon, size=X_real.shape)
# X_privado = [[2298.5, 0.87], [3205.2, 0.70]]  (datos ligeramente alterados)
```

**Tradeoff:**
- ✅ Modelo entrenado no revela datos individuales
- ⚠️ Accuracy baja un poco (porque datos son ruidosos)
- ✅ Vale la pena por privacidad

---

## 4. Consentimiento y Transparencia

### Consentimiento Informado

**Regla:** Nunca uses datos personales sin permiso explícito.

En energy-ml:
```
┌───────────────────────────────────────────────────────────┐
│ CONSENTIMIENTO PARA RECOLECCIÓN DE TELEMETRÍA            │
├───────────────────────────────────────────────────────────┤
│                                                            │
│ ¿Autoriza al ISFT N° 199 a recolectar datos de consumo   │
│ eléctrico de su subestación con fines de:                │
│                                                            │
│ ☑ Diagnóstico de fallas (mejora operativa)              │
│ ☑ Identificación de cargas (eficiencia)                 │
│ ☑ Investigación académica en ML                          │
│                                                            │
│ ¿Los datos serán anonimizados?                           │
│ SÍ — se removerán nombres, direcciones exactas.          │
│ Se guardarán como "Subestación #47" no "Empresa X"       │
│                                                            │
│ ¿Cuánto tiempo se guardan?                               │
│ 2 años. Luego se eliminan.                               │
│                                                            │
│ ¿Puede retirar consentimiento?                           │
│ SÍ, en cualquier momento escribiendo a privacy@isft.ar   │
│                                                            │
│ ☑ Acepto                 ☐ Rechazo                       │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

---

## 5. Auditoría Ética: Preguntas Obligatorias

Antes de deployar un modelo en producción, responde:

### 5.1 Sobre Datos
- [ ] ¿De dónde vienen los datos? (¿públicos? ¿consentimiento?)
- [ ] ¿Representan a TODOS los grupos afectados? (urbano+rural, todas industrias)
- [ ] ¿Qué grupos están SUBREPRESENTADOS?
- [ ] ¿Hay datos etiquetados injustamente? (ej: etiqueta "normal" en falla incipiente)

### 5.2 Sobre el Modelo
- [ ] ¿Qué asunciones hace? (ej: Bayes asume independencia)
- [ ] ¿Cuál es el costo del **falso negativo** vs. **falso positivo**?
  - FN (no detecta falla): muerte de equipos, apagón → **ALTO COSTO**
  - FP (falsa alarma): mantenimiento innecesario → **BAJO COSTO**
  - → Optimizar para **máximo recall**, aunque baje precisión
- [ ] ¿Qué pasa si el modelo falla? (¿hay plan de fallback manual?)

### 5.3 Sobre Evaluación
- [ ] ¿Testeé en subpoblaciones diferentes? (urbano, rural, industrias, etc.)
- [ ] ¿Reporté disparidades? (ej: "Accuracy 95% urbano, 60% rural")
- [ ] ¿Hay supervisión humana en decisiones críticas?

### 5.4 Sobre Privacidad
- [ ] ¿Qué información personal se recolecta?
- [ ] ¿Obtuve consentimiento?
- [ ] ¿Los datos están anonimizados?
- [ ] ¿Hay encriptación en tránsito y en reposo?
- [ ] ¿Quién puede acceder? (principio de least privilege)

---

## 6. Caso Práctico: Auditoría en energy-ml

Imaginemos tu modelo de **"diagnóstico de falla dieléctrica"** en training:

```python
# Datos históricos: 1000 muestras
# Distribución:
# - Subestaciones urbanas: 900 (90%)
# - Subestaciones rurales: 100 (10%)

# Fallas ocurridas:
# - Urbanas: 45 fallas (5% de 900)
# - Rurales: 15 fallas (15% de 100) ← Mayor tasa, pero pocos datos

modelo = GaussianNB()
modelo.fit(X_train, y_train)

# Evaluación global: Accuracy = 94% ✅ Parece bien

# PERO: Desglosar por subpoblación
from sklearn.metrics import classification_report

urbano_mask = X_test[:, -1] == "urbana"
rural_mask = X_test[:, -1] == "rural"

print(classification_report(y_test[urbano_mask], 
                           modelo.predict(X_test[urbano_mask])))
# Accuracy urbano: 96% ✅

print(classification_report(y_test[rural_mask], 
                           modelo.predict(X_test[rural_mask])))
# Accuracy rural: 68% ❌ ← ALERTA: sesgo detectado
```

**Acción correctiva:**
1. Recolectar más datos rurales (estratificación)
2. Entrenar modelo separado para rural si es necesario
3. Reportar disparidad: "Modelo actual tiene 28% menos accuracy en rural"
4. Comprometerse a mejorar (Parte de SLA)

---

## 7. Responsabilidad Legal y Ética

### Regulaciones Vigentes

**GDPR (Europa):** Derecho a la explicabilidad
- Si un algoritmo deniega un crédito, debes explicar por qué

**Ley 25.326 (Argentina):** Protección de Datos Personales
- Consentimiento previo obligatorio
- Derecho a acceso, rectificación, eliminación

**Estándares ISO 42001:** Ética en IA (2023)
- Auditorías periódicas obligatorias
- Documentación de sesgos conocidos

### En energy-ml Específicamente

El ISFT N° 199 es institución educativa pública, no empresa privada. Aún así:
- ✅ Datos de subestaciones = datos públicos (infraestructura del estado)
- ✅ Pero privacidad de **operadores/usuarios** es protegida
- ✅ Auditoría ética es **obligatoria antes de publicar modelos**

---

## 8. Autoevaluación: ¿Entiendes la Responsabilidad?

### Pregunta 1: Sesgo de Datos vs. Sesgo de Algoritmo
"Un modelo k-NN entrenado con 95% datos de subestaciones urbanas predice mal en rural. ¿Es culpa de k-NN?"

**Respuesta esperada:**
No. k-NN es neutro. El culpable es el **dataset desbalanceado**. Solución: recolectar datos rurales o re-ponderar.

---

### Pregunta 2: Privacidad vs. Accuracy
"Usar differential privacy reduce accuracy de 96% a 91%. ¿Vale la pena?"

**Respuesta esperada:**
Depende del costo del error. En diagnóstico de falla eléctrica (vidas en riesgo), **SÍ vale la pena**. Perder 5% de accuracy es mejor que exponer datos privados.

---

### Pregunta 3: Plan de Fallback
"Mi modelo de diagnóstico de falla tiene 99% accuracy. ¿Necesito supervisión humana?"

**Respuesta esperada:**
**SÍ, siempre.** Incluso con 99% accuracy:
- El 1% restante puede ser crítico
- Máquinas se equivocan; humanos revisan antes de decidir
- En energía, la prudencia > la automatización

---

## 9. Recursos y Contacto

- 📚 **Libro:** "Fairness and Machine Learning" (Barocas, Hardt, Narayanan)
- 📖 **Artículo:** "The Mythical Man-Month of Fairness" (Selbst & Barocas)
- 🔗 **GitHub:** [Fairness Indicators](https://github.com/tensorflow/fairness-indicators)
- 📧 **Consultas:** agustin-bustos@isftn199.com.ar

---

## 10. Compromiso Ético del Científico de Datos

> "Reconozco que Machine Learning no es neutral.  
> Diseñaré sistemas considerando equidad, privacidad y transparencia.  
> Reportaré sesgos encontrados, no los ocultaré.  
> Priorizaré personas sobre métricas.  
> Esta es mi responsabilidad."

---

## Próxima Lección

Cap 2.1: **Deducción Simbólica del LLM vs. Inducción Estadística**  
(¿Cuándo confiar en IA para decisiones? Respuesta: cuando datos + ética convergen.)
