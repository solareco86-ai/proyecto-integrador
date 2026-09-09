from typing import Any

from src.application.dtos import CourseModel, InstructorModel


def to_course_model(curso_data: dict[str, Any], instructores: dict[str, InstructorModel]) -> CourseModel:
    """
    Mapea un diccionario crudo de datos de curso a un modelo de dominio CourseModel,
    resolviendo la relación con el instructor correspondiente.
    """
    data = dict(curso_data)
    instructor_id = data.get("instructor_id")

    if instructor_id in instructores:
        data["instructor"] = instructores[instructor_id].model_dump()
    else:
        # Fallback seguro
        data["instructor"] = {
            "id": "unknown",
            "name": "Cátedra ISFT N° 199",
            "role": "Cuerpo Docente",
            "photo": "/static/media/logo-isft199.webp",
            "bio": "Cátedra docente del ISFT N° 199",
        }

    return CourseModel.model_validate(data)
