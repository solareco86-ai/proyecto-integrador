import os

from src.application.data_service import DataService


def test_yaml_files_integrity():
    """
    Test unitario que valida que todos los archivos YAML en la carpeta `data/`
    se carguen y validen correctamente contra sus respectivos modelos Pydantic
    sin levantar el servidor FastAPI.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, "data")
    service = DataService(data_dir=data_dir)

    # 1. Validar Contenido general
    contenido = service.get_contenido()
    assert contenido is not None
    assert contenido.brand.brandName == "ISFT N° 199"

    # 2. Validar Geografía
    geografia = service.get_geografia()
    assert "localidades" in geografia

    # 3. Validar Industrias
    industrias = service.get_industrias()
    assert len(industrias.industrias) > 0

    # 4. Validar Cursos e Instructores
    cursos = service.get_cursos()
    assert len(cursos) > 0
    for curso in cursos:
        assert curso.slug is not None
        assert len(curso.title) > 0

    instructores = service.get_instructores_dict()
    assert len(instructores) > 0

    # 5. Validar Casos de estudio
    casos = service.get_casos()
    assert len(casos) > 0
    for caso in casos:
        assert caso.slug is not None

    # 6. Validar Redirects
    redirects = service.get_redirects()
    assert isinstance(redirects, dict)

    # 7. Validar Landing Content
    landing_content = service.get_landing_content()
    assert landing_content is not None
