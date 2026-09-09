### 4.2 Coordinación de Protecciones y Selectividad

Un diseño adecuado de protecciones eléctricas garantiza que, ante una falla (sobrecarga o cortocircuito), únicamente se desconecte el dispositivo de protección aguas arriba más cercano al punto de la falla, minimizando la interrupción del servicio en el resto de la instalación.

#### 1. Protecciones de Sobrecorriente en Media Tensión (ANSI)
En las celdas de MT que alimentan transformadores se utilizan relés electrónicos de protección asociados a transformadores de corriente (TC). Las funciones principales son:
- **ANSI 50 (Sobrecorriente instantánea)**: Se activa sin retraso intencional cuando la corriente supera el umbral de cortocircuito franco.
- **ANSI 51 (Sobrecorriente temporizada)**: Funciona bajo curvas de tiempo inverso, donde a mayor corriente de falla menor es el tiempo de disparo. Tipos comunes de curvas (según IEC 60255 o IEEE): Tiempo Inverso (SI), Muy Inverso (VI) y Extremadamente Inverso (EI).
- **ANSI 50N / 51N (Sobrecorriente de tierra)**: Detecta corrientes homopolares residuales provocadas por fallas monofásicas a tierra, requiriendo umbrales de ajuste mucho menores que las de fase.

#### 2. Selectividad en Baja Tensión (BT)
En el Tablero General de Distribución (TGBT) se debe garantizar la selectividad entre los interruptores de cabecera (usualmente interruptores abiertos o de bastidor - **ACB**) y los interruptores de los circuitos de salida (generalmente de caja moldeada - **MCCB**):
- **Selectividad Amperométrica**: Basada en la diferencia entre los umbrales de corriente de disparo instantáneo. Es efectiva para fallas de baja magnitud alejadas del tablero.
- **Selectividad Cronométrica**: Se introduce un retraso temporal intencional (retardo de tiempo corto, t<sub>sd</sub>) en el interruptor de cabecera aguas arriba para permitir que el de salida actúe primero.
- **Selectividad Energética**: Utiliza la capacidad de limitación de corriente del interruptor aguas abajo. Ante cortocircuitos severos, el interruptor rápido limita la energía específica letal de paso (I²t), extinguiendo el arco antes de que el de cabecera empiece a abrirse.

#### 3. Estudios de Arco Eléctrico (Arc Flash) y NFPA 70E
La velocidad y selectividad del despeje de fallas tienen un impacto directo en la seguridad de los operarios:
- **Arc Flash**: Liberación violenta de energía térmica y mecánica provocada por un arco eléctrico en el aire.
- **Cálculo de Energía Incidente**: Se determina en calorías por centímetro cuadrado (cal/cm²) y depende de la corriente de cortocircuito y del tiempo de despeje de la protección.
- **NFPA 70E**: Norma que define las distancias de seguridad contra arco y los niveles de Equipo de Protección Personal (EPP o PPE, Categorías de 1 a 4) requeridos para realizar tareas de mantenimiento en tableros energizados. A menor tiempo de disparo de las protecciones, menor será el riesgo de arco eléctrico, aunque esto a veces entra en compromiso con los tiempos exigidos por la selectividad cronométrica.
