### 2.1 Principios y componentes del transformador de potencia

El transformador de potencia es la máquina eléctrica estática fundamental que permite acoplar las redes de distribución de media tensión (13,2 kV) con los consumos industriales de baja tensión (380 V / 220 V) mediante inducción electromagnética.

#### Principio de Funcionamiento
Basado en la Ley de Faraday. Un flujo magnético variable en el tiempo es establecido en un núcleo ferromagnético por una corriente alterna fluyendo en el devanado primario. Este flujo induce una fuerza electromotriz (FEM) proporcional al número de espiras en el devanado secundario.

#### Componentes Principales

1. **Núcleo**:
   - Fabricado de chapas de acero al silicio laminadas en frío y orientadas magnéticamente para minimizar las corrientes de Foucault e histéresis.
2. **Devanados (Bobinados)**:
   - Conductores de cobre o aluminio aislados. Dispuestos concéntricamente alrededor de las columnas del núcleo (primario y secundario).
3. **Cuba o Tanque**:
   - Recipiente de acero que contiene los bobinados, el núcleo y el aceite dieléctrico.
4. **Aceite Dieléctrico / Refrigerante**:
   - Cumple dos funciones vitales: aislar eléctricamente las partes con tensión y transportar el calor generado en los devanados hacia las paredes de la cuba o radiadores. Puede ser mineral o sintético (esteres ecológicos).
5. **Bornes de Conexión (Bushings)**:
   - Aisladores pasatapas que permiten atravesar las paredes metálicas de la cuba sin peligro de arco a masa.
6. **Tanque de Expansión / Conservador**:
   - Cámara ubicada sobre la cuba que absorbe las variaciones de volumen del aceite ante cambios de temperatura del transformador, limitando su contacto con el oxígeno del aire.

#### Grupo de Conexión y Comportamiento Vectorial (Dyn11)
El acoplamiento magnético y eléctrico de las bobinas del transformador define su grupo de conexión. El estándar absoluto en distribución industrial para transformadores MT/BT es el grupo **Dyn11**:
- **D (Triángulo en MT)**: Las tres bobinas del lado primario (13.2 kV) están conectadas en triángulo. Esto evita que el tercer armónico de corriente de secuencia cero (generado por el núcleo o por cargas no lineales aguas abajo) circule por la red de media tensión primaria, confinándolo magnéticamente dentro del lazo cerrado del triángulo.
- **y (Estrella en BT)**: Las tres bobinas del lado secundario (380 V) están conectadas en estrella, compartiendo un punto común.
- **n (Neutro accesible)**: El punto común de la estrella se conecta físicamente a la barra de neutro y a tierra. Esto permite disponer de un conductor de neutro para alimentar cargas monofásicas (220 V) y da el punto de referencia para los esquemas de tierra de la planta.
- **11 (Desfasaje vectorial de 30°)**: Indica que la tensión de fase del secundario se encuentra adelantada 30° respecto a la tensión de fase equivalente del primario. Esta configuración ofrece un comportamiento robusto ante desequilibrios provocados por cargas monofásicas en la instalación de BT.

