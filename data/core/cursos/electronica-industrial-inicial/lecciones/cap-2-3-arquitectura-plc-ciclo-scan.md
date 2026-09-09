### ¿Qué es un PLC?

El **PLC** (*Programmable Logic Controller*, Controlador Lógico Programable) es una computadora industrial diseñada para controlar máquinas y procesos en tiempo real, en entornos hostiles (polvo, vibración, temperatura, ruido eléctrico). Su diseño prioriza la **robustez** y la **determinación temporal** por sobre la potencia de cómputo general.

### Arquitectura interna

Un PLC se compone de los siguientes bloques:

| Bloque | Función |
| :--- | :--- |
| **CPU** | Ejecuta el programa de usuario y la gestión interna. |
| **Memoria** | Almacena el programa, los datos y la tabla de imagen de E/S. |
| **Módulos de entrada (DI/AI)** | Reciben señales de campo: digitales (24 V) o analógicas (0-10 V, 4-20 mA). |
| **Módulos de salida (DO/AO)** | Accionan contactores, válvulas, lámparas o señales analógicas. |
| **Fuente de alimentación** | Alimenta la lógica interna y, a veces, los sensores. |
| **Puertos de comunicación** | Ethernet, Modbus, Profibus, etc., para SCADA y otros equipos. |

### Tipos de señales

- **Digitales (discretas):** solo dos estados, ON/OFF. Ej.: un final de carrera, un pulsador, un relé.
- **Analógicas (continuas):** un rango de valores. Ej.: temperatura (0-10 V), presión (4-20 mA), velocidad.

### El ciclo de scan

El PLC no ejecuta el programa "de corrido" una sola vez: lo ejecuta **en ciclos** repetidos indefinidamente. Cada ciclo se llama **scan** y tiene cuatro fases:

1. **Lectura de entradas:** copia el estado de todas las entradas físicas a una **imagen de entradas** en memoria.
2. **Ejecución del programa:** procesa la lógica usando la imagen de entradas y actualiza una **imagen de salidas** en memoria (aún sin accionar el hardware).
3. **Diagnóstico y comunicaciones:** atiende puertos de red, alarmas y estado interno.
4. **Escritura de salidas:** transfiere la imagen de salidas a los módulos físicos.

```
┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌─────────────┐
│ Leer       │ →  │ Ejecutar     │ →  │ Diagnóstico  │ →  │ Escribir    │
│ entradas   │    │ programa     │    │ y comunic.   │    │ salidas     │
└─────────────┘    └──────────────┘    └──────────────┘    └─────────────┘
         ↑                                                         │
         └───────────────────── repetir ◄───────────────────────────┘
```

### Tiempo de scan

El **tiempo de scan** es la duración de un ciclo completo. En PLC modernos es del orden de **milisegundos o menos**. Es crítico porque determina el retardo máximo entre que ocurre un evento en campo y que el PLC reacciona. Por eso, las tareas de seguridad o muy rápidas usan interrupciones o módulos especiales.

### Micro-desafío práctico

> Si un PLC tarda 5 ms por scan y una fotocélula detecta una pieza que pasa en 20 ms, ¿cuántos scans pueden ocurrir mientras la pieza está frente al sensor? ¿Por qué importa este cálculo para no "perder" la pieza?

### Resumen

- El PLC es una computadora industrial robusta y de tiempo real.
- Se compone de CPU, memoria, módulos de E/S, fuente y comunicaciones.
- Las señales son **digitales** (ON/OFF) o **analógicas** (rango continuo).
- Ejecuta el programa en un **ciclo de scan**: leer → ejecutar → diagnosticar → escribir.
