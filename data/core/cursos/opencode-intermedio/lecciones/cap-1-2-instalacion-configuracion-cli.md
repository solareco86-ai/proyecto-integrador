### Instalación de OpenCode

El primer paso es instalar la CLI en tu sistema. OpenCode se distribuye como un paquete de **Node.js**, por lo que necesitás una versión de Node disponible (se recomienda una versión LTS reciente).

```bash
npm install -g opencode
```

Después de la instalación, verificá que el comando esté disponible:

```bash
opencode --version
```

> Si preferís no instalar de forma global, también podés usar `npx opencode`, que descarga y ejecuta el paquete bajo demanda. La instalación global es más cómoda para uso diario.

### Configuración inicial y proveedores

Para que el agente funcione necesita acceso a un modelo de lenguaje. OpenCode se conecta a distintos **proveedores** (API remota, modelos locales, etc.). La configuración se almacena en un archivo de entorno que no debe versionarse:

```bash
cp .env.example .env
```

El archivo `.env` típico contiene la clave de API del proveedor:

```dotenv
# Proveedor de API remota
OPENAI_API_KEY=sk-xxxxxxxx
# o alternativas: ANTHROPIC_API_KEY, GEMINI_API_KEY, etc.
```

Nunca commitees el archivo `.env`: agregalo a `.gitignore` para evitar exponer credenciales.

### Verificación del entorno

Una vez configurada la clave, ejecutá OpenCode en un directorio de prueba:

```bash
opencode
```

Si el agente responde correctamente a una consigna simple, el entorno está listo.

### Solución de problemas comunes

| Problema | Posible causa | Solución |
| :--- | :--- | :--- |
| `command not found` | npm no instaló en el PATH | Reinstalá o usá `npx opencode` |
| Error de autenticación | Clave ausente o inválida en `.env` | Verificá el archivo y la variable |
| Respuesta lenta | Modelo remoto cargado | Probá con un modelo más pequeño |

### Resumen

- Instalá con `npm install -g opencode` y verificá con `opencode --version`.
- Configurá un proveedor de modelo mediante el archivo `.env`.
- Mantené las credenciales fuera del control de versiones.
- Validá el entorno con una consigna simple antes de trabajar en proyectos reales.
