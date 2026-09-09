### De la estrategia a la ejecución

El **Modo Build** es donde el agente implementa el plan aprobado: crea, modifica y elimina archivos, ejecuta comandos y verifica los resultados. A diferencia de un "copiar y pegar" ciego, el Build asistido es **incremental y verificable**.

### Principios del Modo Build

1. **Cambios incrementales**: se avanza en pasos pequeños y comprensibles.
2. **Verificación continua**: después de cada paso se ejecutan los comandos de validación del proyecto.
3. **Supervisión humana**: vos revisás cada cambio antes de aceptarlo.
4. **Rollback fácil**: al trabajar sobre ramas o commits, podés deshacer lo que no funciona.

### El ciclo de verificación

El corazón del Build es el lazo **cambiar → verificar → corregir**:

```text
┌─────────────┐     ┌───────────────┐     ┌──────────────┐
│ Implementar │────▶│  Verificar    │────▶│  Corregir    │
└─────────────┘     │ (tests/lint)  │     │ (si falla)   │
                    └───────────────┘     └──────────────┘
                          ▲                      │
                          └──────────────────────┘
```

### Ejemplo de sesión Build

```text
Consigna (Modo Build):
"Implementá la función calcular_consumo_promedio según el plan.
Ejecutá los tests y corregí cualquier falla que aparezca."

Acciones esperadas del agente:
1. Crear la función en el módulo de métricas.
2. Agregar un test unitario con datos de ejemplo.
3. Ejecutar: python -m pytest tests/
4. Si falla, corregir el código o el test y repetir.
```

### Cómo supervisar la calidad

| Señal de alerta | Acción |
| :--- | :--- |
| Cambios fuera del alcance | Cancelar y reformular la consigna |
| Código que rompe tests | Pedir que lo corrija antes de continuar |
| Verificación omitida | Exigir que ejecute los comandos de validación |
| Cambios masivos sin explicación | Revisar el diff archivo por archivo |

### Resumen

- El Modo Build implementa el plan de forma incremental y verificable.
- El ciclo cambiar → verificar → corregir mantiene la calidad.
- La supervisión humana es parte del proceso, no un extra.
- Ante señales de alerta, cancelá y reformulá en lugar de aceptar a ciegas.
