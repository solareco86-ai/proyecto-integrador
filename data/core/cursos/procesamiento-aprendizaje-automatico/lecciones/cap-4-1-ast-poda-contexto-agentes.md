# Lección 4.1: Cómo Leen Código los Agentes: Árboles de Sintaxis Abstracta (AST) y Poda de Contexto en energy-ml

A lo largo del curso aprendimos a construir y desplegar modelos de Machine Learning y reglas lógicas en ↗ [energy-ml](file:///home/agustin/proyectos_software/proyecto-integrador/data/core/cursos/procesamiento-aprendizaje-automatico/lecciones/cap-1-3-git-clone-proyecto-energy-ml.md). Sin embargo, una pregunta fundamental para todo ingeniero de software e IA es: **¿Cómo interactúan realmente los agentes de código (como AGY CLI, OpenCode o Aider) con repositorios de miles de líneas?**

La respuesta intuitiva —"el agente lee todos los archivos enteros y se los envía al modelo de lenguaje"— es económicamente inviable y técnicamente errónea. Enviar archivos completos colapsaría la ventana de contexto de los modelos, diluiría la atención del LLM y dispararía facturas exorbitantes en APIs comerciales.

En esta lección descubrimos cómo la **poda determinística basada en Árboles de Sintaxis Abstracta (AST)** en la CPU local ($0 tokens) permite a los agentes razonar sobre arquitecturas complejas con una fracción mínima de tokens.

---

## 1. El Cuello de Botella del Contexto y el Desperdicio de Tokens

Cuando un agente de IA necesita comprender cómo interactúa un endpoint de FastAPI con un servicio de inferencia en `energy-ml`, no requiere ver los detalles internos de implementación de cada función auxiliar, sino sus **contratos de interfaz**:
- ¿Qué clases existen?
- ¿Qué métodos públicos exponen?
- ¿Cuáles son los tipos de entrada y salida (`type hints`)?
- ¿Qué docstrings describen la precondición o postcondición?

```
Archivo Completo (1.500 tokens)          Esqueleto AST Podado (180 tokens)
+-------------------------------+        +-------------------------------+
| class PredictorService:       |        | class PredictorService:       |
|   def __init__(self, path):   |        |   def __init__(...): ...      |
|     # 40 líneas de setup      |        |                               |
|     ...                       |  ===>  |   def predict(                |
|   def predict(self, x: In)    |        |     self, x: TelemetriaInput  |
|       -> PrediccionOut:       |        |   ) -> PrediccionOut:         |
|     # 80 líneas de cálculo    |        |     """Docstring del método"""|
|     # bucles, loggers, etc.   |        |     ...                       |
+-------------------------------+        +-------------------------------+
       [Gasto excesivo de tokens]                [88% de Ahorro en Contexto]
```

La CPU local del desarrollador (o del estudiante) puede analizar la gramática formal del lenguaje en menos de 5 milisegundos sin enviar un solo byte a la nube.

---

## 2. ¿Qué es un Árbol de Sintaxis Abstracta (AST)?

El AST (*Abstract Syntax Tree*) es la estructura de datos jerárquica en forma de árbol que genera el compilador o intérprete de Python tras la fase de análisis léxico y sintáctico. Cada nodo del árbol representa una construcción elemental del lenguaje: `FunctionDef`, `ClassDef`, `AnnAssign` (anotación de tipos), `Return`, `Import`, etc.

Python incluye en su biblioteca estándar el módulo nativo `ast`, lo que permite inspeccionar y transformar código fuente de forma programática y determinística sin requerir librerías externas.

---

## 3. Implementación de un Podador de Código en Python Nativo

A continuación construimos un transformador que recibe un archivo fuente de `energy-ml` y genera su esqueleto contractual reemplazando los cuerpos internos de funciones por `...` (`Ellipsis`):

```python
import ast
import sys


class ASTContextPruner(ast.NodeTransformer):
    """Transformador que poda cuerpos de funciones preservando contratos y tipos."""

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        self.generic_visit(node)
        # Extraer docstring original si existe
        docstring = ast.get_docstring(node)

        nuevo_cuerpo: list[ast.stmt] = []
        if docstring:
            nuevo_cuerpo.append(ast.Expr(value=ast.Constant(value=docstring)))

        # Reemplazar el resto de la implementación por '...'
        nuevo_cuerpo.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
        node.body = nuevo_cuerpo
        return node

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        self.generic_visit(node)
        docstring = ast.get_docstring(node)
        nuevo_cuerpo: list[ast.stmt] = []
        if docstring:
            nuevo_cuerpo.append(ast.Expr(value=ast.Constant(value=docstring)))
        nuevo_cuerpo.append(ast.Expr(value=ast.Constant(value=Ellipsis)))
        node.body = nuevo_cuerpo
        return node


def podar_archivo_python(codigo_fuente: str) -> str:
    """Convierte código Python en un esqueleto ultracompacto para agentes."""
    arbol = ast.parse(codigo_fuente)
    podador = ASTContextPruner()
    arbol_podado = podador.visit(arbol)
    ast.fix_missing_locations(arbol_podado)
    return ast.unparse(arbol_podado)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            contenido = f.read()
        print(podar_archivo_python(contenido))
```

---

## 4. Cómo Utilizan los Agentes la Poda de Contexto

Las principales herramientas del cuarteto de IA agéntica aplican esta técnica internamente:

1. **Aider (`repomap`):** Antes de iniciar la conversación, analiza el repositorio con `tree-sitter`, extrae identificadores, clases y firmas, y construye un mapa del repositorio en formato de grafo de llamadas que ocupa menos del 5% del contexto.
2. **Antigravity CLI (AGY):** Posee optimizadores de hardware local en CPU para filtrar dependencias y podar firmas antes de interactuar con el modelo maestro, asegurando respuestas hiperfocalizadas.
3. **OpenCode:** Utiliza indexadores de símbolos para responder consultas arquitectónicas sin necesidad de cargar los módulos completos en la ventana del LLM.

---

## 5. Ejercicio Práctico en la Terminal

1. Navega al directorio de `energy-ml`:

```bash
cd ~/proyectos_software/energy-ml
```
2. Ejecuta el podador AST sobre el archivo del servicio de predicción:

```bash
python3 scripts/prune_ast.py src/infrastructure/fastapi/routes/predict.py
```
3. Observa cómo un archivo de 200 líneas se sintetiza en un contrato de 30 líneas que incluye únicamente los tipos de entrada `Pydantic`, decoradores de ruta (`@router.post`) y firmas de retorno.

En la próxima lección veremos cómo exponer la funcionalidad de `energy-ml` hacia los agentes mediante el protocolo estándar **Model Context Protocol (MCP)**.
