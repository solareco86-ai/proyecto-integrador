# 5A.2 Trabajo en Campo: Contextos Reales, Permisos y Seguros

## Objetivo

Vincular el proyecto con contextos laborales REALES. No es observación pasiva; es inserción auténtica en problemáticas que el proyecto intenta resolver. Gestionar aspectos administrativos (permisos, seguros, confidencialidad).

## Referencia

**Plan Oficial § d:** "Prácticas profesionalizantes en entornos formativos. Taller grupal y el trabajo en campo. Inserción de los estudiantes en el contexto laboral o en aquel que mejor se aproxime a las condiciones reales."

**Plan Oficial § f:** "Vinculación real con el mundo del trabajo para poder reflexionar y construir experiencias significativas."

## Contenidos

### 1. ¿Por Qué Trabajo en Campo?

En semanas 1-8 (Trayecto I), estudiantes definen QUÉS (Canvas, SRS, Arquitectura, Planificación). TODO está en papel o en reuniones con docente.

Trabajo en campo es el momento para **salir del aula** y ver la realidad:
- ¿Operadores realmente necesitan dashboard en tiempo real? (Podrían vivir con reportes semanales)
- ¿Qué problemas NO anticipamos? (Facturas vienen en papel, no digitales)
- ¿Hay más de una forma de resolver el problema? (Hay empresas con soluciones comerciales)
- ¿Qué restricciones legales hay? (Datos de consumo son sensibles)

**Resultado:** SRS y Backlog se actualizan con información real, NO asumida.

### 2. Requisito Oficial: Gestión de Permisos y Seguros

El plan oficial exige explícitamente:
- "Gestión de **permisos** para realizar visitas en contextos de trabajo"
- "Gestión de **seguros** que se requieran"
- "Actividades prácticas en contextos seguros"

Esto NO es burocracia: es **profesionalismo y responsabilidad legal**.

**Permisos:**
- Autorización del rector/director para que estudiantes salgan de institución
- Autorización del lugar a visitar (empresa energética, oficinas ISFT, etc.) para recibir estudiantes
- Acuerdos de confidencialidad (si veremos datos sensibles)
- Autorizaciones de padres (si algún estudiante es menor)

**Seguros:**
- Responsabilidad civil: si estudiante causa daño (ej: derrama líquido en oficina), ¿quién paga?)
- Accidentes: si estudiante se accidenta en visita, ¿tiene cobertura de salud?)
- Generalmente: ISFT ya tiene pólizas institucionales; hay que verificar que cubran "actividades de campo"

**Seguridad:**
- ¿Hay riesgos en el lugar? (ej: subestación eléctrica, máquinas)
- ¿Hay protocolos (casco, gafas, chaleco reflectivo)?
- ¿Hay responsable de seguridad en lugar?

### 3. Caso Energy-ML: Trabajo en Campo

**Objetivo:** Entender cómo operan institución/empresa energética en la práctica.

**Pre-salida (Semana 8-9):**
- Docente contacta a responsable de institución energética o escuela con alto consumo
- Se pide: "¿Podemos visitarlos? Estudiantes harán proyecto sobre monitoreo de consumo"
- Se acuerdan: fecha, horario, grupo de estudiantes, responsable de seguridad en lugar

**Documentos a preparar:**
```markdown
# Formulario de Autorización

Institución visitante: ISFT N° 199
Lugar a visitar: [Institución energética / Escuela XXX]
Fecha: [Semana 9]
Hora: [18:00-19:30]
Participantes: [Nombres estudiantes]
Docente responsable: [Nombre]

Objetivo: Entender cómo se monitorea consumo eléctrico actualmente.
Actividades:
- Observar medidores y sensores
- Entrevistar a operadores
- Registrar datos (anónimos)

Confidencialidad: Estudiantes se comprometen a no publicar datos específicos.
Responsable de seguridad en lugar: [Nombre]
```

**Durante visita (2-3 horas):**
- Observación: ¿Cómo llegan datos de sensores hoy? ¿A qué sistema? ¿Quién lo monitorea?
- Entrevistas: "¿Cuál es tu mayor dolor con consumo? ¿Sorpresas en facturas? ¿Cómo detectan anomalías?"
- Fotos: (solo si permiten) Medidores, equipos, escritorios operadores
- Datos: Consumo promedio, variabilidad, horarios pico (información no confidencial)

**Documentación:**
```markdown
# Acta de Visita - Energy-ML

**Fecha:** [Fecha]
**Lugar:** [Institución]
**Participantes:** [Estudiantes], [Docente], [Responsable lugar]

## Observaciones

### Infraestructura Actual
- Medidores: digitales, marca ABB, se leen manualmente
- Sensores: NO hay (datos vienen de factura mensual)
- Dashboard: NO existe (reportes en Excel, actualizados cada mes)

### Dolores Principales (Problema Real)
1. Sorpresas en facturas: "Nunca sabemos si consumo subió hasta mes siguiente"
2. Sin visibilidad intra-mes: "No podemos detectar si máquina está con fugas"
3. Manual: "Leer 50 medidores por mano lleva 2 horas"

### Oportunidades
1. Sensores IoT podrían dar visibilidad en tiempo real
2. Alertas automáticas si consumo > X
3. Datos históricos → ML para predicción

### Restricciones Descubiertas
1. Datos de consumo son sensibles (contrato con proveedor energético)
2. No podemos instalar sensores sin aprobación del proveedor
3. Docente debe firmar acuerdo de confidencialidad

## Cambios al Proyecto
- SRS: Agregar requisito "Datos no se publican públicamente"
- Backlog: Cambiar prioridad (No es MUST entrenar modelo; es MUST tener dashboard tiempo real)
- Arquitectura: Clarificar: ¿Nosotros instalamos sensores? No, datos vienen de sistema existente.

## Learning Log Individual
[Cada estudiante escribe 1 página: ¿Qué aprendiste? ¿Cómo cambia tu visión del proyecto?]
```

### 4. Caso Portal Institucional: Trabajo en Campo

**Objetivo:** Entender cómo alumnos reales eligen carrera, qué dudas tienen.

**Pre-salida (Semana 8):**
- Docente coordina con secretaría del ISFT
- "¿Podemos entrevistar a 5-10 alumnos sobre cómo eligieron carrera?"
- "¿Podemos observar consultas a secretaría?"

**Durante trabajo en campo (2-3 horas):**

**Entrevistas a alumnos actuales (15 min c/u):**
- "¿Cómo elegiste tu carrera?"
- "¿Qué dudas tenías antes de decidir?"
- "¿Cómo obtuviste información?"
- "¿Qué información te hubiera ayudado?"

**Observación de consultas a secretaría (30 min):**
- Anotar preguntas que recibe secretaría
- ¿Cuánto tiempo se tarda responder?
- ¿Hay preguntas frecuentes?

**Documentación:**
```markdown
# Acta de Visita - Portal Institucional

## Entrevistas a Alumnos

### Alumno 1
**Carrera elegida:** Ciencia de Datos
**¿Cómo elegiste?** "Amigo estudia ahí, le pregunté"
**Dudas:** "¿Qué trabajo hay después?" "¿Es difícil?"
**Información usada:** Conversación informal, nada oficial
**Feedback:** "Hubiera estado bien un video de egresados mostrando qué laboran"

### Alumno 2
**Carrera elegida:** Mecatrónica
**¿Cómo elegiste?** "Consulté portal web, pero no había mucha info"
**Dudas:** "¿Requisitos exactos?" "¿Cómo es el primer cuatrimestre?"
**Información usada:** Portal web (escaso), consulta a secretaría (lenta, 20 min esperando)
**Feedback:** "Portal podría ser más amigable. Secretaría está saturada."

## Observación Secretaría

**Preguntas frecuentes en 1 hora:**
- "¿Cómo ingreso a Ciencia de Datos?" (x3)
- "¿Qué es Mecatrónica?" (x2)
- "¿Hay cursada vespertina?" (x1)

**Tiempo promedio:** 10-15 min por consulta
**Satisfacción:** Secretaría OK pero cansada ("tendría que estar haciendo otra cosa")

## Cambios al Proyecto
- SRS: Agregar requisito "Bot debe responder en < 1 min" (valor: secretaría ahorra 15-20h/mes)
- Backlog: Priorizar "Mostrar egresados y sus trabajos" (fue feedback de 4/5 alumnos)
- Casos de uso: Agregar "Alumno curiosea sin estar seguro" (antes asumíamos alumno decidido)
```

### 5. Reflexión Grupal (Taller)

Después de salida a campo, hay **taller grupal** (Semana 9, 1h):

- Cada estudiante comparte 1 min: una observación que sorprendió
- Docente modera: ¿Qué patrones vemos?
- Decisión: ¿Cambios a SRS? ¿Prioridades nuevas? ¿Rebajas scope?
- Documentar en `FIELDWORK_SYNTHESIS.md`

## Actividad Práctica

1. **Planificar salida a campo (Semana 8-9):**
   ```markdown
   # Plan de Trabajo en Campo

   ## Objetivo General
   [Qué queremos aprender del contexto real]

   ## Lugar a visitar
   [Institución/empresa]

   ## Fecha y Horario
   [Semana 9, XX:XX-XX:XX]

   ## Participantes
   - Estudiantes: [nombres]
   - Docente responsable: [nombre]
   - Contacto en lugar: [nombre, teléfono]

   ## Actividades
   - [ ] Observación: [qué observaremos]
   - [ ] Entrevistas: [a quiénes, cuántas preguntas]
   - [ ] Recolección de datos: [qué datos anonimizados]

   ## Permisos y Seguros
   - [ ] Autorización de rector ISFT
   - [ ] Acuerdo de confidencialidad firmado
   - [ ] Verificación de cobertura de seguros
   - [ ] Protocolo de seguridad (riesgos?, equipos?)

   ## Deliverables
   - [ ] Acta de visita (1-2 págs)
   - [ ] Learning log individual (1 pág c/estudiante)
   - [ ] Síntesis grupal (cambios a SRS/Backlog)
   ```

2. **Ejecutar visita y documentar:**
   - Fotografías (si permiten)
   - Notas de entrevistas
   - Datos anónimos recolectados

3. **Reflexión individual:**
   ```markdown
   # Learning Log - [Nombre Estudiante]

   ## ¿Qué aprendiste?
   [Cosas que no esperabas; sorpresas; confirmaciones]

   ## ¿Cómo cambia tu visión del proyecto?
   [¿Qué cambiaría en SRS? ¿En prioridades?]

   ## ¿Qué fue difícil?
   [Cosas que no salieron como esperabas]

   ## Próximos pasos para el proyecto
   [Recomendaciones basadas en lo aprendido]
   ```

4. **Síntesis grupal:**
   - Taller (1h): presentar hallazgos
   - Actualizar `SRS.md`, `PRODUCT_BACKLOG.md` con cambios descubiertos

## Palabras clave

Trabajo en campo, Contexto real, Stakeholders, Permisos, Confidencialidad, Seguros, Entrevistas, Learning log, Síntesis

## Referencias

- Plan Oficial § d § f
- Lave & Wenger, "Situated Learning"
- Cooper & Reimann, "About Face" (ch. Interviews)
