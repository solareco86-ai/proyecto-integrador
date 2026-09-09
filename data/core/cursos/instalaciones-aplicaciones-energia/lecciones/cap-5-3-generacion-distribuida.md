### 5.3 Transición Energética y Generación Distribuida

Las redes industriales están evolucionando de un modelo de consumo unidireccional pasivo a microredes activas que integran generación propia a partir de fuentes renovables y almacenamiento inteligente de energía.

#### 1. Sistemas Fotovoltaicos On-Grid Industriales
La energía solar fotovoltaica conectada a la red (On-Grid) representa la principal tecnología de generación distribuida en plantas industriales debido a su rápida amortización y bajo mantenimiento:
- **Principio de Operación**: Los módulos fotovoltaicos convierten la radiación solar en corriente continua (CC). Los **inversores solares** (de cadena o string) transforman esta energía en corriente alterna (CA) y la inyectan en fase directamente en el tablero general de la planta, operando en paralelo con la red eléctrica pública.
- **Esquema de Inyección Cero (Zero Export)**: Cuando las regulaciones locales no permiten inyectar excedentes a la red externa o no hay medidor bidireccional, se instala un controlador de inyección cero asociado a un medidor en la cabecera. Este sistema reduce dinámicamente la potencia de los inversores para que la generación coincida exactamente con el autoconsumo instantáneo de la fábrica.
- **Medición Bidireccional (Net Metering)**: En regiones con leyes de generación distribuida activas, el excedente no consumido se inyecta a la red pública, siendo registrado por un medidor bidireccional para obtener un crédito en la facturación eléctrica.

#### 2. Sistemas de Almacenamiento con Baterías (BESS)
Los sistemas BESS (Battery Energy Storage Systems) de gran escala, basados en acumuladores de Litio-Ferrofosfato (**LiFePO4**) por su seguridad y alta ciclicidad, resuelven la intermitencia solar y optimizan los costos de facturación mediante varias estrategias:
- **Peak Shaving (Reducción de Picos)**: El sistema inyecta energía acumulada durante las horas donde la planta experimenta sus picos de consumo máximo. Esto reduce la potencia máxima contratada registrada por la distribuidora, disminuyendo fuertemente el cargo fijo por capacidad o potencia máxima facturada.
- **Load Shifting (Desplazamiento de Carga)**: Consiste en cargar las baterías desde la red en horarios nocturnos (tarifa valle o barata) y descargarlas en horarios pico (tarifa cara), aprovechando el arbitraje tarifario en tarifas con discriminación horaria.
- **Respaldo y Soporte de Frecuencia**: Actúan como sistemas UPS de gran escala para procesos críticos de planta, entregando potencia en milisegundos ante microcortes o caídas del suministro principal mientras arrancan los generadores diésel auxiliares.
