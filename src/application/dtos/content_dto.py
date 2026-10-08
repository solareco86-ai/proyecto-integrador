"""DTOs de Pydantic para el subdominio de contenido general, servicios, planes y layout."""

from pydantic import BaseModel, Field

from src.application.dtos.lead_dto import ContactModel


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


class RequisitoIngresoModel(BaseModel):
    """Un ítem de la documentación exigida para el legajo de ingreso."""

    text: str


class PasoIngresoModel(BaseModel):
    """Un paso del circuito administrativo de ingreso."""

    title: str
    text: str


class CierreInscripcionModel(BaseModel):
    """Plazo de cierre de la preinscripción.

    Opcional a propósito: mientras Secretaría no comunique una fecha oficial, el
    bloque de admisión se renderiza sin cuenta regresiva (`AGENTS.md`, 7.5).
    """

    fecha_iso: str
    fecha_texto: str


class AdmisionModel(BaseModel):
    """Bloque de estado de admisión que encabeza la portada."""

    titular: str
    bajada: str
    estado: str | None = None
    cierre: CierreInscripcionModel | None = None
    requisitos_titulo: str
    requisitos: list[RequisitoIngresoModel]
    cifras: list[BenefitModel]
    pasos_eyebrow: str
    pasos: list[PasoIngresoModel]
    nota: list[str] = Field(default_factory=list[str])


class SedeModel(BaseModel):
    """Una sede donde el instituto dicta clases."""

    nombre: str
    direccion: list[str]


class CampusEstudianteModel(BaseModel):
    nombre: str
    iniciales: str
    legajo: str
    carrera: str
    anio: str
    comision: str
    turno: str


class CampusEnlaceModel(BaseModel):
    label: str
    actual: bool = False
    aviso: str | None = None


class CampusSeccionModel(BaseModel):
    titulo: str
    enlaces: list[CampusEnlaceModel]


class CampusVencimientoModel(BaseModel):
    dias: int
    titulo: str
    detalle: str
    accion: str
    urgente: bool = False


class CampusMateriaModel(BaseModel):
    nombre: str
    docente: str
    asistencia: int
    parcial_1: str
    parcial_2: str
    condicion: str
    estado: str


class CampusFinalModel(BaseModel):
    materia: str
    mesa: str
    fecha: str
    estado: str
    estado_clase: str = ""
    accion: str = ""
    accion_clase: str = ""


class CampusTramiteModel(BaseModel):
    estado: str
    estado_clase: str
    titulo: str
    detalle: str


class CampusItemResumenModel(BaseModel):
    etiqueta: str
    valor: str


class CampusComunicadoModel(BaseModel):
    fecha: str
    titulo: str


class CampusMuestraModel(BaseModel):
    """Datos de muestra del campus virtual.

    El módulo todavía no existe: no hay base de estudiantes, notas ni
    asistencias. Este modelo alimenta la pantalla de estructura para poder
    revisar el diseño y el flujo antes de construirlo.
    """

    estudiante: CampusEstudianteModel
    ciclo: str
    secciones: list[CampusSeccionModel]
    vencimientos: list[CampusVencimientoModel]
    materias: list[CampusMateriaModel]
    nota_materias: str
    finales: list[CampusFinalModel]
    tramites: list[CampusTramiteModel]
    resumen: list[CampusItemResumenModel]
    comunicados: list[CampusComunicadoModel]


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


class ErrorLinkModel(BaseModel):
    label: str
    href: str
    icon: str


class Error404Model(BaseModel):
    description: str
    links_title: str
    links: list[ErrorLinkModel]


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
    error_404: Error404Model
    assistance_modes: dict[str, AssistanceModeModel]
    courses: CoursesHeroModel
    cases: CasesHeroModel
    guias: GuiasHeroModel | None = None
    process: ProcessModel
    admision: AdmisionModel | None = None
    sedes: list[SedeModel] = Field(default_factory=list[SedeModel])


class SeoModel(BaseModel):
    title: str
    cta: str | None = None
    description: str
    canonical_url: str
    site_name: str
    og_image: str


class FooterModel(BaseModel):
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

