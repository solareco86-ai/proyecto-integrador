### 3.2 Celdas de Media Tensión: características y tipos

Las celdas de Media Tensión (MT) son conjuntos modulares de aparamenta de maniobra, control, medición y protección bajo cubierta metálica que integran los circuitos de distribución primaria. Su fabricación y clasificación se rigen internacionalmente por la norma **IEC 62271-200** (Aparamenta bajo envolvente metálica para tensiones alternativas superiores a 1 kV y hasta 52 kV).

#### Funciones de los Módulos de una Celda (IEC 62271-200)

1. **Celda de Entrada/Salida de Línea (Acometida)**:
   - Permite la conexión física de los cables de distribución primaria.
   - Cuenta con seccionadores de tres posiciones (conectado, desconectado, puesto a tierra) y descargadores de sobretensión.
2. **Celda de Protección con Interruptor (Interruptor de Vacío o SF6)**:
   - Capaz de establecer, soportar e interrumpir corrientes en condiciones normales del circuito, así como corrientes de cortocircuito extremas.
   - Gobernado por relés de protección secundarios.
3. **Celda de Medición**:
   - Aloja transformadores de corriente (TI) y de tensión (TV) para alimentar instrumentos de facturación y supervisión.
4. **Celda de Protección con Fusibles**:
   - Utiliza fusibles limitadores de corriente de MT asociados a un seccionador bajo carga, ideal para la protección de transformadores de distribución.

#### Criterios de Clasificación según IEC 62271-200
La norma define parámetros fundamentales para garantizar la seguridad de los operadores y la disponibilidad del servicio:
- **Pérdida de Continuidad de Servicio (LSC - Loss of Service Continuity)**: Define qué partes de la celda deben quedar fuera de servicio al abrir un compartimento de cables o interruptor.
  - **LSC-1**: Apertura de un compartimento requiere desenergizar toda la celda o barra general.
  - **LSC-2A**: Permite abrir un compartimento de equipo (ej. interruptor) manteniendo energizados los cables de acometida y la barra general.
  - **LSC-2B**: Máxima continuidad; permite abrir el compartimento del interruptor manteniendo energizados los cables y la barra (requiere compartimentación independiente de cables, barras e interruptor).
- **Tipo de Tabique de Separación**: **PM** (particiones metálicas puestas a tierra entre compartimentos) o **PI** (particiones de material aislante).
- **Clasificación de Arco Interno (IAC - Internal Arc Classified)**: Certifica que la celda resiste los efectos térmicos y mecánicos de un arco interno durante un tiempo determinado (ej. 1s a 25 kA), protegiendo al personal en el frente, laterales y parte posterior (clasificación AFLR).

#### Enclavamientos de Seguridad (Safety Interlocks)
Los enclavamientos mecánicos y eléctricos son dispositivos obligatorios por la **IEC 62271-200** diseñados para prevenir errores de operación humana catastróficos. Los sistemas de celdas deben incluir por diseño:
- **Interlock de Maniobra de Barra/Línea**: Impide cerrar o abrir un seccionador de aislamiento bajo carga. El interruptor automático de la celda asociado debe estar obligatoriamente abierto para habilitar la maniobra de sus seccionadores.
- **Interlock de Puesta a Tierra**: Evita cerrar el seccionador de puesta a tierra si el seccionador de aislamiento de línea se encuentra en posición de conectado. Inversamente, impide cerrar el seccionador de línea si la puesta a tierra está aplicada.
- **Interlock de Acceso a Compartimentos**: Bloquea la apertura de las puertas de acceso físicas a los cables de potencia o interruptor si el seccionador de puesta a tierra no ha sido previamente cerrado.


