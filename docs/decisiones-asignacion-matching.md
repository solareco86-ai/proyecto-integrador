# Decisiones del algoritmo de asignación

## Decisión principal

La primera propuesta automática utiliza **matching bipartito por franja horaria exacta**.

```text
Comisiones ↔ Aulas compatibles
```

Una arista existe cuando el aula tiene capacidad suficiente para la comisión. En una misma franja, un aula no puede asignarse a dos comisiones.

## Por qué se eligió este enfoque

- Es explicable para el Proyecto Integrador.
- Permite demostrar una solución real sin resolver todavía todo el problema de horarios.
- Detecta cuándo una comisión queda sin alternativas.
- Permite reutilizar un aula en horarios diferentes.
- Se puede extender posteriormente con equipamiento, edificios y preferencias.

## Criterio de asignación

1. Se agrupan las sesiones por día, hora de inicio y hora de fin.
2. Se calculan las aulas compatibles por capacidad, tipo y requerimientos.
3. Se priorizan las comisiones con menos alternativas.
4. Se busca un matching máximo mediante búsquedas aumentantes.
5. Las comisiones sin aula se exportan con el motivo.

## Resultado del dataset sintético

Con los datos sintéticos actuales:

- Sesiones procesadas: 9.
- Sesiones asignadas: 8.
- Sesiones sin asignar: 1.
- Aulas reutilizadas en horarios diferentes: sí.

La sesión `S008` queda sin asignar porque requiere el único laboratorio de computación en una franja en la que ya está ocupado por `S002`.

Los resultados completos se generan en:

```text
tmp/grafos-asignacion-aulas/asignaciones.csv
tmp/grafos-asignacion-aulas/comisiones-sin-asignar.csv
```

## Limitaciones actuales

- Los horarios deben estar definidos previamente.
- Se consideran franjas exactas; todavía no se modelan superposiciones parciales.
- No se consideran docentes, distancia entre sedes ni preferencias.
- El matching maximiza la cantidad de comisiones asignadas, pero todavía no optimiza calidad o comodidad.

## Patrones que se podrán estudiar

- Comisiones con una única aula compatible.
- Aulas utilizadas por muchas comisiones.
- Franjas con demanda superior a la oferta.
- Comisiones que quedan sin solución por capacidad.
- Diferencias entre la asignación manual y la propuesta automática.

## Evolución futura

El siguiente nivel puede agregar pesos a las aristas y convertir el matching en una optimización: minimizar aulas sobredimensionadas, priorizar equipamiento, reducir cambios de edificio y comparar distintas soluciones.
