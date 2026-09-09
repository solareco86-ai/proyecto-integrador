### 3.3 Diseño de Puesta a Tierra y Seguridad en Subestaciones

El sistema de puesta a tierra (PAT) es el pilar fundamental de la seguridad en subestaciones y redes eléctricas, garantizando la correcta actuación de las protecciones y limitando los gradientes de potencial superficial a valores seguros para las personas y equipos.

#### 1. Diseño y Cálculo de Mallas de Puesta a Tierra (IEEE 80)
El diseño de la malla de puesta a tierra en Media Tensión (habitualmente en 13.2 kV) y subestaciones se rige por la norma **IEEE 80** y las directrices locales de la **AEA 95403** (Estaciones Transformadoras):
- **Estructura de la Malla**: Consiste en una retícula horizontal de conductores de cobre desnudo (típicamente de sección ≥ 50 mm²) enterrados a una profundidad de entre 0.5 m y 1 m, complementada por jabalinas (electrodos verticales) en los puntos periféricos y de conexión de descargadores.
- **Objetivo del Diseño**: Mantener la resistencia total de puesta a tierra de la subestación lo más baja posible (usualmente R<sub>g</sub> < 1 Ω o < 5 Ω según exigencia de la distribuidora) y asegurar que las tensiones superficiales no excedan los límites tolerables para el cuerpo humano.

#### 2. Conceptos Críticos de Seguridad
Durante una falla a tierra, circula una corriente de cortocircuito a través de la malla, elevando el potencial del suelo circundante (EPR - Earth Potential Rise). Se deben controlar dos variables críticas:
- **Tensión de Contacto (V<sub>touch</sub>)**: Diferencia de potencial máxima entre una estructura metálica conectada a tierra y un punto de la superficie del suelo situado a una distancia al alcance de la mano de una persona (estimado en 1 metro).
- **Tensión de Paso (V<sub>step</sub>)**: Diferencia de potencial máxima en la superficie del suelo entre dos puntos separados por una distancia de un paso (estimado en 1 metro), sin hacer contacto con ninguna estructura.
- **Equipotencialidad**: Se logra interconectando todas las partes metálicas no activas (chasis de transformador, celdas, puertas metálicas, cercos perimetrales) a la malla general mediante soldaduras exotérmicas o terminales de compresión aprobados, minimizando riesgos por choque eléctrico de acuerdo a **AEA 90364-4-41**.
- **Capa de Rodadura de Alta Resistividad (Grava)**: La norma **IEEE 80** prescribe la colocación de una capa de piedra partida o grava de alta resistividad eléctrica (típicamente de 8 a 15 cm de espesor y con resistividad ρ<sub>s</sub> ≥ 3000 Ω·m) sobre el terreno de la subestación. Esta capa actúa como un aislante en serie con los pies del operador, reduciendo drásticamente la corriente de paso del cuerpo humano y permitiendo que los límites tolerables de V<sub>touch</sub> y V<sub>step</sub> de diseño sean sustancialmente más elevados.


#### 3. Mediciones y Ensayos de Campo
- **Medición de Resistividad del Terreno (Método de Wenner)**: Se realiza antes del diseño de la malla. Se colocan 4 picas equidistantes y alineadas en el suelo a una distancia a. Se inyecta corriente entre las picas externas y se mide el potencial entre las internas. La resistividad aparente se calcula como:
  **ρ = 2 · π · a · R**
- **Medición de Resistencia de PAT (Método de la Caída de Potencial)**: Utilizando un telurímetro de 3 polos. Se inyecta una corriente conocida entre el electrodo bajo prueba (E) y una pica de corriente auxiliar (C). Una pica de potencial (P) se desplaza alineadamente a distancias intermedias (típicamente al 61.8% de la distancia E-C) para trazar la curva de potencial y determinar el valor óhmico en la meseta estabilizada.
