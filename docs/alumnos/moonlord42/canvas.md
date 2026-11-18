# Canvas · Generador de actas de examen como servicio

Modelo de negocio en una página (Business Model Canvas). Camino elegido: venta de servicios
(ver [caminos de ingreso](caminos-de-ingreso.md)).

| Bloque | Contenido |
|---|---|
| **1. Segmentos de clientes** | Secretarías de institutos superiores (técnicos y de formación docente) que inscriben a finales con un formulario de Google. Primer cliente: el ISFT N° 199 (Tigre), que ya la usa. En los institutos públicos suele pagar la asociación cooperadora. |
| **2. Propuesta de valor** | Las actas de todos los finales en un minuto, con la plantilla de siempre. Menos errores de tipeo, porque no se copian alumnos a mano. Avisa qué revisar: inscripciones repetidas, alumnos sin DNI y materias sin profesor. Los datos de los alumnos no salen de la computadora de Secretaría. |
| **3. Canales** | Demo en vivo con datos inventados. Recomendación entre secretarios y directivos de la misma región. Contacto directo con institutos vecinos de Zona Norte. Publicaciones en LinkedIn con el caso del ISFT 199. |
| **4. Relación con clientes** | Puesta en marcha acompañada: se prueba con los datos de un turno anterior antes de usarlo en serio. Soporte por WhatsApp durante cada turno de mesas. |
| **5. Fuentes de ingreso** | Pago único de puesta en marcha: $250.000 por instituto. Abono de $90.000 por turno de mesas (3 por año), o $240.000 por año, con el soporte incluido. Desde 2027, la inscripción a materias como módulo aparte. Ver [precios](#precios). |
| **6. Recursos clave** | El código, con tests automáticos, y el conocimiento del circuito de inscripción a finales de un instituto real. El ISFT 199 como cliente que ya la usa. |
| **7. Actividades clave** | Adaptar la herramienta a cada instituto. Dar soporte en los turnos de mesas. Mantener el código y sumar módulos: para 2027, la inscripción a materias. |
| **8. Socios clave** | El ISFT N° 199, que valida y recomienda. Docentes y directivos que conectan con otros institutos. GitHub y Vercel, que alojan el código y la página. |
| **9. Estructura de costos** | Mis horas de adaptación y soporte, que son el costo principal. Un dominio propio. El alojamiento es gratuito o casi gratuito, porque la página no usa servidor. |

## Precios

Pesos argentinos de noviembre de 2026. Con el dólar oficial a $1.575, $250.000 son unos USD 160.

| Concepto | Qué incluye | Horas | Precio |
|---|---|---|---|
| Puesta en marcha | Adaptar la lectura a su Forms y su acta volante, probar con un turno anterior y enseñarle a Secretaría a usarla. | 10 | $250.000, una sola vez |
| Abono por turno | Soporte por WhatsApp durante el turno y ajustes si cambian el Forms o la plantilla. | 3 a 4 | $90.000 por turno |
| Abono anual | Los 3 turnos de mesas (febrero-marzo, julio-agosto y diciembre). | 9 a 12 | $240.000 por año |

**De dónde salen los números.**
- **Valor de mi hora:** unos $25.000 (USD 16). Las referencias públicas para desarrolladores freelance en
  Argentina van de USD 15 a 25 por hora para un junior y de USD 30 a 55 para un senior. Tomé el piso
  porque estoy empezando.
- **Precio bajo a propósito:** un sistema de gestión escolar completo cuesta desde USD 250 por mes
  más IVA (unos $394.000 por mes). Mi herramienta hace una sola tarea, pero la hace bien, y el
  precio tiene que entrar en el presupuesto de una cooperadora.
- **Cómo se paga:** con factura C como monotributista.

**Cuentas de un año.** Cada instituto deja $490.000 el primer año (puesta en marcha más abono anual)
y $240.000 por año desde el segundo. Con 10 institutos son $2.400.000 por año de abonos, más las puestas en marcha. No reemplaza
un sueldo, pero es un ingreso que se repite y casi no tiene costos, porque no hay servidor que pagar.
Con el módulo de inscripción a materias, el abono puede subir.

## Supuestos para validar

- Que otros institutos inscriban a finales con un Forms parecido. Hay que confirmarlo hablando con 3 o 4 Secretarías.
- Cuánto tiempo les lleva hoy armar las actas a mano. Es lo que justifica el precio.
- Si prefieren pagar por turno de mesas o por año.
- Que el ISFT 199 esté de acuerdo en que ofrezca la herramienta a otros institutos y en que lo nombre
  como cliente. Los datos de sus alumnos nunca salen de su computadora, así que no se comparten.
