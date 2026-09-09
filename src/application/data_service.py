import os
from typing import Any, cast

import yaml  # type: ignore

from src.application.dtos import (
    CarreraModel,
    CarrerasContainerModel,
    CasoModel,
    CasosContainerModel,
    ContenidoModel,
    CourseModel,
    CursosContainerModel,
    GuiaModel,
    GuiasContainerModel,
    IndustriaModel,
    InstructoresContainerModel,
    InstructorModel,
    LandingCampaignModel,
    LandingCampaignsContainerModel,
    LandingContentModel,
    LessonModel,
    QuizModel,
    TelemetryPlanModel,
)
from src.application.mappers.course_mapper import to_course_model
from src.application.markdown_parser import MarkdownParser
from src.application.pricing_service import PricingService


class DataService:
    def __init__(self, data_dir: str | None = None):
        if not data_dir or (data_dir == "data" and "DATA_DIR" in os.environ):
            self.data_dir = os.getenv("DATA_DIR", "data")
        else:
            self.data_dir = data_dir
        self.pricing_service = PricingService(data_dir=self.data_dir)

        # Deducir rutas según la arquitectura física por Bounded Contexts
        self.brand_path = os.path.join(self.data_dir, "config", "brand.yaml")
        self.footer_path = os.path.join(self.data_dir, "config", "footer.yaml")
        self.redirects_path = os.path.join(self.data_dir, "config", "redirects.yaml")

        self.home_sections_path = os.path.join(self.data_dir, "content", "home_sections.yaml")
        self.legal_path = os.path.join(self.data_dir, "content", "legal.yaml")
        self.carreras_path = os.path.join(self.data_dir, "content", "carreras.yaml")
        self.planes_path = os.path.join(self.data_dir, "content", "planes.yaml")
        self.landings_path = os.path.join(self.data_dir, "content", "landings.yaml")

        self.seo_path = os.path.join(self.data_dir, "seo", "seo.yaml")
        self.landing_content_path = os.path.join(self.data_dir, "seo", "landing_content.yaml")

        self.geography_path = os.path.join(self.data_dir, "meta", "geografia.yaml")
        self.industry_path = os.path.join(self.data_dir, "meta", "industrias.yaml")

        self.instructors_path = os.path.join(self.data_dir, "core", "instructores.yaml")
        self.courses_dir = os.path.join(self.data_dir, "core", "cursos")
        self.cases_dir = os.path.join(self.data_dir, "core", "casos")
        self.guias_dir = os.path.join(self.data_dir, "core", "guias")

        self.markdown_parser = MarkdownParser()

        self._cached_contenido: ContenidoModel | None = None
        self._cached_carreras: list[CarreraModel] | None = None
        self._cached_geografia: dict[str, Any] | None = None
        self._cached_industrias: IndustriaModel | None = None
        self._cached_cursos: CursosContainerModel | None = None
        self._cached_landings: LandingCampaignsContainerModel | None = None
        self._cached_instructores: dict[str, InstructorModel] | None = None
        self._cached_redirects: dict[str, str] | None = None
        self._cached_landing_content: LandingContentModel | None = None
        self._cached_casos: CasosContainerModel | None = None
        self._cached_guias: GuiasContainerModel | None = None
        self._cached_planes: list[TelemetryPlanModel] | None = None

    def get_contenido(self) -> ContenidoModel:
        if self._cached_contenido is None:
            # Leer los archivos separados del CMS
            with open(self.brand_path, encoding="utf-8") as f:
                brand_data: dict[str, Any] = yaml.safe_load(f) or {}

            with open(self.home_sections_path, encoding="utf-8") as f:
                home_sections_data: dict[str, Any] = yaml.safe_load(f) or {}

            with open(self.legal_path, encoding="utf-8") as f:
                legal_data: dict[str, Any] = yaml.safe_load(f) or {}

            with open(self.seo_path, encoding="utf-8") as f:
                seo_data: dict[str, Any] = yaml.safe_load(f) or {}

            with open(self.footer_path, encoding="utf-8") as f:
                footer_data: dict[str, Any] = yaml.safe_load(f) or {}

            # Reconstruir el diccionario compatible con ContenidoModel
            raw_data: dict[str, Any] = {
                "brand": brand_data,
                "content": home_sections_data,
                "seo": seo_data,
                "legal_pages": legal_data,
                "footer": footer_data,
            }

            # --- Generar Footer Dinámico ---
            if "navigation_groups" not in raw_data["footer"]:
                raw_data["footer"]["navigation_groups"] = []

            # 1. Grupo de Navegación (mantener o definir por defecto)
            nav_group: dict[str, Any] | None = None
            for group in raw_data["footer"].get("navigation_groups", []):
                if group.get("title") == "Navegación":
                    nav_group = group
                    break

            if not nav_group:
                nav_group = {
                    "title": "Navegación",
                    "links": [
                        {"label": "Inicio", "href": "/"},
                        {"label": "Casos", "href": "/casos"},
                        {"label": "Cursos", "href": "/cursos"},
                        {"label": "Contacto", "href": "/contact"},
                    ],
                }

            # 2. Grupo de Cobertura dinámica
            geografia_data = self.get_geografia()
            cobertura_links: list[dict[str, str]] = []
            localidades: dict[str, Any] = geografia_data.get("localidades", {})
            for provincia_key, provincia in localidades.items():
                for municipio_key, municipio in provincia.items():
                    for localidad_key, nombre_localidad in municipio.items():
                        cobertura_links.append(
                            {
                                "label": nombre_localidad,
                                "href": f"/{provincia_key}/{municipio_key}/{localidad_key}.html",
                            }
                        )

            cobertura_group: dict[str, Any] = {"title": "Cobertura", "links": cobertura_links}

            # 3. Grupo de Industrias dinámica
            industrias_data = self.get_industrias()
            industrias_links: list[dict[str, str]] = []
            for industria_key, nombre_industria in industrias_data.industrias.items():
                label = nombre_industria.replace("Industria ", "")
                industrias_links.append({"label": label, "href": f"/industria/{industria_key}.html"})

            industrias_group: dict[str, Any] = {"title": "Industrias", "links": industrias_links}

            raw_data["footer"]["navigation_groups"] = [nav_group, cobertura_group, industrias_group]

            self._cached_contenido = ContenidoModel.model_validate(raw_data)
        return self._cached_contenido

    def get_geografia(self) -> dict[str, Any]:
        if self._cached_geografia is None:
            with open(self.geography_path, encoding="utf-8") as f:
                loaded: dict[str, Any] = yaml.safe_load(f) or {}
                self._cached_geografia = loaded
        return self._cached_geografia or {}

    def get_industrias(self) -> IndustriaModel:
        if self._cached_industrias is None:
            with open(self.industry_path, encoding="utf-8") as f:
                raw_data: dict[str, Any] = yaml.safe_load(f) or {}
            self._cached_industrias = IndustriaModel(**raw_data)
        return self._cached_industrias

    def get_cursos_container(self) -> CursosContainerModel:
        if self._cached_cursos is None:
            cursos_list: list[CourseModel] = []
            instructores = self.get_instructores_dict()

            if os.path.exists(self.courses_dir):
                for folder_name in sorted(os.listdir(self.courses_dir)):
                    curso_folder_path = os.path.join(self.courses_dir, folder_name)
                    if os.path.isdir(curso_folder_path):
                        curso_yaml_path = os.path.join(curso_folder_path, "curso.yaml")
                        if os.path.exists(curso_yaml_path):
                            with open(curso_yaml_path, encoding="utf-8") as f:
                                curso_data: dict[str, Any] = yaml.safe_load(f) or {}

                                # Cargar lecciones markdown locales al curso
                                if "sections" in curso_data:
                                    for seccion in curso_data["sections"]:
                                        if "chapters" in seccion:
                                            for chapter in seccion["chapters"]:
                                                if "items" in chapter:
                                                    for item in chapter["items"]:
                                                        if item.get("type") == "lesson" and item.get("content_file"):
                                                            file_path = os.path.join(
                                                                curso_folder_path, "lecciones", item["content_file"]
                                                            )
                                                            if os.path.exists(file_path):
                                                                with open(file_path, encoding="utf-8") as cf:
                                                                    raw_markdown = cf.read()
                                                                    item["content"] = self.markdown_parser.to_html(
                                                                        raw_markdown
                                                                    )
                                                            else:
                                                                item["content"] = (
                                                                    f"<p class='error'>Error: No se encontró el archivo de contenido en {file_path}</p>"
                                                                )

                                # Delegar la hidratación/resolución del instructor al mapper
                                course_model = to_course_model(curso_data, instructores)
                                cursos_list.append(course_model)

            self._cached_cursos = CursosContainerModel(cursos=cursos_list)
        return self._cached_cursos

    def get_instructores_dict(self) -> dict[str, InstructorModel]:
        if self._cached_instructores is None:
            with open(self.instructors_path, encoding="utf-8") as f:
                raw_data: dict[str, Any] = yaml.safe_load(f) or {"instructores": []}

            container = InstructoresContainerModel(**raw_data)
            self._cached_instructores = {inst.id: inst for inst in container.instructores}
        return self._cached_instructores

    def get_cursos(self) -> list[CourseModel]:
        return self.get_cursos_container().cursos

    def get_cursos_publicos(self) -> list[CourseModel]:
        return [c for c in self.get_cursos() if not c.academic_only]

    def get_curso_por_slug(self, slug: str) -> CourseModel | None:
        for curso in self.get_cursos():
            if curso.slug == slug:
                return curso
        return None

    def get_leccion(self, curso_slug: str, leccion_slug: str) -> tuple[CourseModel, LessonModel | QuizModel] | None:
        curso = self.get_curso_por_slug(curso_slug)
        if not curso:
            return None
        for seccion in curso.sections:
            for chapter in seccion.chapters:
                for item in chapter.items:
                    if item.slug == leccion_slug:
                        return curso, item
        return None

    def get_instructor_por_id(self, instructor_id: str) -> InstructorModel | None:
        return self.get_instructores_dict().get(instructor_id)

    def get_redirects(self) -> dict[str, str]:
        if self._cached_redirects is None:
            self._cached_redirects = {}
            if self.redirects_path and os.path.exists(self.redirects_path):
                with open(self.redirects_path, encoding="utf-8") as f:
                    raw_data: dict[str, Any] = yaml.safe_load(f) or {}
                redirects_raw = cast(dict[str, str], raw_data.get("redirects", {}))
                if isinstance(redirects_raw, dict):
                    for k, v in redirects_raw.items():
                        self._cached_redirects[str(k)] = str(v)
        return self._cached_redirects

    def get_landing_content(self) -> LandingContentModel:
        if self._cached_landing_content is None:
            self._cached_landing_content = LandingContentModel()
            if self.landing_content_path and os.path.exists(self.landing_content_path):
                with open(self.landing_content_path, encoding="utf-8") as f:
                    raw_data: dict[str, Any] = yaml.safe_load(f) or {}
                self._cached_landing_content = LandingContentModel.model_validate(raw_data)
        return self._cached_landing_content

    def get_casos_container(self) -> CasosContainerModel:
        if self._cached_casos is None:
            casos_list: list[CasoModel] = []

            if os.path.exists(self.cases_dir):
                for folder_name in sorted(os.listdir(self.cases_dir)):
                    caso_folder_path = os.path.join(self.cases_dir, folder_name)
                    if os.path.isdir(caso_folder_path):
                        caso_yaml_path = os.path.join(caso_folder_path, "caso.yaml")
                        if os.path.exists(caso_yaml_path):
                            with open(caso_yaml_path, encoding="utf-8") as f:
                                caso_data: dict[str, Any] = yaml.safe_load(f) or {}
                            if caso_data.get("content"):
                                caso_data["content"] = self.markdown_parser.to_html(caso_data["content"])
                            casos_list.append(CasoModel.model_validate(caso_data))

            self._cached_casos = CasosContainerModel(casos=casos_list)
        return self._cached_casos

    def get_casos(self) -> list[CasoModel]:
        return self.get_casos_container().casos

    def get_caso_por_slug(self, slug: str) -> CasoModel | None:
        for caso in self.get_casos():
            if caso.slug == slug:
                return caso
        return None

    def get_guias_container(self) -> GuiasContainerModel:
        if self._cached_guias is None:
            guias_list: list[GuiaModel] = []

            if os.path.exists(self.guias_dir):
                for folder_name in sorted(os.listdir(self.guias_dir)):
                    guia_folder_path = os.path.join(self.guias_dir, folder_name)
                    if os.path.isdir(guia_folder_path):
                        guia_yaml_path = os.path.join(guia_folder_path, "guia.yaml")
                        if os.path.exists(guia_yaml_path):
                            with open(guia_yaml_path, encoding="utf-8") as f:
                                guia_data: dict[str, Any] = yaml.safe_load(f) or {}
                            if guia_data.get("content"):
                                guia_data["content"] = self.markdown_parser.to_html(guia_data["content"])
                            guias_list.append(GuiaModel.model_validate(guia_data))

            self._cached_guias = GuiasContainerModel(guias=guias_list)
        return self._cached_guias

    def get_guias(self) -> list[GuiaModel]:
        return self.get_guias_container().guias

    def get_guia_por_slug(self, slug: str) -> GuiaModel | None:
        for guia in self.get_guias():
            if guia.slug == slug:
                return guia
        return None

    def get_pricing_service(self) -> PricingService:
        return self.pricing_service

    def get_planes(self) -> list[TelemetryPlanModel]:
        if self._cached_planes is None:
            with open(self.planes_path, encoding="utf-8") as f:
                raw_data: dict[str, Any] = yaml.safe_load(f) or {}
            planes: list[TelemetryPlanModel] = []
            for plan in raw_data.get("planes", []):
                plan_model = TelemetryPlanModel.model_validate(plan)
                plan_model.price = self.pricing_service.get_plan_display_price(
                    plan_model.id, default_price=plan_model.price
                )
                planes.append(plan_model)
            self._cached_planes = planes
        return self._cached_planes

    def get_landing_campaigns(self) -> LandingCampaignsContainerModel:
        if self._cached_landings is None:
            if os.path.exists(self.landings_path):
                with open(self.landings_path, encoding="utf-8") as f:
                    raw_data: dict[str, Any] = yaml.safe_load(f) or {}
                self._cached_landings = LandingCampaignsContainerModel.model_validate(raw_data)
            else:
                raise FileNotFoundError(f"No se encontró el archivo de landings en {self.landings_path}")
        return self._cached_landings

    def get_landing_campaign(self, slug: str) -> LandingCampaignModel | None:
        campaigns = self.get_landing_campaigns()
        if slug == "calidad-energia":
            return campaigns.calidad_energia
        elif slug == "telemetria-industrial":
            return campaigns.telemetria_industrial
        return None

    def get_carreras(self) -> list[CarreraModel]:
        if self._cached_carreras is None:
            if not os.path.exists(self.carreras_path):
                return []
            with open(self.carreras_path, encoding="utf-8") as f:
                raw_data: dict[str, Any] = yaml.safe_load(f) or {}
            container = CarrerasContainerModel.model_validate(raw_data)
            self._cached_carreras = container.carreras
        return self._cached_carreras

    def get_carrera_by_slug(self, slug: str) -> CarreraModel | None:
        for carrera in self.get_carreras():
            if carrera.slug == slug:
                return carrera
        return None

