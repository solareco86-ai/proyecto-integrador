### 5.4 Sistemas Eléctricos Auxiliares y de Seguridad

Los sistemas auxiliares de una subestación o planta industrial son aquellas instalaciones que garantizan la operación segura de los equipos de potencia principales y la salvaguarda de vidas ante emergencias. Las exigencias para sistemas de seguridad eléctrica se estructuran bajo **AEA 90364-5-56** (Servicios de seguridad) e **IEC 60364-5-55 / 5-56**.

#### 1. Sistemas Auxiliares de Corriente Continua (CC)
Es el sistema más crítico para la protección de la subestación, alimentando de forma ininterrumpida los circuitos de control, alarmas y disparos de los interruptores de MT:
- **Cargador de Baterías**: Rectifica la CA y mantiene el banco en flotación.
- **Banco de Baterías**: Almacena energía química (típicamente Plomo-Ácido regulado por válvula - VRLA o Níquel-Cadmio). Operan en 110 Vcc o 125 Vcc.
- **Tablero de Distribución de CC**: Distribuye la tensión de corriente continua de forma segregada y supervisada (detectores de falla a tierra en barras de CC).

#### 2. Alimentación de Servicios de Seguridad (Generadores y UPS)
Según **IEC 60364-5-55 / 5-56**, las fuentes de seguridad para alimentación de emergencia se clasifican por su tiempo de conmutación y deben garantizar autonomía suficiente ante cortes:
- **Sistemas de Alimentación Ininterrumpida (UPS)**: Clasificados como fuentes de corte nulo (0 ms). Basados en rectificador, banco de baterías y un inversor de estática que alimenta cargas críticas de control y sistemas informáticos industriales. Ante fallas internas del inversor, conmutan a un bypass estático rápido sin interrupción.
- **Grupos Electrógenos de Emergencia**: Clasificados como fuentes de corte medio (conmutación en < 15 segundos). Equipados con un Tablero de Transferencia Automática (TTA) que supervisa la tensión de red externa, arranca el motor diésel y realiza la conmutación de cargas prioritarias (bombas de incendio, iluminación de escape, sistemas de extracción de gases).

#### 3. Canalizaciones Seguras para Emergencias
Para asegurar que los servicios de seguridad sigan operativos en presencia de fuego directo (según **AEA 90364-5-56**):
- **Cables Resistentes al Fuego (LSZH - Low Smoke Zero Halogen)**: Deben certificar resistencia al fuego directo durante períodos prolongados (norma **IEC 60331**, típicamente 90 o 120 minutos manteniendo continuidad eléctrica) y estar compuestos por materiales libres de halógenos para evitar la emisión de humos oscuros y gases ácidos altamente corrosivos y tóxicos.
- **Segregación Física**: Los tendidos de cables de servicios de seguridad deben ir por bandejas o ductos exclusivos, físicamente separados de los cables de fuerza motriz convencionales, o protegidos por barreras cortafuego homologadas.
