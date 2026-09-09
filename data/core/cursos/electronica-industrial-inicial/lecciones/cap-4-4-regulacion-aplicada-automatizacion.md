### Del algoritmo al proceso real

Un PID "en el papel" es una ecuación. En la planta, es un bloque que corre dentro de un PLC o un controlador dedicado, conectado a sensores y actuadores reales. Esta lección repasa cómo se **aplica** la regulación a la automatización industrial.

### Dónde vive el PID

El control PID puede implementarse en:

- **PLC:** como bloque de función PID dentro del programa (la opción más común en automatización).
- **Controlador dedicado:** un lazo simple (temperatura de un horno) con su propio PID.
- **Variador de frecuencia:** PID interno para regular caudal o presión (ej. bomba).
- **SCADA/DCS:** en sistemas distribuidos de gran escala.

### Casos típicos por variable

| Variable | Actuador típico | Control habitual |
| :--- | :--- | :--- |
| Temperatura | Resistencia, quemador, válvula de vapor | PI o PID |
| Presión | Válvula, variador de bomba | PI |
| Nivel | Bomba, válvula de llenado | P o PI |
| Caudal | Válvula proporcional, VFD | PI |
| Velocidad / posición | Servomotor, VFD | PID (con rampas) |

### El PID dentro del scan del PLC

Como el PLC ejecuta en ciclos de scan, el PID se calcula **una vez por scan**. Por eso el **período de muestreo** (cada cuánto se ejecuta el PID) debe ser adecuado a la dinámica del proceso:

- Procesos rápidos (presión, caudal): muestreo corto (decenas de ms).
- Procesos lentos (temperatura): muestreo de segundos.

Un muestreo mal elegido degrada la regulación: si es muy lento, el control llega tarde; si es muy rápido, se amplifica el ruido.

### Arranque y seguridades

Al aplicar la regulación conviene cuidar:

1. **Rampas de consigna:** subir/bajar el SP gradualmente para no saturar el actuador.
2. **Límites de salida (MV min/max):** proteger el actuador (ej. no abrir la válvula más de 90%).
3. **Modo manual/automático:** permitir al operador tomar control en arranque o falla.
4. **Anti-windup:** evitar que el término integral se "dispare" cuando el actuador está saturado.

### El anti-windup explicado

Si el actuador llega a su tope (ej. válvula 100% abierta) y el error persiste, el término integral sigue acumulando un valor enorme. Cuando el error cambia de signo, esa acumulación tarda en "descargarse" y provoca un sobrepico. El **anti-windup** congela o limita la integral mientras la salida está saturada.

### Micro-desafío práctico

> Un sistema de bombeo regula presión con un VFD y un PID interno. ¿Qué protecciones configurarías (rampa, límites, anti-windup) y por qué? Justificá cada una en una línea.

### Resumen

- El PID se implementa en **PLC, controladores dedicados, VFD o DCS**.
- El **período de muestreo** debe ajustarse a la dinámica del proceso.
- Se agregan **rampas**, **límites de MV** y **modo manual/automático** por seguridad.
- El **anti-windup** evita el sobrepico causado por la saturación del término integral.
