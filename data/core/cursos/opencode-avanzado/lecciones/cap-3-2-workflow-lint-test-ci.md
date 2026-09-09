### Un pipeline con calidad garantizada

El primer workflow profesional combina **lint**, **tests** y la **asistencia de IA** para garantizar que ningún cambio rompa la calidad del proyecto.

### Workflow: lint + test

El siguiente flujo se ejecuta en cada push y pull request hacia `main`:

```yaml
name: CI
on:
  push:
    branches: [ main ]
  pull_request:

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Instalar dependencias
        run: |
          pip install --upgrade pip
          pip install -r requirements.txt -r requirements-dev.txt

      - name: Lint
        run: ruff check src/

      - name: Tests con cobertura
        run: pytest --cov=src --cov-fail-under=85 tests/
```

### Añadir la asistencia de IA a la tubería

OpenCode en modo headless puede participar de la CI, por ejemplo para **revisar** el código o **sugerir** mejoras antes de que el cambio se fusione:

```yaml
      - name: Revisión asistida con OpenCode
        run: |
          opencode "Revisá el diff de este PR. Indicá riesgos, bugs y mejoras de rendimiento." --json
```

> En entornos CI, el agente necesita credenciales seguras (secrets) y un límite de recursos para no bloquear la tubería.

### Buenas prácticas en CI con IA

| Práctica | Razón |
| :--- | :--- |
| Fijar versiones de dependencias | Resultados reproducibles entre corridas |
| Secrets en GitHub | Nunca exponer claves en el código |
| Timeouts | Evitar ejecuciones infinitas |
| Ejecutar la IA en un job separado | No retrasar el pipeline principal |
| Cachear dependencias | Acelerar la tubería |

### Validación del workflow

Antes de confiar en el pipeline, verificá:

1. **Trigger correcto**: se ejecuta en los eventos esperados.
2. **Instalación reproducible**: las dependencias se resuelven desde cero.
3. **Umbral de cobertura**: falla si la calidad baja.
4. **Logs claros**: el equipo entiende el motivo de cada falla.

### Resumen

- Un workflow de CI combina lint, tests y validación de cobertura.
- OpenCode headless puede sumar revisión asistida dentro de la tubería.
- Fijá versiones, usá secrets, definí timeouts y cacheá dependencias.
- Validá el pipeline desde cero antes de adoptarlo como estándar.
