# Lección 4.2: Implementación de un Servidor MCP en FastAPI para AGY, OpenCode y Aider en energy-ml

Hasta ahora, para que un modelo de lenguaje interactúe con una API REST tradicional, un desarrollador debía escribir manualmente prompts complejos o invocar llamadas `curl` ad-hoc. En 2024, la industria convergió hacia un estándar universal de interoperabilidad entre modelos de IA y aplicaciones externas: el **Model Context Protocol (MCP)**.

En esta lección transformamos ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md) en un **Servidor MCP nativo** sobre FastAPI. Esto permite que asistentes de desarrollo y agentes autónomos (**Antigravity CLI**, **OpenCode**, **Claude Code** y **Aider**) descubran dinámicamente las herramientas del sistema eléctrico, soliciten diagnósticos de telemetría y consulten reglas lógicas de manera transparente.

---

## 1. Fundamentos del Protocolo MCP (Model Context Protocol)

MCP es un protocolo abierto basado en **JSON-RPC 2.0** que estandariza tres primitivas centrales:

```
+--------------------------------------------------------------+
|                    Cliente / Host MCP                        |
|        (Antigravity CLI, OpenCode, Claude Code, Aider)       |
+--------------------------------------------------------------+
                               |
                   Petición JSON-RPC 2.0
                  (tools/list o tools/call)
                               v
+--------------------------------------------------------------+
|                     Servidor MCP                             |
|               (API FastAPI en energy-ml)                     |
+--------------------------------------------------------------+
        |                      |                      |
        v                      v                      v
  [ Inferencia ML ]     [ Catálogo Reglas ]    [ MLOps Metrics ]
```

1. **`tools/list`:** El cliente pregunta al servidor: *"¿Qué herramientas sabes ejecutar y qué parámetros requieres?"*. El servidor responde con la lista de herramientas documentadas con **JSON Schema**.
2. **`tools/call`:** El cliente solicita ejecutar una herramienta puntual pasando los argumentos validados. El servidor ejecuta la lógica de negocio y retorna el resultado estructurado.
3. **`resources` / `prompts`:** Primitivas adicionales para compartir documentos estáticos o plantillas de razonamiento.

---

## 2. Esquemas Pydantic v2 para JSON-RPC y Herramientas MCP

En `src/application/dtos/mcp_dto.py`:

```python
from typing import Any, Literal
from pydantic import BaseModel, ConfigDict, Field


class MCPToolParameterSchema(BaseModel):
    """Esquema JSON Schema de parámetros de una herramienta."""

    type: Literal["object"] = "object"
    properties: dict[str, dict[str, Any]]
    required: list[str]


class MCPToolDefinition(BaseModel):
    """Definición declarativa de una herramienta MCP."""

    name: str = Field(..., description="Nombre canónico de la tool")
    description: str = Field(..., description="Instrucciones para el agente")
    inputSchema: MCPToolParameterSchema


class MCPRequest(BaseModel):
    """Envelope JSON-RPC 2.0 para peticiones al servidor MCP."""

    model_config = ConfigDict(extra="ignore")

    jsonrpc: Literal["2.0"] = "2.0"
    id: int | str
    method: Literal["tools/list", "tools/call"]
    params: dict[str, Any] = Field(default_factory=dict)


class MCPTextContent(BaseModel):
    type: Literal["text"] = "text"
    text: str


class MCPResponse(BaseModel):
    """Envelope JSON-RPC 2.0 de respuesta."""

    jsonrpc: Literal["2.0"] = "2.0"
    id: int | str
    result: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
```

---

## 3. Catálogo de Herramientas y Ejecutor en energy-ml

En `src/infrastructure/fastapi/routes/mcp_server.py`, exponemos tres herramientas críticas del sistema eléctrico:

```python
import json
from typing import Any
from fastapi import APIRouter, status
from src.application.dtos.mcp_dto import (
    MCPRequest,
    MCPResponse,
    MCPToolDefinition,
    MCPToolParameterSchema,
)

router = APIRouter(prefix="/mcp", tags=["Model Context Protocol (MCP)"])

# Catálogo oficial de tools disponibles para agentes
CATALOGO_TOOLS: list[MCPToolDefinition] = [
    MCPToolDefinition(
        name="diagnosticar_telemetria_trafo",
        description="Evalúa el riesgo de falla térmica en un transformador a partir de su telemetría",
        inputSchema=MCPToolParameterSchema(
            properties={
                "temperatura_aceite": {
                    "type": "number",
                    "description": "Temperatura en °C",
                },
                "carga_pct": {
                    "type": "number",
                    "description": "Porcentaje de carga nominal (ej: 110.0)",
                },
                "vibracion_rms": {
                    "type": "number",
                    "description": "Vibración en mm/s",
                },
            },
            required=["temperatura_aceite", "carga_pct", "vibracion_rms"],
        ),
    ),
    MCPToolDefinition(
        name="consultar_reglas_operativas",
        description="Consulta las reglas lógicas activas inducidas por el motor simbólico",
        inputSchema=MCPToolParameterSchema(
            properties={
                "criticidad": {
                    "type": "string",
                    "enum": ["BAJA", "MEDIA", "CRITICA"],
                    "description": "Filtro de severidad",
                }
            },
            required=[],
        ),
    ),
]


def ejecutar_herramienta(tool_name: str, args: dict[str, Any]) -> str:
    """Despacha la ejecución hacia la lógica de negocio correspondiente."""
    if tool_name == "diagnosticar_telemetria_trafo":
        temp = float(args.get("temperatura_aceite", 0.0))
        carga = float(args.get("carga_pct", 0.0))
        vibracion = float(args.get("vibracion_rms", 0.0))

        if temp > 85.0 and carga >= 110.0:
            resultado = {
                "diagnostico": "DISPARO_CRITICO",
                "probabilidad": 0.985,
                "accion_recomendada": "Abrir interruptor de cabecera de inmediato",
            }
        else:
            resultado = {
                "diagnostico": "NORMAL",
                "probabilidad": 0.991,
                "accion_recomendada": "Mantener monitoreo continuo SCADA",
            }
        return json.dumps(resultado, ensure_ascii=False)

    elif tool_name == "consultar_reglas_operativas":
        criticidad = args.get("criticidad", "TODAS")
        resultado = {
            "filtro_aplicado": criticidad,
            "regla_aplicable": "SI temp > 85 °C AND carga >= 110% ENTONCES DISPARO_CRITICO",
            "soporte_casos": 412,
        }
        return json.dumps(resultado, ensure_ascii=False)

    return json.dumps(
        {"error": f"Herramienta desconocida: {tool_name}"}, ensure_ascii=False
    )


@router.post(
    "",
    response_model=MCPResponse,
    status_code=status.HTTP_200_OK,
    summary="Endpoint JSON-RPC para interactuar con agentes vía Model Context Protocol",
)
def handle_mcp_request(request: MCPRequest) -> MCPResponse:
    if request.method == "tools/list":
        return MCPResponse(
            id=request.id,
            result={
                "tools": [t.model_dump() for t in CATALOGO_TOOLS],
            },
        )

    elif request.method == "tools/call":
        tool_name = str(request.params.get("name", ""))
        tool_args = request.params.get("arguments", {})
        texto_resultado = ejecutar_herramienta(tool_name, tool_args)

        return MCPResponse(
            id=request.id,
            result={
                "content": [{"type": "text", "text": texto_resultado}],
            },
        )

    return MCPResponse(
        id=request.id,
        error={"code": -32601, "message": f"Método no soportado: {request.method}"},
    )
```

---

## 4. Configuración en Clientes Agénticos (AGY CLI / OpenCode / Claude Code)

Para conectar tu asistente de IA a este servidor, se define la configuración en el cliente local (por ejemplo en `~/.config/antigravity/mcp_servers.json` o en el archivo de configuración de OpenCode):

```json
{
  "mcpServers": {
    "energy-ml-service": {
      "type": "http",
      "url": "http://127.0.0.1:8000/mcp"
    }
  }
}
```

Al iniciar una sesión de desarrollo:
1. El agente invoca `tools/list` y descubre la tool `diagnosticar_telemetria_trafo`.
2. Cuando el usuario le indica en lenguaje natural: *"Revisa el estado de la subestación Pacheco con 92 °C y 115% de carga"*, el agente ejecuta de forma autónoma una llamada `tools/call` hacia nuestro endpoint de FastAPI.
3. El agente recibe el JSON estructurado con el diagnóstico y responde al operador humano con el plan de acción sugerido.

En la siguiente y última lección, abordaremos el **Taller Integrador Final**, donde se ensambla todo el pipeline de inferencia, observabilidad y orquestación con agentes.
---

## Autoevaluación Formativa y Caza de Código Alucinado

### Preguntas de Razonamiento Conceptual
1. ¿Por qué es crítico que un servidor MCP exponga el esquema exacto de argumentos que cada herramienta espera, en lugar de solo devolver descripciones en texto?
2. ¿Qué indicador de IA alucinadora verías si un servidor MCP no implementa el handshake inicial de inicialización?

### Caza de Código Alucinado (Code Review Inverso)
Observa el siguiente código generado por un asistente de IA:

```python
# CÓDIGO CON BUG DE PROTOCOLO GENERADO POR IA:
@app.post("/mcp/call_tool")
async def call_tool(tool_name: str, arguments: dict):
    # IA generó esto sin validar argumentos
    if tool_name == "predict":
        return predictor.predict(arguments)
    # ¡Sin schema validation, sin error handling de protocolo MCP!
```

**Diagnóstico del Revisor Humano:**
1. **Sin Validación de Esquema:** No verifica que los argumentos cumplan el contrato MCP.
2. **Sin Inicialización MCP:** No implementa `initialize`, `listTools`, etc.
3. **Corrección Obligatoria en energy-ml:**
   ```python
   from mcp.server import Server

   server = Server("energy-ml-mcp")

   @server.list_tools()
   async def list_tools():
       return [
           Tool(
               name="predict",
               description="Predice falla en base a telemetría",
               inputSchema={
                   "type": "object",
                   "properties": {
                       "temperatura_c": {"type": "number"},
                       "voltaje_v": {"type": "number"}
                   },
                   "required": ["temperatura_c", "voltaje_v"]
               }
           )
       ]

   @server.call_tool()
   async def call_tool(name: str, arguments: dict):
       if name == "predict":
           return predictor.predict(arguments["temperatura_c"], arguments["voltaje_v"])
   ```

---
