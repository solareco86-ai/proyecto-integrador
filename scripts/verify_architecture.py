#!/usr/bin/env python3
"""verify_architecture.py — Validador AST de Arquitectura Limpia y Reglas Hexagonales.

Verifica estáticamente mediante el Árbol de Sintaxis Abstracta (AST) que todas las dependencias
entre módulos de `src/` respeten la regla de dependencia de Clean Architecture y DDD:

  1. Domain: Núcleo puro (stdlib + Pydantic). No depende de Application, Adapters ni Infrastructure.
  2. Application: Casos de uso y servicios (stdlib + Pydantic + Domain). No depende de Adapters ni Infrastructure.
  3. Adapters: Presenters y formateadores (stdlib + Pydantic + Domain + Application). No depende de Infrastructure ni FastAPI.
  4. Infrastructure: Detalle externo. Rutas HTTP (routes/) son controladores delgados y no deben importar SQLAlchemy directamente.

Uso:
    python3 scripts/verify_architecture.py
"""

import ast
import os
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(ROOT_DIR, "src")


def get_all_imports(file_path: str) -> list[str]:
    """Extrae todos los módulos importados en un archivo Python mediante AST."""
    with open(file_path, encoding="utf-8") as f:
        try:
            tree = ast.parse(f.read(), filename=file_path)
        except Exception as e:
            print(f"[ERROR] No se pudo parsear {file_path}: {e}")
            return []

    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name:
                    imports.append(str(alias.name))
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(str(node.module))
    return imports


def verify_architecture() -> list[str]:
    """Verifica todas las reglas de arquitectura y retorna la lista de errores encontrados."""
    errors: list[str] = []

    if not os.path.exists(SRC_DIR):
        errors.append(f"[ERROR] No se encontró el directorio {SRC_DIR}")
        return errors

    for root, _, files in os.walk(SRC_DIR):
        for file in files:
            if not file.endswith(".py"):
                continue

            full_path = os.path.join(root, file)
            rel_path = os.path.relpath(full_path, ROOT_DIR)
            imports = get_all_imports(full_path)

            # 1. Regla de Dominio: Solo stdlib pura (dataclasses, typing, abc). Prohibido pydantic y capas superiores.
            if "src/domain" in rel_path:
                forbidden = (
                    "pydantic",
                    "pydantic_core",
                    "fastapi",
                    "sqlalchemy",
                    "starlette",
                    "httpx",
                    "requests",
                    "pymysql",
                    "src.application",
                    "src.adapters",
                    "src.infrastructure",
                )
                for imp in imports:
                    if any(imp.startswith(f) for f in forbidden):
                        errors.append(f"[DOMINIO VIOLADO] {rel_path} importa módulo prohibido '{imp}'")

            # 2. Regla de Aplicación: No depende de Adapters ni Infrastructure.
            elif "src/application" in rel_path:
                forbidden = (
                    "fastapi",
                    "sqlalchemy",
                    "starlette",
                    "pymysql",
                    "src.adapters",
                    "src.infrastructure",
                )
                for imp in imports:
                    if any(imp.startswith(f) for f in forbidden):
                        errors.append(f"[APLICACIÓN VIOLADA] {rel_path} importa módulo prohibido '{imp}'")

            # 3. Regla de Adaptadores: No depende de Infrastructure ni frameworks web.
            elif "src/adapters" in rel_path:
                forbidden = ("fastapi", "starlette", "src.infrastructure")
                for imp in imports:
                    if any(imp.startswith(f) for f in forbidden):
                        errors.append(f"[ADAPTADORES VIOLADO] {rel_path} importa módulo prohibido '{imp}'")

            # 4. Regla de Rutas (Thin Controllers): No acceden directamente a SQLAlchemy/DB.
            elif "src/infrastructure/fastapi/routes" in rel_path:
                forbidden_routes = ("sqlalchemy",)
                for imp in imports:
                    if any(imp.startswith(f) for f in forbidden_routes):
                        errors.append(
                            f"[CONTROLADOR NO DELGADO] {rel_path} importa '{imp}' directamente (debe delegar en Application)"
                        )

    return errors


def main():
    errors = verify_architecture()
    if errors:
        print("\n".join(errors))
        print(f"\n❌ [FAIL] Se encontraron {len(errors)} violaciones de arquitectura en src/.")
        sys.exit(1)
    else:
        print("✅ [PASS] 100% de las reglas de Clean Architecture, Hexagonal y DDD fueron respetadas.")
        sys.exit(0)


if __name__ == "__main__":
    main()
