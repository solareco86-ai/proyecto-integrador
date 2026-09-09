### Automatizar con el agente

Combinar el modo headless con scripts permite construir **tareas repetibles** donde el agente actúa como un paso más del flujo. El objetivo es que la automatización sea consistente y auditable.

### Diseño de un script de automatización

Un script bien diseñado sigue una secuencia clara:

```text
1. Preparar el entorno (variables, directorio, modelo).
2. Definir la consigna del agente.
3. Ejecutar OpenCode en modo headless.
4. Capturar la salida y validar el resultado.
5. Reportar el estado (éxito/fallo) al proceso que lo invoca.
```

### Ejemplo: actualizar dependencias documentadas

```bash
#!/bin/bash
# scripts/actualizar_docs.sh
set -e

echo "Generando documentación de dependencias con OpenCode..."
opencode \
  "Generá una tabla en README.md con las dependencias del proyecto, su versión y para qué se usan." \
  --json > /tmp/opencode_docs.json

echo "Verificando que el archivo haya cambiado..."
git diff --name-only | grep -q README.md && echo "OK: README actualizado" || echo "Sin cambios"
```

### Validación dentro del script

La automatización no reemplaza el control de calidad. El script debe:

| Paso | Validación |
| :--- | :--- |
| Entrada | Confirmar que el repositorio esté en el estado esperado |
| Ejecución | Verificar que el agente completó sin errores |
| Salida | Correr los tests y el linter después del cambio |
| Estado | Devolver un código de salida correcto (0 éxito, distinto de 0 fallo) |

### Orquestación con otras herramientas

El agente puede encadenarse con procesadores de datos, validadores y sistemas de notificación:

```bash
opencode "Limpiá el pipeline en src/data/pipeline.py" --json \
  && python -m pytest tests/ \
  && echo "Pipeline validado" | logger
```

### Errores comunes en la automatización

- **Sin control de errores**: si el agente falla, el script debe detenerse de forma clara.
- **Consignas no repetibles**: frases ambiguas producen resultados distintos en cada corrida.
- **Sin validación posterior**: aceptar los cambios del agente sin tests es peligroso.
- **Logs excesivos**: dificultan identificar el punto de falla en procesos largos.

### Resumen

- Los scripts con OpenCode headless hacen repetibles las tareas asistidas.
- Diseñá secuencias claras: preparar, ejecutar, validar y reportar.
- Siempre corré tests y linters después de los cambios del agente.
- Controlá errores y usá consignas deterministas para resultados confiables.
