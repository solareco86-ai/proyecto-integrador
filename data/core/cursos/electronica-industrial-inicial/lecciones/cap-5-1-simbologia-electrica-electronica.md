### ¿Por qué normalizar los símbolos?

Un plano de electrónica industrial debe poder leerse igual en cualquier planta del mundo. Para eso existen **normas de simbología** que estandarizan el dibujo de cada componente. Las dos grandes familias:

- **IEC (Comisión Electrotécnica Internacional):** predominante en Argentina, Europa y Latinoamérica. Símbolos simples y abstractos.
- **ANSI/NEMA (americana):** usada en EE. UU. y plantas de origen estadounidense. Símbolos más "físicos".

Saber leer ambas es clave porque en una planta conviven equipos de distintos orígenes.

### Símbolos eléctricos fundamentales

| Componente | Símbolo IEC (concepto) | Función |
| :--- | :--- | :--- |
| Contacto NA (normalmente abierto) | Dos líneas separadas | Conduce al cerrarse |
| Contacto NC (normalmente cerrado) | Dos líneas con trazo que las une | Conduce en reposo, abre al accionarse |
| Bobina (relé/contactor) | Rectángulo con designación | Energiza contactos al recibir señal |
| Fusible | Rectángulo con línea interior | Protección contra cortocircuito |
| Pulsador NA | Botón con contacto abierto | Cierra el circuito al presionar |
| Lámpara | Círculo con cruz | Señalización |
| Motor | Círculo con letra M | Carga rotativa |
| Tierra (PE) | Tres trazos horizontales | Protección |

### Designaciones de componentes

Cada componente lleva una **letra de clase** que indica su función, según IEC 81346:

| Letra | Componente |
| :--- | :--- |
| K | Relés, contactores |
| Q | Interruptores, seccionadores, disyuntores |
| F | Fusibles, protecciones |
| M | Motores |
| S | Pulsadores, finales de carrera |
| T | Transformadores |
| X | Borneras, conectores |

### Contactos NA y NC: la confusión clásica

- **NA (NO):** en **reposo** está abierto; se cierra al accionar el elemento.
- **NC:** en **reposo** está cerrado; se abre al accionar.

Un error frecuente es pensar que "NC" significa "contacto de seguridad siempre abierto". En realidad, un contacto NC en una puerta de seguridad mantiene el circuito cerrado cuando la puerta está **cerrada** y lo abre (corta) cuando la puerta se **abre**.

### Referencias cruzadas en el plano

En planos profesionales, cada contacto de un relé indica **dónde está su bobina** y viceversa (referencias cruzadas con número de hoja y coordenadas). Esto permite navegar el plano sin perderse.

### Micro-desafío práctico

> Dibujá con símbolos IEC un circuito simple: un pulsador NA `S1` que energiza la bobina `K1`, y un contacto `K1` (NA) que enciende una lámpara `H1`. Identificá cada símbolo con su letra de clase.

### Resumen

- **IEC** (símbolos abstractos) y **ANSI/NEMA** (símbolos físicos) son las dos familias.
- Contacto **NA** (abre en reposo) y **NC** (cierra en reposo) son la base de la lectura.
- Las **letras de clase** (K, Q, F, M, S, T, X) indican la función del componente.
- Las **referencias cruzadas** vinculan bobinas y contactos entre hojas del plano.
