"""DTOs de Pydantic para el subdominio de contenido general, servicios, planes y layout."""

from pydantic import BaseModel, Field

from src.application.dtos.lead_dto import ContactModel
from src.application.dtos.seo_dto import SeoModel


class PhotoModel(BaseModel):
    src: str
    alt: str
    width: int | None = None
    height: int | None = None


class TechnicianModel(BaseModel):
    name: str
    role: str
    photo: PhotoModel
    linkedin_url: str | None = None
    bio: str | None = None


class CtaModel(BaseModel):
    label: str
    href: str


class BenefitModel(BaseModel):
    title: str
    cta: str | None = None
    text: str


class NavbarLinkModel(BaseModel):
    label: str
    href: str


class FaqItemModel(BaseModel):
    question: str
    answer: str


class BrandModel(BaseModel):
    brandName: str
    brandAriaLabel: str
    baseOperativa: str
    contactEmail: str
    whatsappUrl: str | None = None
    technician: TechnicianModel
    footerDescription: str
    address: dict[str, str] | None = None
    geo: dict[str, float] | None = None
    openingHours: str | None = None
    sameAs: list[str] | None = None


class HeroModel(BaseModel):
    badge: str
    title: str
    subtitle: str
    responseNote: str
    primaryCta: CtaModel
    secondaryCta: CtaModel
    benefits: list[BenefitModel]
    image: PhotoModel


class ServiceCardModel(BaseModel):
    id: str
    title: str
    cta: str | None = None
    description: str
    problem: str
    key_points: list[str]
    proof: str | None = None
    caso_slug: str | None = None
    modality: str | None = "both"


class ServicesModel(BaseModel):
    eyebrow: str = "Servicios"
    title: str
    description: str | None = None
    cta: str | None = None
    cards: list[ServiceCardModel]


class NavbarModel(BaseModel):
    links: list[NavbarLinkModel]


class FaqModel(BaseModel):
    eyebrow: str = "Ayuda"
    title: str = "Preguntas frecuentes"
    questions: list[FaqItemModel]


class AboutModel(BaseModel):
    title: str
    cta: str | None = None
    paragraphs: list[str]
    image: PhotoModel


class ProfileModel(BaseModel):
    eyebrow: str | None = None
    title: str | None = None
    description: str | None = None
    detail_label: str | None = None
    detail_copy: str | None = None
    bullets: list[str]
    cta_label: str | None = None
    cta_href: str | None = None


class ProofStripItemModel(BaseModel):
    label: str | None = None
    text: str


class ProofStripModel(BaseModel):
    items: list[ProofStripItemModel]


class ProcessStepModel(BaseModel):
    title: str
    text: str


class ProcessModel(BaseModel):
    eyebrow: str
    title: str
    description: str | None = None
    steps: list[ProcessStepModel]


class LegalModel(BaseModel):
    text: str


class TelemetryPlanModel(BaseModel):
    id: str
    name: str
    badge: str | None = None
    price: str
    tagline: str
    featured: bool = False
    features: list[str]
    cta_label: str
    cta_whatsapp_text: str


class PlanesModel(BaseModel):
    eyebrow: str = "Planes de Telemetría"
    title: str
    subtitle: str
    live_demo_label: str = "Ver demo en vivo"
    live_demo_href: str = "https://app.datamaq.com.ar"
    plans: list[TelemetryPlanModel]


class PricingModel(BaseModel):
    eyebrow: str = "Planes y Precios"
    title: str
    subtitle: str
    seo_title: str
    seo_description: str
    live_demo_label: str = "Ver demo en vivo"
    live_demo_href: str = "https://app.datamaq.com.ar"


class CookieBannerModel(BaseModel):
    title: str
    text: str
    accept_label: str
    reject_label: str
    more_info_label: str
    more_info_link: str


class LegalSectionModel(BaseModel):
    title: str
    paragraphs: list[str]


class LegalPageModel(BaseModel):
    title: str
    last_updated: str
    introduction: str
    sections: list[LegalSectionModel]


class LegalPagesModel(BaseModel):
    terms: LegalPageModel


class AssistanceModeModel(BaseModel):
    label: str
    description: str
    icon: str


class CoursesHeroModel(BaseModel):
    badge: str
    title: str
    subtitle: str
    assistance_cta_label: str
    assistance_cta_href: str


class CasesHeroModel(BaseModel):
    badge: str
    title: str
    subtitle: str
    detail_sidebar_title: str = "¿Tenés un caso similar?"
    detail_sidebar_text: str = ""
    detail_sidebar_cta: str = "Contactar"


class GuiasHeroModel(BaseModel):
    badge: str = "Base de Conocimiento y Guías Técnicas"
    title: str = "Guías de Ingeniería de Datos y Eficiencia Energética"
    subtitle: str = "Artículos técnicos, marcos regulatorios y procedimientos prácticos de telemetría IoT y optimización energética."
    detail_sidebar_title: str = "¿Necesitás aplicar esto en tu planta?"
    detail_sidebar_text: str = (
        "Coordinamos un relevamiento técnico en campo para diagnosticar tu tablero y medir tu consumo real."
    )
    detail_sidebar_cta: str = "Consultar por WhatsApp"


class ContentModel(BaseModel):
    hero: HeroModel
    proof_strip: ProofStripModel
    services: ServicesModel
    planes: PlanesModel | None = None
    pricing: PricingModel | None = None
    navbar: NavbarModel
    faq: FaqModel
    about: AboutModel
    profile: ProfileModel
    legal: LegalModel
    contact: ContactModel
    cookie_banner: CookieBannerModel
    assistance_modes: dict[str, AssistanceModeModel]
    courses: CoursesHeroModel
    cases: CasesHeroModel
    guias: GuiasHeroModel | None = None
    process: ProcessModel


class FooterLinkModel(BaseModel):
    label: str
    href: str


class FooterGroupModel(BaseModel):
    title: str
    links: list[FooterLinkModel]


class FooterModel(BaseModel):
    navigation_groups: list[FooterGroupModel]
    cta_title: str
    cta_label: str
    whatsapp_text: str | None = None
    terms_label: str
    terms_href: str
    copyright_suffix: str


class ContenidoModel(BaseModel):
    brand: BrandModel
    content: ContentModel
    seo: SeoModel
    legal_pages: LegalPagesModel
    footer: FooterModel


class IndustriaModel(BaseModel):
    industrias: dict[str, str]


class CasoModel(BaseModel):
    slug: str
    title: str = Field(..., min_length=1)
    industry: str
    location: str
    client: str | None = None
    summary: str
    problem: str
    solution: str
    results: list[str]
    published_at: str
    og_image: str | None = None
    content: str | None = None


class CasosContainerModel(BaseModel):
    casos: list[CasoModel]


class GuiaModel(BaseModel):
    slug: str
    title: str = Field(..., min_length=1)
    category: str
    reading_time: str
    summary: str
    problem: str
    solution: str
    key_takeaways: list[str] = Field(default_factory=list)
    published_at: str
    og_image: str | None = None
    content: str | None = None


class GuiasContainerModel(BaseModel):
    guias: list[GuiaModel]


class LandingBenefitModel(BaseModel):
    title: str
    text: str


class LandingCalculatorModel(BaseModel):
    title: str
    subtitle: str
    default_kw: float = 50.0
    default_cos_phi: float = 0.78
    target_cos_phi: float = 0.96
    help_text: str | None = None


class LandingFormModel(BaseModel):
    title: str
    subtitle: str
    cta_button: str = "Solicitar Diagnóstico Express"


class LandingProofItemModel(BaseModel):
    title: str
    description: str


class LandingCampaignModel(BaseModel):
    slug: str
    badge: str
    hero_title: str
    hero_subtitle: str
    primary_cta_label: str
    primary_cta_whatsapp_text: str
    secondary_cta_label: str | None = None
    secondary_cta_href: str | None = None
    benefits: list[LandingBenefitModel]
    calculator: LandingCalculatorModel | None = None
    form: LandingFormModel | None = None
    proof_items: list[LandingProofItemModel] = Field(default_factory=list[LandingProofItemModel])
    faqs: list[FaqItemModel] = Field(default_factory=list[FaqItemModel])


class LandingCampaignsContainerModel(BaseModel):
    calidad_energia: LandingCampaignModel
    telemetria_industrial: LandingCampaignModel


class CarreraModel(BaseModel):
    id: str
    slug: str
    title: str
    titulo_otorgado: str
    duracion: str
    modalidad: str
    turno: str
    resolucion: str | None = None
    badge: str | None = None
    icon: str | None = None
    description_short: str = ""
    description_long: str = ""
    perfil_egresado: str = ""
    materias_destacadas: list[str] = Field(default_factory=list[str])
    salida_laboral: list[str] = Field(default_factory=list[str])


class CarrerasContainerModel(BaseModel):
    carreras: list[CarreraModel]

