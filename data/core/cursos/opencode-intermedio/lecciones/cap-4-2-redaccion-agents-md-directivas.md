### Escribir directivas efectivas

Un AGENTS.md útil es **específico**, **accionable** y **medible**. Las directivas vagas generan comportamiento inconsistente; las directivas concretas producen resultados predecibles.

### De lo vago a lo concreto

| Vago | Concreto |
| :--- | :--- |
| "Seguí buenas prácticas" | "No escribas lógica de negocio dentro de las rutas HTTP" |
| "Testeá tu código" | "Ejecutá `pytest` tras cada modificación al código fuente" |
| "No rompas nada" | "No reduzcas la cobertura por debajo del 85%" |
| "Documentá" | "Toda función pública debe tener docstring en español" |

### Directivas recomendadas

**1. Arquitectura y estructura**

```markdown
## Arquitectura
- El código se organiza en capas: domain, application, infrastructure.
- No se permite lógica de acceso a datos dentro de los endpoints.
- La capa de dominio solo usa Pydantic.
```

**2. Validación obligatoria**

```markdown
## Control de calidad
- Ejecutar: pytest
- Verificar cobertura: pytest --cov=src tests/
- No reducir la cobertura existente.
```

**3. Prohibiciones explícitas**

```markdown
## Prohibiciones
- No hardcodear datos de contenido en el código.
- No desplegar a producción sin autorización explícita.
```

### Errores comunes al redactar

- **Demasiado largo**: si el documento supera lo esencial, los agentes pierden el foco. Priorizá.
- **Sin comandos concretos**: las instrucciones sin comandos verificables son difíciles de cumplir.
- **Contradictorio**: una sección que pide una cosa y otra que pide lo contrario confunde al agente.
- **Desactualizado**: un AGENTS.md que no refleja el estado real del repo es peor que ninguno.

### Validación del documento

Probalo con una tarea real: pedile al agente una modificación simple y verificá que:

1. Respete las capas y convenciones definidas.
2. Ejecute los comandos de validación indicados.
3. No viole ninguna prohibición.

Si falla en alguno de estos puntos, la directiva está mal redactada o es ambigua.

### Resumen

- Las directivas efectivas son específicas, accionables y medibles.
- Incluí arquitectura, validaciones obligatorias y prohibiciones.
- Evitá documentos largos, vagos o contradictorios.
- Validá el AGENTS.md con una tarea real y ajustá según el resultado.
