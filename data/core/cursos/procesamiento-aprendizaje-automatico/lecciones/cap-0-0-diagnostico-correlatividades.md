# Lección Diagnóstica: ¿Estás listo para PAA? Autoevaluación de conocimientos previos recomendados

**Asignatura:** Unidad 0 — Diagnóstico Inicial  
**Carga horaria:** 30 min (autopauseada)  
**Prerrequisitos:** Ninguno. Toma esta prueba ANTES de iniciar Cap 0.  
**Objetivo:** Verificar el dominio de los conocimientos previos recomendados para el espacio (álgebra lineal y matrices de Elementos de Análisis Matemático, probabilidad condicional de Estadística y Probabilidades para la Gestión de Datos, y programación estructurada en Python de Técnicas de Programación).

> **Aclaración sobre el marco normativo (Resolución DGCyE N° 2730/22, Anexo I):**  
> El espacio curricular 12 (*Procesamiento de Aprendizaje Automático*, 2.º año, 2.º cuatrimestre, Trayecto F) **no figura en la tabla de correlatividades formales obligatorias** de la sección 8 del Anexo I. Sin embargo, pedagógicamente se asume el dominio de los saberes desarrollados en los espacios curriculares de 1.er año para poder modelar, entrenar y evaluar sistemas predictivos y estadísticos.

---

## ¿Por Qué Este Diagnóstico?

Aunque normativamente no existe correlatividad formal previa, el diseño curricular prescribe que este módulo profundiza en modelos predictivos, agrupamiento y análisis estadístico avanzado. Para aprovechar el curso plenamente, se recomienda contar con los conocimientos previos de:
- **Elementos de Análisis Matemático (Espacio 3):** matrices, determinantes, vectores, sistemas de ecuaciones
- **Estadística y Probabilidades para la Gestión de Datos (Espacio 4):** distribuciones, media, varianza, regla de Bayes
- **Técnicas de Programación (Espacio 7):** funciones, listas, Python básico, pruebas unitarias

Si detectás dificultades en estas áreas, esta lección te orientará con rutas de nivelación y repaso antes de abordar los laboratorios prácticos.

---

## Autoevaluación Interactiva

Contesta las preguntas abajo. No hay calificación: es solo para vos. Si respondes mal, revisaremos juntos.

### **Bloque 1: Álgebra Lineal Básica**

**Pregunta 1.1:** ¿Qué es una matriz? (Selecciona la opción correcta)
- A) Un arreglo de números organizados en filas y columnas
- B) Un programa que corre en la computadora
- C) El inicio de una película
- D) Una fórmula química

**Respuesta correcta:** A  
**Por qué:** Una matriz es una estructura rectangular de números. En Machine Learning, representamos datos como matrices (muestras × características).

---

**Pregunta 1.2:** Dado el vector **v = [3, 4]**, ¿cuál es su magnitud (norma euclidiana)?

Hint: magnitud = √(3² + 4²)

- A) 7
- B) 5
- C) 12
- D) √7

**Respuesta correcta:** B  
**Por qué:** √(9 + 16) = √25 = 5. Esta operación es **crítica en k-NN** (cálculo de distancias).

---

**Pregunta 1.3:** ¿Qué es el broadcast (difusión) en NumPy?
- A) Una película de Netflix
- B) Realizar operaciones entre arreglos de formas diferentes sin duplicar memoria
- C) Enviar un email
- D) Un algoritmo de clasificación

**Respuesta correcta:** B  
**Por qué:** Broadcasting permite restar un vector de 3 elementos a cada fila de una matriz 4×3 sin bucles `for`. Veremos esto en la lección de NumPy.

---

### **Bloque 2: Probabilidad y Estadística**

**Pregunta 2.1:** En un dataset de telemetría, los valores de temperatura tienen media = 65°C y desviación estándar σ = 5°C. ¿Qué significa σ?
- A) La temperatura máxima posible
- B) Una medida de cuánto varían los datos respecto a la media
- C) La temperatura más común
- D) El número de sensores

**Respuesta correcta:** B  
**Por qué:** La desviación estándar cuantifica la dispersión. En Naive Bayes, usamos μ y σ para modelar distribuciones gausianas.

---

**Pregunta 2.2:** ¿Cuál es la probabilidad de que llueva mañana, DADO que hoy está nublado? ¿Cuál de estas frases describe esta probabilidad?
- A) Probabilidad incondicional
- B) Probabilidad condicional
- C) Probabilidad a priori
- D) Probabilidad marginal

**Respuesta correcta:** B  
**Por qué:** La "probabilidad DADO" es **condicional**. Esta es la base del **Teorema de Bayes** que estudiaremos en Unidad 2.

---

**Pregunta 2.3:** En una muestra de 100 eventos de falla eléctrica:
- 5 son fallos dieléctricos
- 95 son condiciones normales

¿Cuál es P(Falla)?
- A) 5%
- B) 95%
- C) 1/100
- D) A y C son equivalentes (ambas correctas)

**Respuesta correcta:** D  
**Por qué:** P(Falla) = 5/100 = 0.05 = 5%. Usaremos estas probabilidades como priors en Naive Bayes.

---

### **Bloque 3: Programación Python Básica**

**Pregunta 3.1:** ¿Qué diferencia hay entre una lista y una función en Python?
- A) Una lista guarda múltiples valores; una función realiza una tarea
- B) Las funciones son más rápidas
- C) Las listas se usan solo en Ciencia de Datos
- D) No hay diferencia

**Respuesta correcta:** A  
**Por qué:** Las listas (`[1, 2, 3]`) almacenan datos. Las funciones (`def mi_funcion()`) encapsulan lógica reutilizable. En PAA usarás ambas.

---

**Pregunta 3.2:** ¿Qué es una prueba unitaria (unit test)?
- A) Una prueba de amor
- B) Una línea de código que verifica si una función produce el resultado esperado
- C) Un examen de la universidad
- D) Una métrica de ML

**Respuesta correcta:** B  
**Por qué:** Las pruebas unitarias aseguran que tu código es correcto. En PAA Unidad 1 Cap 5, haremos TDD (Test-Driven Development) con pytest.

---

**Pregunta 3.3:** ¿Cuál es la diferencia entre `for` loop y comprensión de lista en Python?
```python
# Opción A: Loop tradicional
resultado = []
for x in [1, 2, 3]:
    resultado.append(x ** 2)

# Opción B: Comprensión de lista
resultado = [x ** 2 for x in [1, 2, 3]]
```
- A) La opción A es más rápida
- B) La opción B es más Pythonica y legible
- C) Son equivalentes, pero B es preferido en código profesional
- D) B y C son correctas

**Respuesta correcta:** D  
**Por qué:** Ambas dan el mismo resultado `[1, 4, 9]`, pero B es más concisa. En PAA preferiremos **NumPy arrays** sobre comprensiones por eficiencia.

---

## Rutas de Recuperación

**Si contestaste MAL en Bloque 1 (Álgebra):**
- 📚 Repasa: [Khan Academy — Introducción a Matrices](https://www.khanacademy.org/) (30 min)
- 💡 Recurso: "Elementos de Análisis Matemático" (espacio curricular de 1.er año)
- ⏭️ **Después de repasar**, vuelve a intentar las preguntas

**Si contestaste MAL en Bloque 2 (Probabilidad):**
- 📚 Repasa: "Estadística y Probabilidades para Gestión de Datos" (espacio curricular de 1.er año)
- 💡 Clave: Recuerda que P(A|B) = "probabilidad de A **dado** B"
- ⏭️ Unidad 2 Cap 3 (Bayes) depende críticamente de esto

**Si contestaste MAL en Bloque 3 (Python):**
- 📚 Repasa: "Técnicas de Programación" (espacio curricular de 1.er año) — especialmente funciones y listas
- 💡 Practica: Escribe 3-5 funciones simples en un archivo `.py` y ejecuta con `python mi_archivo.py`
- ⏭️ Sin Python fluido, no podrás seguir laboratorios en PAA

---

## Próximos Pasos

**Si dominaste TODOS los bloques:**
- ✅ Eres candidato/a ideal para PAA
- 🚀 Continúa directamente a Unidad 1 Cap 0

**Si necesitas recuperación parcial:**
- ⏸️ Dedica **2-3 horas** a repasar los bloques fallidos
- 📝 Siéntete libre de consultarle a tu instructor(a)
- 🔄 Retoma PAA cuando te sientas seguro/a

**Si necesitas recuperación extensa (fallaste 2+ bloques):**
- ☕ Conversá con tu instructor(a) sobre un plan de nivelación
- 📞 Hay tutorías disponibles (preguntar en secretaría)
- 🎯 Recuperación activa es mejor que avanzar en el vacío

---

## Notas Finales

- Este diagnóstico **NO es calificable**. No afecta tu promedio.
- Es una herramienta para vos, para identificar brechas.
- La autonomía está en tus manos: ¿necesitas repasar o seguir adelante?

**¡Buena suerte y adelante! 🚀**
