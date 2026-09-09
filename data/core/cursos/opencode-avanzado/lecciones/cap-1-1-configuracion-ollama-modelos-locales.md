### ¿Por qué ejecutar modelos locales?

Los modelos de lenguaje alojados en la nube ofrecen potencia, pero no siempre son la mejor opción. Ejecutar modelos locales mediante **Ollama** permite mantener el código y los datos dentro de tu infraestructura, trabajar sin conexión y controlar los costos.

### Instalación de Ollama

Ollama se instala de forma nativa según el sistema operativo. En Linux:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Para otras plataformas se descarga el instalador oficial. Luego se verifica que el servidor esté activo:

```bash
ollama --version
```

### Descarga de modelos

Ollama funciona con una línea de comandos simple para descargar y administrar modelos:

```bash
# Listar modelos descargados
ollama list

# Descargar un modelo (ej. un LLM liviano)
ollama pull llama3.2

# Ejecutar una prueba interactiva
ollama run llama3.2 "Hola, resumime cómo funciona un modelo de lenguaje"
```

### Criterios para elegir un modelo

| Criterio | Consideración |
| :--- | :--- |
| Recursos disponibles | Modelos grandes exigen GPU y RAM abundante |
| Tarea | Modelos pequeños sirven para generación simple |
| Calidad del código | Para asistencia en desarrollo conviene priorizar capacidad de razonamiento |
| Privacidad | Modelos locales nunca envían datos a la nube |

### Verificación del servicio

Antes de integrarlo con OpenCode, confirmá que el endpoint local responde:

```bash
curl http://localhost:11434/api/tags
```

Una respuesta con la lista de modelos descargados indica que el servidor está listo.

### Resumen

- Ollama permite ejecutar modelos de lenguaje de forma local.
- Instalá Ollama, descargá un modelo con `ollama pull` y probalo con `ollama run`.
- Elegí el modelo según recursos, tarea y necesidades de privacidad.
- Verificá el servicio local antes de conectarlo a otras herramientas.
