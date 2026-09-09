### Conectar OpenCode con Ollama

Una vez que Ollama corre localmente, OpenCode puede usarlo como **proveedor de modelo**. La integración se configura declarando el endpoint local, sin necesidad de claves de API externas.

### Configuración del proveedor local

OpenCode permite definir proveedores a través de su archivo de configuración. El patrón general es apuntar el modelo al servidor local de Ollama:

```dotenv
# .env (configuración local)
OPENCODE_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434
```

> Los nombres de variables y la estructura exacta dependen de la versión de OpenCode instalada. Consultá la documentación de configuración de tu versión para los nombres correctos.

### Prueba de conexión

Ejecutá OpenCode y pedile una tarea simple que use el modelo local:

```bash
opencode
```

Consigna de prueba:

```text
"Escribí una función Python que calcule la media móvil de una serie temporal."
```

Si la respuesta proviene del modelo local, la integración está funcionando.

### Ventajas de usar modelos locales

| Ventaja | Descripción |
| :--- | :--- |
| Privacidad | El código y los datos no salen del equipo |
| Sin conexión | Trabajás sin depender de internet |
| Costo | Sin costos por token en proveedores externos |
| Control | Elección exacta del modelo y de su configuración |

### Limitaciones a considerar

- **Rendimiento**: los modelos locales pueden ser más lentos que los grandes modelos en la nube.
- **Calidad**: para tareas complejas de razonamiento, un modelo local pequeño puede quedarse corto.
- **Recursos**: se requieren suficiente RAM y, para modelos grandes, GPU.

### Estrategia híbrida

Muchos equipos combinan ambos mundos: modelos locales para tareas sensibles o rutinarias y modelos remotos para tareas de alto razonamiento. La configuración por proyecto permite elegir el proveedor según la consigna.

### Resumen

- OpenCode se integra con Ollama apuntando al endpoint local.
- Configurá el proveedor y validá con una tarea simple.
- Los modelos locales aportan privacidad, autonomía y control de costos.
- Considerá una estrategia híbrida según la sensibilidad y complejidad de la tarea.
