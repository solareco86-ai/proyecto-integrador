#!/usr/bin/env python
import argparse
import os
import sys
from typing import Any

import yaml  # type: ignore
from pydantic import ValidationError

# Asegurar que el path del proyecto esté en el PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.application.data_service import DataService
from src.application.dtos import (
    BrandModel,
    CarrerasContainerModel,
    CasoModel,
    ContentModel,
    CourseModel,
    FooterModel,
    LandingContentModel,
    LegalPagesModel,
    SeoModel,
)


def get_default_value_for_type(type_name: str) -> Any:
    """Devuelve un valor por defecto o placeholder según el tipo esperado en el esquema."""
    if "string" in type_name or "str" in type_name:
        return "TODO"
    elif "integer" in type_name or "int" in type_name:
        return 0
    elif "number" in type_name or "float" in type_name:
        return 0.0
    elif "boolean" in type_name or "bool" in type_name:
        return False
    elif "array" in type_name or "list" in type_name:
        return []
    elif "object" in type_name or "dict" in type_name:
        return {}
    return "TODO"


def fix_yaml_file(file_path: str, model_cls: type[Any]) -> bool:
    """
    Intenta arreglar interactivamente un archivo YAML añadiendo campos obligatorios faltantes
    detectados por Pydantic.
    """
    print(f"\n[FIX] Analizando y reparando: {file_path}")

    try:
        with open(file_path, encoding="utf-8") as f:
            raw_data = yaml.safe_load(f) or {}
    except Exception as e:
        print(f"  ❌ Error de lectura de YAML: {e}")
        return False

    fixed = False
    iterations = 0
    max_iterations = 10  # Prevenir loops infinitos

    while iterations < max_iterations:
        try:
            # Validar con Pydantic
            model_cls.model_validate(raw_data)
            break  # Validación exitosa
        except ValidationError as e:
            errors = e.errors()
            missing_fields: list[tuple[tuple[str | int, ...], str]] = []

            for err in errors:
                if err.get("type") == "missing":
                    loc = err.get("loc")
                    if loc:
                        missing_fields.append((loc, err.get("msg", "")))

            if not missing_fields:
                print(f"  ❌ Falló la validación pero no por campos faltantes: {e}")
                return False

            # Intentar resolver los campos faltantes
            for loc, msg in missing_fields:
                # Navegar por el diccionario para insertar la clave
                ptr = raw_data
                for step in loc[:-1]:
                    if isinstance(step, str):
                        if step not in ptr:
                            ptr[step] = {}
                        ptr = ptr[step]
                    elif isinstance(step, int):
                        # Pydantic loc puede tener índices numéricos para listas
                        pass

                last_key = loc[-1]
                if isinstance(last_key, str):
                    schema = model_cls.model_json_schema()
                    # Intento heurístico de obtener el tipo del campo
                    prop_schema = schema.get("properties", {}).get(last_key, {})
                    type_str = prop_schema.get("type", "string")

                    default_val = get_default_value_for_type(type_str)

                    print(f"  🔧 Campo faltante '{'.'.join(map(str, loc))}' detectado.")
                    response = input(f"    ¿Deseas inyectar el placeholder '{default_val}'? (S/n): ").strip().lower()
                    if response in ("", "s", "si", "y", "yes"):
                        ptr[last_key] = default_val
                        fixed = True
                    else:
                        val = input("    Ingresa el valor personalizado: ").strip()
                        ptr[last_key] = val
                        fixed = True

            iterations += 1
        except Exception as e:
            print(f"  ❌ Error inesperado durante el fix: {e}")
            return False

    if fixed:
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                yaml.dump(raw_data, f, allow_unicode=True, sort_keys=False)
            print("  ✅ Archivo guardado y corregido con éxito.")
            return True
        except Exception as e:
            print(f"  ❌ Error al guardar el archivo: {e}")
            return False

    print("  No se requirieron cambios.")
    return True


def run_validation(data_dir: str, fix_mode: bool) -> bool:
    """Ejecuta la auditoría completa de archivos de datos."""
    print("==================================================")
    print(f"🔍 Iniciando auditoría de esquemas YAML en '{data_dir}'")
    print("==================================================")

    # Validar archivos maestros y específicos
    targets: list[tuple[str, type[Any]]] = [
        (os.path.join(data_dir, "config", "brand.yaml"), BrandModel),
        (os.path.join(data_dir, "config", "footer.yaml"), FooterModel),
        (os.path.join(data_dir, "content", "carreras.yaml"), CarrerasContainerModel),
        (os.path.join(data_dir, "content", "home_sections.yaml"), ContentModel),
        (os.path.join(data_dir, "content", "legal.yaml"), LegalPagesModel),
        (os.path.join(data_dir, "seo", "seo.yaml"), SeoModel),
        (os.path.join(data_dir, "seo", "landing_content.yaml"), LandingContentModel),
    ]

    # Agregar cursos
    courses_dir = os.path.join(data_dir, "core", "cursos")
    if os.path.exists(courses_dir):
        for folder in os.listdir(courses_dir):
            c_path = os.path.join(courses_dir, folder, "curso.yaml")
            if os.path.exists(c_path):
                # Pydantic valida CourseModel, pero en curso.yaml el instructor es instructor_id (se hidrata en DataService)
                # Por lo tanto, para validar el YAML directamente antes de hidratar, podemos validar la estructura cruda.
                # Como el instructor es obligatorio en CourseModel, vamos a simular un instructor ficticio si queremos validarlo directo,
                # o cargarlo a través de DataService.
                # Validar usando el DataService es más robusto porque ya integra mappers y adaptadores.
                targets.append((c_path, CourseModel))

    # Agregar casos
    cases_dir = os.path.join(data_dir, "core", "casos")
    if os.path.exists(cases_dir):
        for folder in os.listdir(cases_dir):
            c_path = os.path.join(cases_dir, folder, "caso.yaml")
            if os.path.exists(c_path):
                targets.append((c_path, CasoModel))

    failures = 0
    service = DataService(data_dir=data_dir)

    for path, model_cls in targets:
        if not os.path.exists(path):
            print(f"⚠️  Archivo no encontrado (omitido): {path}")
            continue

        try:
            # Si es un curso, lo cargamos usando el DataService para que resuelva dependencias e instructores
            if model_cls == CourseModel:
                folder_name = os.path.basename(os.path.dirname(path))
                # Intentar cargar a través de DataService
                course = service.get_curso_por_slug(folder_name)
                if not course:
                    # Alternativa: cargar directo el YAML
                    with open(path, encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                    CourseModel.model_validate(data)
            # Si es un caso, cargamos usando DataService
            elif model_cls == CasoModel:
                folder_name = os.path.basename(os.path.dirname(path))
                caso = service.get_caso_por_slug(folder_name)
                if not caso:
                    with open(path, encoding="utf-8") as f:
                        data = yaml.safe_load(f) or {}
                    CasoModel.model_validate(data)
            else:
                with open(path, encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                model_cls.model_validate(data)

            print(f"✅ {os.path.basename(path)}: Estructura y validación OK.")
        except (ValidationError, Exception) as e:
            print(f"❌ {os.path.basename(path)}: Fallo en esquema.")
            print(f"  Detalles del error: {e}")
            failures += 1

            if fix_mode:
                # Caso especial para CourseModel ya que requiere instructor hidratado.
                # Si vamos a arreglar, le pasamos los datos del YAML crudo pero asumiendo un instructor de prueba para pasar la validación
                if model_cls == CourseModel:
                    # Para reparar curso.yaml agregamos temporalmente el sub-esquema del instructor
                    try:
                        with open(path, encoding="utf-8") as f:
                            raw = yaml.safe_load(f) or {}
                        if "instructor" not in raw:
                            raw["instructor"] = {
                                "id": "test",
                                "name": "Test",
                                "role": "Test",
                                "photo": "test.jpg",
                                "bio": "test",
                            }
                        # Validar y corregir
                        CourseModel.model_validate(raw)
                    except ValidationError:
                        # Si sigue fallando por otras claves, procedemos con el reparador
                        pass

                success = fix_yaml_file(path, model_cls)
                if success:
                    failures -= 1

    print("\n==================================================")
    if failures == 0:
        print("🎉 ¡Auditoría exitosa! Todos los esquemas están correctos.")
        print("==================================================")
        return True
    else:
        print(f"❌ Auditoría fallida. Se encontraron {failures} archivos con esquemas inválidos.")
        print("==================================================")
        return False


def main():
    parser = argparse.ArgumentParser(description="Auditor de esquemas e integridad YAML para el CMS de DataMaq.")
    parser.add_argument(
        "--fix", action="store_true", help="Activar el modo interactivo para reparar campos obligatorios faltantes."
    )
    parser.add_argument("--data-dir", default="data", help="Ruta de la carpeta de datos (default: 'data').")

    args = parser.parse_args()

    success = run_validation(args.data_dir, args.fix)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
