### Los niveles de la automatización

Una planta industrial no se automatiza "toda de una vez" ni en un solo nivel. Se organiza en **capas jerárquicas**, donde cada nivel tiene un alcance, un tipo de equipo y una velocidad de respuesta diferente. La representación clásica de esta jerarquía es la **pirámide CIM** (*Computer Integrated Manufacturing*, manufactura integrada por computadora).

### La pirámide CIM

| Nivel | Nombre | Función | Equipo típico | Horizonte de tiempo |
| :--- | :--- | :--- | :--- | :--- |
| 0 | Campo / Proceso | Captar variables físicas y accionar equipos | Sensores, actuadores, motores | Milisegundos |
| 1 | Control | Controlar máquinas y procesos | PLC, controladores PID, variadores | Milisegundos a segundos |
| 2 | Supervisión | Monitorear y operar la planta | SCADA, HMI, PCs de operación | Segundos a minutos |
| 3 | Gestión de producción (MES) | Planificar y programar la producción | Sistemas MES | Horas a días |
| 4 | Gestión empresarial (ERP) | Administrar la empresa | ERP (ej. Xubio, SAP) | Días a meses |

### Nivel de campo y nivel de control

En el **nivel de campo** conviven los elementos que "tocan" el proceso: un termopar que mide temperatura, un final de carrera que detecta una posición, un contactor que alimenta un motor.

En el **nivel de control** trabajan los equipos que toman decisiones en tiempo real: el **PLC** lee esas señales, ejecuta la lógica programada y ordena las salidas. Este nivel debe responder en milisegundos, por eso es determinístico y cableado a campo.

### Supervisión y gestión

El **SCADA** (Supervisión, Control y Adquisición de Datos) permite ver la planta en pantallas, generar alarmas y registrar históricos. Por encima, el **MES** programa la producción y el **ERP** gestiona compras, ventas y contabilidad. La integración de datos "de la planta a la oficina" es justamente el corazón del negocio DataMaq: telemetría real desde el campo hasta el ERP.

### Por qué importa la pirámide

Entender la pirámide evita confusiones: un PLC no reemplaza a un ERP, y un SCADA no sustituye a un controlador. Cada nivel responde a una pregunta distinta: ¿qué está pasando? (campo), ¿qué hago ahora? (control), ¿cómo está la planta? (supervisión), ¿qué produzco mañana? (gestión).

### Micro-desafío práctico

> Dibujá la pirámide CIM y ubicá en cada nivel un ejemplo real: un sensor de temperatura, un PLC, una pantalla SCADA, un sistema de órdenes de producción y un ERP. Justificá por qué cada uno pertenece a ese nivel.

### Resumen

- La automatización se organiza en capas jerárquicas: la **pirámide CIM**.
- Nivel 0: sensores/actuadores; nivel 1: PLC/control; nivel 2: SCADA; nivel 3: MES; nivel 4: ERP.
- Cuanto más bajo el nivel, más rápida debe ser la respuesta.
- Cada nivel responde a una pregunta de negocio distinta.
