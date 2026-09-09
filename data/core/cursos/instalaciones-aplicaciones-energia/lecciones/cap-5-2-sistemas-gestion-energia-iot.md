### 5.2 Sistemas de Gestión de Energía (SGE) e IoT

La digitalización de las instalaciones eléctricas permite realizar una gestión energética activa, capturando datos de consumo y variables eléctricas en tiempo real para optimizar procesos y reducir la huella de carbono. Esto representa una sinergia directa con el núcleo operativo de captura de datos de **Datamaq**.

#### 1. Medidores Inteligentes y Analizadores de Redes
Los **analizadores de redes** y **smart meters** instalados en celdas de MT y salidas principales del TGBT son dispositivos electrónicos que miden y registran continuamente:
- Tensiones y corrientes (valores RMS instantáneos, máximos y mínimos).
- Potencias activa, reactiva y aparente (kW, kVAR, kVA) tanto consumidas como generadas.
- Factor de potencia total y distorsión armónica (THD) por fase hasta el armónico 51.
- Registro de transitorios de tensión, huecos de tensión (sags) y sobretensiones temporales (swells).

#### 2. Protocolos de Comunicación Industrial para Energía
Para recolectar estos datos y enviarlos a sistemas centralizados, los medidores utilizan diversos buses y protocolos:
- **Modbus RTU (sobre RS-485)**: El estándar industrial más extendido por su simplicidad. Utiliza un par trenzado blindado en topología bus, operando bajo un esquema Maestro/Esclavo.
- **Modbus TCP (sobre Ethernet/IP)**: Encapsula las tramas Modbus en paquetes TCP/IP, permitiendo velocidades de comunicación superiores (10/100 Mbps) y el aprovechamiento de la infraestructura de red estructurada de la planta.
- **BACnet**: Muy extendido en la automatización de edificios (BMS) para integrar la climatización, iluminación y consumo eléctrico.
- **IEC 61850 (Automatización de Subestaciones)**: Estándar global moderno para subestaciones digitales. A diferencia de Modbus, define un modelado de objetos lógicos estandarizados y permite la comunicación horizontal ultrarrápida entre protecciones (mensajes GOOSE para enclavamientos en menos de 4 ms) y comunicación vertical cliente/servidor.

#### 3. Sistemas SCADA de Energía e ISO 50001
- **SCADA de Energía (EMS / PMS)**: Aplicaciones de software que centralizan la información de los analizadores de redes. Permiten visualizar diagramas unifilares animados con mediciones dinámicas, gestionar alarmas de eventos eléctricos críticos y registrar bases de datos históricas para auditorías.
- **Norma ISO 50001**: Estándar internacional para la gestión de la energía. Exige que las empresas identifiquen sus usos significativos de la energía, definan una **Línea de Base Energética (LBE)** histórica y establezcan **Indicadores de Desempeño Energético (IDEn)** para monitorizar las mejoras de eficiencia logradas con la automatización y gestión.
