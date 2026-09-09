### ¿Qué es CI/CD?

**CI/CD** (Integración Continua y Entrega Continua) es la práctica de automatizar la verificación y publicación del software. La **integración continua** valida cada cambio de código; la **entrega continua** prepara y publica los artefactos de forma automatizada.

### La tubería como red de seguridad

Cada cambio que llega al repositorio atraviesa una serie de pasos automáticos:

```text
Commit ──▶ Checkout ──▶ Instalar deps ──▶ Lint ──▶ Test ──▶ Build ──▶ Publicar
```

Si cualquier paso falla, la tubería se detiene y el equipo recibe el aviso antes de que el cambio llegue a producción.

### Conceptos de GitHub Actions

GitHub Actions organiza la automatización en tres niveles:

| Concepto | Descripción |
| :--- | :--- |
| **Workflow** | Archivo YAML que define un proceso automatizado completo |
| **Job** | Conjunto de pasos que se ejecutan en un runner |
| **Step** | Acción individual dentro de un job (instalar, testear, publicar) |

### Triggers (disparadores)

Un workflow se dispara por eventos del repositorio:

```yaml
on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
```

### Estructura mínima de un workflow

```yaml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt
      - run: pytest
```

### Beneficios para proyectos de datos

- **Regresión controlada**: los modelos y pipelines se validan ante cada cambio.
- **Reproducibilidad**: la misma versión de dependencias en cada corrida.
- **Señal temprana**: un test que falla se detecta en minutos, no al desplegar.
- **Despliegue seguro**: los artefactos verificados llegan a producción con confianza.

### Resumen

- CI/CD automatiza la validación y publicación del software.
- GitHub Actions organiza la automatización en workflows, jobs y steps.
- Los triggers (`on:`) definen cuándo se ejecuta cada flujo.
- Una tubería bien configurada actúa como red de seguridad ante cada cambio.
