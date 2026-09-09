### 4.1 Suministros en Baja Tensión e Instalaciones de BT

El suministro en Baja Tensión (BT) representa la interfaz final de entrega de la energía eléctrica hacia las instalaciones industriales y comerciales. El diseño de estas instalaciones está regulado estrictamente por la reglamentación **AEA 90364** (Asociación Electrotécnica Argentina) y las normas internacionales **IEC 60364**.

#### 1. Esquemas de Conexión a Tierra (ECT)
Establecidos por **AEA 90364-3** e **IEC 60364-1**, definen la conexión del neutro de la fuente y de las masas metálicas de la instalación a tierra:
- **Esquema TT**: Neutro del distribuidor directamente a tierra; masas del usuario a una tierra local independiente. Obliga al uso de interruptores diferenciales (RCD) en el usuario para asegurar la desconexión ante fallas de baja corriente.
- **Esquema TN (TN-S, TN-C)**: Neutro a tierra; masas conectadas al conductor de protección (PE) que se une al neutro. TN-S mantiene el Neutro (N) y el conductor de protección (PE) separados en toda la instalación. TN-C los combina en un único conductor PEN. **Regla Crítica de Seguridad (AEA 90364-3):** Se permite la transición de TN-C a TN-S aguas abajo, pero está terminantemente prohibido volver a unir el PE y el Neutro (pasar de TN-S a TN-C) en ningún punto posterior de la instalación, ya que esto provocaría corrientes de retorno indeseadas por las masas metálicas de la planta, disparos erráticos de RCDs y graves problemas de Compatibilidad Electromagnética (CEM).
- **Esquema IT**: Neutro aislado de tierra (o conectado mediante alta impedancia); masas a tierra local. La primera falla a masa genera una corriente de falla despreciable, permitiendo mantener la continuidad del servicio. Obligatorio en quirófanos e industrias de proceso continuo, requiriendo un Vigilador de Aislamiento (monitor de aislamiento continuo).

#### 2. Dimensionamiento de Conductores (AEA 90364-5-52 / IEC 60364-5-52)
La sección de los conductores eléctricos de BT debe seleccionarse y verificarse cumpliendo tres criterios fundamentales:
- **Capacidad de Corriente (Criterio Térmico)**: La corriente de diseño del circuito (I<sub>b</sub>) no debe superar la corriente admisible del cable (I<sub>z</sub>). Esta última se determina aplicando factores de corrección por temperatura ambiente (F<sub>t</sub>) y por agrupamiento de cables en la misma canalización o bandeja (F<sub>g</sub>) sobre las capacidades tabuladas de la norma.
- **Caída de Tensión**: Se calcula para asegurar que la tensión en bornes de la carga esté dentro de los límites regulados (habitualmente máximo 3% para alumbrado y 5% para fuerza motriz).
- **Corriente de Cortocircuito (Criterio de Corto Circuito)**: Verificación térmica del conductor ante fallas, asegurando que la energía específica letal de paso admisible por el cable sea mayor que la disipada por la protección.

#### 3. Coordinación de Protecciones contra Sobrecargas y Cortocircuitos (AEA 90364-4-43 / IEC 60364-4-43)
Para asegurar que los conductores estén totalmente protegidos, los dispositivos de protección (fusibles o interruptores automáticos) deben cumplir con:
- **Protección contra Sobrecargas**:
  **I<sub>b</sub> ≤ I<sub>n</sub> ≤ I<sub>z</sub>**  y  **I₂ ≤ 1.45 · I<sub>z</sub>**
  Donde I<sub>n</sub> es la corriente nominal de la protección e I₂ es la corriente que asegura el funcionamiento efectivo del dispositivo en el tiempo convencional.
- **Protección contra Cortocircuitos**: Se debe verificar que la protección despeje el cortocircuito antes de que el cable alcance su temperatura límite admisible de cortocircuito (ej. 160 °C para PVC, 250 °C para XLPE). Esto se expresa mediante la fórmula de la energía específica de paso:
  **I² · t ≤ k² · S²**
  Donde I es la corriente de cortocircuito eficaz, t el tiempo de despeje, S la sección del conductor en mm², y k un factor constante del material conductor y aislante (ej. k = 115 para cobre con aislamiento PVC).
- **Cálculo de la Corriente de Cortocircuito Presunta (I<sub>cc</sub>)**: En bornes del secundario del transformador (cabecera del TGBT), la corriente de cortocircuito trifásico presunta se calcula de forma conservadora a partir de la potencia nominal del transformador (S<sub>n</sub> en kVA) y su tensión de cortocircuito porcentual (U<sub>cc</sub>%):
  **I<sub>cc</sub> = S<sub>n</sub> / (√3 · U<sub>n</sub> · (U<sub>cc</sub>% / 100))**
  Donde U<sub>n</sub> es la tensión nominal entre fases (ej. 380 V). Este valor define el **poder de corte mínimo** (en kA) que deben poseer los interruptores automáticos del TGBT para despejar fallas de forma segura sin destruirse.

#### Aisladores de Baja Tensión
Para canalizaciones y barras del Tablero General de Distribución (TGBT) se emplean soportes aisladores mecánicos de resina epoxi o poliéster cargado con fibra de vidrio. Estos aisladores deben estar dimensionados no solo para resistir el esfuerzo dieléctrico, sino fundamentalmente para soportar las fuerzas electrodinámicas de repulsión mecánica que se manifiestan entre barras de cobre durante un cortocircuito severo.

