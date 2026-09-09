"""DTOs de Pydantic para el subdominio de SEO y contenido geolocalizado."""

from pydantic import BaseModel, Field


class SeoModel(BaseModel):
    title: str
    cta: str | None = None
    description: str
    canonical_url: str
    site_name: str
    og_image: str


class LandingFaqItemModel(BaseModel):
    """Equivalente a FaqItemModel, replicado acá porque content_dto ya importa
    de este módulo y la dirección inversa sería un import circular."""

    question: str
    answer: str


class LandingLinkModel(BaseModel):
    """Enlace interno curado (guía o caso) con anchor text propio de la página."""

    label: str
    url: str


class LandingContentItemModel(BaseModel):
    title: str | None = None
    paragraphs: list[str] = Field(default_factory=list)
    bullets: list[str] = Field(default_factory=list)
    links: list[LandingLinkModel] = Field(default_factory=list[LandingLinkModel])
    # FAQ propia de la localidad o industria. Si viene vacía, la página cae en
    # el FAQ genérico de home_sections.yaml.
    faq: list[LandingFaqItemModel] = Field(default_factory=list[LandingFaqItemModel])


class LandingContentModel(BaseModel):
    industrias: dict[str, LandingContentItemModel] = Field(default_factory=dict)
    localidades: dict[str, dict[str, dict[str, LandingContentItemModel]]] = Field(default_factory=dict)
