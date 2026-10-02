### Implementación de un servidor MCP en FastAPI para AGY, OpenCode y Aider

El protocolo **MCP** (*Model Context Protocol*) estandariza la forma en que los modelos de lenguaje y agentes descubren e invocan herramientas externas en tiempo de ejecución.

#### Exposición de Tools MCP desde FastAPI
Implementamos un endpoint que provee el esquema de herramientas y maneja la ejecución de llamadas remotas:
```python
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/mcp", tags=["Model Context Protocol"])

class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict

class ToolCallRequest(BaseModel):
    tool_name: str
    arguments: dict

@router.get("/tools", response_model=list[ToolDefinition])
def listar_herramientas() -> list[ToolDefinition]:
    return [
        ToolDefinition(
            name="clasificar_evento",
            description="Clasifica un evento de sensores utilizando el modelo supervisado activo",
            parameters={
                "type": "object",
                "properties": {
                    "temperatura": {"type": "number"},
                    "vibracion": {"type": "number"}
                },
                "required": ["temperatura", "vibracion"]
            }
        )
    ]
```
Con este protocolo, herramientas de desarrollo como AGY o Aider pueden conectar su razonamiento a nuestra API de Machine Learning de forma nativa.
