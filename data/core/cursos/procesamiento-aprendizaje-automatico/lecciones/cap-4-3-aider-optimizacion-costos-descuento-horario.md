# Guía de Laboratorio — Lección 4.3: Optimización y Cautela Financiera en Aider: 2 USD Prepago, Horario Valle y Commits Atómicos

**Asignatura:** Nivel 0 — Procesamiento y Aprendizaje Automático Inicial  
**Capítulo 4:** Ecosistema Avanzado de IA Agéntica: Claude Code, Aider y Arneses Autónomos  
**Carga horaria estimada:** 25 min  
**Prerrequisitos:** Haber completado la Lección 4.2 (Aider y Repomap).

---

## 1. La Regla de Oro del Pago por Uso: Cautela y Control Presupuestario

En las suscripciones mensuales fijas (como los 5 USD de Antigravity CLI o los 20 USD de Claude Code), existe una barrera de contención natural: pagas una cuota y no puedes gastar más dinero ese mes, incluso si utilizas el servicio intensamente.

En cambio, las **APIs de pago por uso (*Pay-as-you-go*)** operan bajo un modelo de facturación por consumo granular de tokens. Si un desarrollador descuidado deja un agente en un bucle autónomo sin supervisión o comete un error en un script que llama a una API costosa en un bucle `while True`, la factura al cierre del ciclo puede generar una desagradable sorpresa.

Por este motivo, en la carrera técnica del ISFT N° 199 enseñamos la **estrategia de seguridad financiera basada en saldo prepago controlado**.

---

## 2. Configuración de Seguridad: Saldo Prepago de 2 USD en DeepSeek

Para utilizar Aider sin ningún tipo de riesgo financiero, aplicamos este protocolo:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                   PROTOCOLO DE SEGURIDAD FINANCIERA                    │
├────────────────────────────────────────────────────────────────────────┤
│ 1. Crear cuenta en https://platform.deepseek.com/                      │
│ 2. Cargar un saldo prepago inicial de exactamente 2 USD.               │
│ 3. Comprobar que "Auto-recharge" (recarga automática) esté en OFF.     │
│ 4. Definir un límite estricto de gasto mensual (Spending Limit).       │
└────────────────────────────────────────────────────────────────────────┘
```

Al operar con saldo prepago, el peor escenario posible ante cualquier error humano es que el agente agote los 2 USD y se detenga con un mensaje `Insufficient Balance`. Jamás se generará una deuda sobre tu tarjeta bancaria.

---

## 3. ¿Por Qué DeepSeek es el Proveedor Más Competitivo del Mercado?

Para comprender la magnitud del ahorro, comparemos las tarifas por millón de tokens entre los principales proveedores de IA:

| Proveedor / Modelo | Input (Entrada) por Millón | Output (Salida) por Millón | Relación de Costo |
| :--- | :--- | :--- | :--- |
| **Claude 3.5 Sonnet** | ~3,00 USD | ~15,00 USD | Base de referencia |
| **GPT-4o** | ~2,50 USD | ~10,00 USD | Base de referencia |
| **DeepSeek-V3 / Chat (Tarifa Base)** | **~0,14 USD** | **~0,28 USD** | **20 a 50 veces más económico** |
| **DeepSeek (Horario Valle / Off-Peak)** | **~0,07 USD** | **~0,14 USD** | **40 a 100 veces más económico** |

### El Descuento de Horario Valle (*Off-Peak Discount*)

DeepSeek premia a los desarrolladores que operan fuera de los picos de demanda global aplicando un **descuento automático del 50%**:
* **Ventana Horaria Valle:** De **16:30 a 00:30 UTC** de cada día.
* **Horario Local en Argentina (UTC-3):** De **13:30 a 21:30 hs**.

Esto coincide precisamente con el turno vespertino y de cursada del instituto. En esa franja horaria, tus **2 USD te otorgan acceso a más de 14 millones de tokens**, lo que alcanza para cientos de sesiones completas de programación técnica.

---

## 4. Taller Práctico con Aider sobre `energy-ml`

Navegamos a nuestro repositorio local:

```bash
cd ~/proyectos_software/energy-ml
source .venv/bin/activate
export DEEPSEEK_API_KEY="sk-tu-clave-aqui"
```

Iniciamos Aider vinculándolo a DeepSeek y cargando `src/pipeline.py`:

```bash
aider --model deepseek/deepseek-chat src/pipeline.py
```

### Paso 1: Petición Técnica Precisa

En la consola de Aider escribimos:

> *"En `src/pipeline.py`, añade la función `calcular_estadisticas_consumo(valores: list[float]) -> dict[str, float]`. Debe calcular la media, el percentil 95 y el valor máximo. Retorna los resultados redondeados a 2 decimales y maneja listas vacías retornando ceros. Incluye Type Hints completos y docstring explicativo."*

### Paso 2: Observación del Flujo de Ejecución

Observa lo que ocurre en la terminal:
1. DeepSeek genera el bloque de reemplazo (*diff*) con un costo de tokens ínfimo.
2. Aider aplica el cambio de forma quirúrgica en `src/pipeline.py`.
3. Al detectar que el repositorio Git está configurado, Aider **crea automáticamente un commit atómico**:
   ```text
   Commit 7f3a8b1: Agregar función calcular_estadisticas_consumo en src/pipeline.py

```
4. Aider muestra en la esquina inferior el costo de la interacción: normalmente **menos de 0,004 USD** (menos de medio centavo de dólar).

---

## 5. Salir de Aider e Inspeccionar el Historial

Escribe `/exit` para finalizar la sesión interactiva y audita el historial con Git:

```bash
git log -n 1 --stat
git show HEAD
```

Comprobarás que Aider implementó el código con rigor y documentó el historial sin que tuvieses que redactar el commit a mano.

---

## 6. Conclusión

Aprender a operar con APIs bajo el modelo de pago por uso de forma controlada y prudente es una habilidad técnica esencial. Demuestra madurez profesional: saber aprovechar proveedores hiper-competitivos como **DeepSeek**, proteger la economía personal con **saldo prepago de 2 USD** y maximizar el rendimiento mediante **descuentos de horario valle**.

En la última lección del capítulo, cerraremos el panorama conociendo los **arneses de IA agéntica (Codex, Kimi Code y DPH)**.
