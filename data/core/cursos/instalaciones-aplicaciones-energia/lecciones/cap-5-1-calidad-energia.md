### 5.1 Calidad de Energía y Compensación de Reactiva

En las industrias modernas, las cargas no lineales introducen perturbaciones en la red eléctrica. Entender el comportamiento del factor de potencia y la distorsión armónica es crucial para optimizar el consumo de energía y evitar penalidades de la distribuidora.

#### 1. Compensación de Potencia Reactiva y Armónicos
La compensación de potencia reactiva inductiva mediante bancos de capacitores reduce la corriente total circulante, liberando capacidad en los transformadores y reduciendo caídas de tensión y pérdidas por efecto Joule:
- **Cálculo de la Reactiva Requerida**: La potencia de paso para corregir el factor de potencia desde un cos φ₁ inicial a un cos φ₂ objetivo se calcula mediante:
  
  Q<sub>c</sub> = P · (tan φ₁ - tan φ₂)

- **Bancos Automáticos**: Utilizan un regulador automático de reactiva (FP) que mide el desfase entre tensión y corriente de la planta y comanda la conexión o desconexión de pasos de capacitores.
- **Corriente de Inrush y Contactores Específicos (Categoría AC-6b)**: Al conmutar pasos de capacitores, se genera un transitorio de corriente de alta frecuencia (inrush) que puede llegar a ser de **60 a 100 veces la corriente nominal** del capacitor por fracción de milisegundo. Este transitorio fatiga el dieléctrico del capacitor y suelda los contactos de contactores convencionales. Para mitigarlo, se exige el uso de **contactores específicos para capacitores (AC-6b)** dotados de contactos auxiliares de preinserción en serie con resistencias limitadoras de alambre que se cierran momentáneamente antes de los contactos principales para disipar el transitorio.
- **Reactancias de Desintonización (Filtros Antirresonantes)**: En instalaciones con alta distorsión armónica, la conexión directa de capacitores puede crear un circuito resonante en paralelo con la inductancia del transformador a una frecuencia armónica específica, provocando sobrecorrientes destructivas. Se conectan inductancias en serie con los capacitores, sintonizando la rama a una frecuencia por debajo del primer armónico relevante (típicamente a 189 Hz para redes de 50 Hz con predominio de 5º armónico, factor de desintonización p = 7%).


#### 2. Distorsión Armónica Total (THD) e Impacto Industrial
Las cargas electrónicas no lineales (variadores de velocidad, rectificadores, arrancadores suaves, luminarias LED) consumen corrientes no senoidales, inyectando corrientes armónicas a la red:
- **Distorsión Armónica Total**: Se cuantifica mediante el **THD-I** (en corriente) y el **THD-V** (en tensión), expresando el contenido armónico acumulado como porcentaje de la componente fundamental (50 Hz).
- **Efectos sobre Transformadores y Conductores**:
  - **Calentamiento Adicional**: Las corrientes de alta frecuencia aumentan las pérdidas por corrientes de Foucault en el transformador. Se requiere aplicar un **Factor K** de reducción de potencia (derating) al transformador si alimenta cargas muy no lineales.
  - **Sobrecarga de Conductores y Efecto Pelicular (Skin Effect)**: A frecuencias superiores a 50 Hz, la corriente circula preferentemente por la periferia del conductor, aumentando su resistencia efectiva.
  - **Corriente de Neutro por Armónicos Triples**: Los armónicos impares múltiplos de tres (3º, 9º, 15º) se suman aritméticamente en el conductor neutro en sistemas trifásicos equilibrados, pudiendo sobrecargar el neutro hasta un 170% de la corriente de fase, requiriendo el dimensionamiento de conductores de neutro sobredimensionados según **AEA 90364-5-52**.
