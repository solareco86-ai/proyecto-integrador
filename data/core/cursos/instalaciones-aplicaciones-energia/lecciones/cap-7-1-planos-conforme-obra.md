### 7.1 Planos e Ingeniería Conforme a Obra

La documentación conforme a obra (As-Built) constituye el registro final de ingeniería de una instalación eléctrica, detallando exactamente cómo fue construida físicamente e interconectada en la realidad. Además de ser el manual operativo para mantenimiento, es un requisito legal normado por **AEA 90364-6** e **IEC 60364-6** para la habilitación de la obra.

#### 1. Planos Eléctricos y Documentación Técnica Obligatoria
De acuerdo a **AEA 90364-3** y **Parte 6**, toda obra eléctrica habilitada debe contar con la siguiente carpeta de ingeniería básica:
- **Esquema Unifilar**: Representación simplificada del sistema eléctrico completo mediante una sola línea. Muestra la jerarquía de distribución, acometidas, potencias de transformadores, tipos de interruptores, calibres de cables y protecciones.
- **Croquis de Distribución de Tableros**: Detalle físico interno de los gabinetes, garantizando el cumplimiento de distancias mínimas y compartimentación de seguridad.
- **Memoria de Cálculo**: Justificación técnica de las secciones de cables seleccionadas (caída de tensión, capacidad térmica de cortocircuito) y el cálculo de la corriente de cortocircuito en cada nodo.
- **Plano de Puesta a Tierra (PAT)**: Plano de planta detallando el tendido de la malla, ubicación de los puntos de inspección (cámaras de registro) e interconexiones de equipotencialidad.

#### 2. Protocolo de Ensayos Obligatorios (AEA 90364-6 / IEC 60364-6)
Antes de la puesta en servicio inicial de una instalación eléctrica de BT, se debe ejecutar y certificar una serie de pruebas y verificaciones visuales e instrumentales obligatorias:
- **Continuidad de Conductores de Protección**: Verificación de que todos los conductores de protección (PE) y conexiones equipotenciales principales y suplementarias tienen una resistencia eléctrica menor a 0.2 Ω.
- **Resistencia de Aislamiento**: Medición con Megger entre conductores activos y entre conductores activos y tierra. Para tensiones de servicio de 380/220 V, la norma exige inyectar 500 Vcc, debiendo obtenerse una resistencia mínima de aislamiento de **1.0 MΩ**.
- **Resistencia de Puesta a Tierra**: Medición de los electrodos de PAT con telurímetro mediante el método de caída de potencial. El valor obtenido debe cumplir con los límites seguros según el esquema de conexión a tierra adoptado (ej. en esquema TT, R<sub>pat</sub> < 40 Ω o 10 Ω dependiendo de la distribuidora, garantizando que el producto R<sub>pat</sub> × I<sub>Δn</sub> ≤ 24 V o 50 V).
- **Ensayo de Disparo de Interruptores Diferenciales (RCDs)**: Prueba instrumental para verificar que los diferenciales desconectan dentro de los tiempos máximos permitidos por norma (ej. con una corriente de fuga diferencial nominal I<sub>Δn</sub> = 30 mA, el interruptor debe disparar en menos de 40 ms a una corriente de prueba de 5 × I<sub>Δn</sub> para protección de contactos directos).

