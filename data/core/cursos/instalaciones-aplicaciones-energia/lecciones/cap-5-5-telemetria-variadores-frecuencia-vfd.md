# 5.5 Telemetría y Monitoreo IoT en Variadores de Frecuencia (VFD)

Los variadores de frecuencia (VFD / VVF) son dispositivos clave para la regulación de velocidad en motores asincrónicos trifásicos, constituyendo uno de los puntos de mayor impacto en la eficiencia energética industrial.

## 1. Importancia Energética y Leyes de Afinidad

En aplicaciones cinemáticas con cargas de par variable (como bombas centrífugas y ventiladores), la potencia absorbida por el motor varía con el cubo de la velocidad de rotación ($P \propto N^3$).

$$\frac{P_1}{P_2} = \left(\frac{N_1}{N_2}\right)^3$$

Reducir la velocidad del motor en un 20% permite obtener un ahorro energético teórico de hasta un **48.8%**, lo que convierte a los VFDs en activos críticos para el control de demanda energética.

## 2. Parámetros Clave para Captura e Integración IoT

A través de la interfaz de comunicación industrial (habitualmente RS-485 Modbus RTU o Modbus TCP), es posible extraer registros en tiempo real sin requerir sensores analógicos adicionales:

- **Frecuencia de salida (Hz):** Velocidad real suministrada al motor.
- **Corriente de salida (A):** Consumo de amperaje instantáneo en las fases.
- **Tensión de bus de CC (Vdc):** Monitoreo de estabilidad de red y filtrado de armónicos.
- **Potencia Activa (kW) y Consumo Acumulado (kWh):** Medición de energía dedicada al proceso.
- **Temperatura del Inverter (ºC):** Control de disipador de calor y módulo IGBT.
- **Código de Falla y Registro de Disparos:** Diagnóstico preventivo por sobrecorriente, sobretensión o falta de fase.

## 3. Arquitectura de Conexión en Planta

```
┌─────────────────────────┐       RS-485 Modbus       ┌────────────────────────┐
│ Variador de Frecuencia  │ ────────────────────────> │ Gateway IoT Industrial │
│       (VFD / VVF)       │    (Registros 40001+)    │   (Python / MQTT / REST│
└─────────────────────────┘                           └───────────┬────────────┘
                                                                  │
                                                                  ▼
                                                      ┌────────────────────────┐
                                                      │ Servidor / Dashboard SGE│
                                                      └────────────────────────┘
```

El monitoreo continuo de estos registros permite pasar de un esquema de mantenimiento reactivo a un modelo de **mantenimiento predictivo**, optimizando tanto el consumo de energía como la disponibilidad operativa de las líneas de producción.
