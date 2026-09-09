### Automatización local con hooks

Los **hooks de Git** son scripts que se ejecutan automáticamente en momentos clave del flujo de trabajo: antes de commitear, antes de pushear, etc. Combinados con el modo headless de OpenCode, permiten **validar en el equipo de cada desarrollador**.

### Hooks habituales

| Hook | Momento de ejecución | Uso típico |
| :--- | :--- | :--- |
| `pre-commit` | Antes de crear el commit | Lint, formato y chequeos rápidos |
| `commit-msg` | Antes de aceptar el mensaje | Validar convención del mensaje |
| `pre-push` | Antes de enviar al remoto | Tests completos y cobertura |

### Ejemplo: pre-commit con asistencia

```bash
#!/bin/bash
# .git/hooks/pre-commit
set -e

# Chequeo rápido de sintaxis
python -m compileall src/ -q

# Asistencia de IA para detectar problemas evidentes
opencode "Detectá errores obvios en los archivos modificados y reportalos." --json
```

> Los hooks de `.git/hooks/` son locales. Para compartirlos con el equipo, versionalos en `scripts/` y creá un instalador que los copie.

### Pre-push como barrera de calidad

El hook `pre-push` es ideal para validaciones que requieren más tiempo:

```bash
#!/bin/bash
# scripts/pre-push.sh (versionado en el repo)
pytest --cov=src --cov-fail-under=85 tests/
```

Si los tests fallan, el push se aborta y el desarrollador corrige antes de enviar.

### Cómo integrar el flujo

El patrón profesional combina los tres niveles:

```text
pre-commit  → validación rápida (lint, formato, asistencia IA)
pre-push    → validación completa (tests, cobertura)
CI (remoto) → validación final en el servidor
```

| Nivel | Velocidad | Cobertura de checks |
| :--- | :--- | :--- |
| Local pre-commit | Muy rápida | Básica |
| Local pre-push | Media | Completa |
| CI remoto | Lenta | Definitiva |

### Buenas prácticas

- **Hooks cortos**: los hooks locales deben ser rápidos para no frustrar al equipo.
- **Mensajes claros**: explicá por qué falló la validación y cómo corregirla.
- **Saltables con responsabilidad**: permití `--no-verify` solo para casos justificados.
- **Versionados**: compartí los hooks a través del repositorio.

### Resumen

- Los hooks de Git automatizan validaciones en el equipo local.
- `pre-commit` y `pre-push` combinan cheques rápidos con validaciones completas.
- OpenCode headless puede sumar revisión asistida a los hooks.
- Una jerarquía de validaciones local + remota protege la calidad del proyecto.
