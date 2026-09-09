### Publicar lo verificado

La **entrega continua** convierte los artefactos verificados por la CI en algo publicable. En proyectos de datos e IA, los "artefactos" suelen ser modelos entrenados, paquetes de código, contenedores o reportes.

### Tipos de artefactos

| Artefacto | Descripción | Publicación típica |
| :--- | :--- | :--- |
| Paquete de código | Librería instalable | PyPI, npm |
| Contenedor | Imagen lista para ejecutar | Docker Hub, GHCR |
| Modelo entrenado | Peso de un modelo | Registry de modelos, almacenamiento |
| Reporte | Documento o métricas | Páginas o artefactos del workflow |

### Publicar un modelo como artefacto

Un workflow puede entrenar y publicar un modelo de forma automatizada:

```yaml
name: Publicar modelo
on:
  workflow_dispatch:
  push:
    branches: [ main ]
    paths: [ "models/**" ]

jobs:
  entrenar-y-publicar:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt

      - name: Entrenar modelo
        run: python scripts/entrenar.py

      - name: Subir artefacto
        uses: actions/upload-artifact@v4
        with:
          name: modelo-entrenado
          path: models/artifacts/
```

### Integración con la asistencia de IA

El agente puede participar en el despliegue verificando consistencia:

```bash
opencode "Compará la configuración del nuevo modelo con la del anterior y reportá diferencias de esquema." --json
```

### Versionado y trazabilidad

Cada publicación debe ser **reproducible y auditable**:

1. **Etiquetado**: cada artefacto se asocia a un commit o tag.
2. **Metadatos**: registrar modelo, datos y configuración usados.
3. **Registro**: mantener un historial de qué versión está en cada entorno.
4. **Rollback**: poder volver a una versión anterior ante un problema.

### Publicación bajo control

| Paso | Acción |
| :--- | :--- |
| Verificar | Correr la CI completa antes de publicar |
| Etiquetar | Asociar el artefacto a una versión |
| Desplegar | Publicar en el registro correspondiente |
| Monitorizar | Observar el comportamiento en producción |

> El despliegue a producción debe requerir **autorización explícita**. Una tubería con aprobación humana evita publicar cambios no revisados.

### Resumen

- La entrega continua publica artefactos verificados (paquetes, contenedores, modelos).
- Los workflows de GitHub Actions automatizan entrenamiento y publicación.
- Versionado, metadatos y rollback garantizan trazabilidad.
- Toda publicación a producción requiere revisión y autorización explícita.
