"""DTOs de Pydantic para el subdominio de leads y contacto."""

from pydantic import BaseModel, EmailStr, Field


class OptionModel(BaseModel):
    value: str
    label: str


class FieldModel(BaseModel):
    id: str
    label: str
    autocomplete: str | None = None
    type: str | None = "text"  # "text", "textarea", "select"
    options: list[OptionModel] | None = None


class StepModel(BaseModel):
    title: str
    cta: str | None = None
    fields: list[FieldModel]


class AltEmailModel(BaseModel):
    label: str
    title: str
    cta: str | None = None
    email: str


class ContactModel(BaseModel):
    title: str
    subtitle: str
    cta: str
    alt_email: AltEmailModel
    progress_text: str
    privacy_note: str
    error_message: str
    optional_text: str
    steps: list[StepModel]


class ContactSubmitPayload(BaseModel):
    name: str = Field(..., min_length=2, max_length=120)
    firstName: str | None = Field(None, max_length=60)
    lastName: str | None = Field(None, max_length=60)
    email: EmailStr | None = None
    phone: str | None = Field(None, max_length=30)
    company: str | None = Field(None, max_length=120)
    geographicLocation: str | None = Field(None, max_length=200)
    comment: str = Field(..., min_length=1, max_length=3000)
    preferredContactChannel: str | None = "whatsapp"
    pageLocation: str | None = Field(None, max_length=500)
    trafficSource: str | None = Field(None, max_length=500)
    gclid: str | None = Field(None, max_length=255)
    fbclid: str | None = Field(None, max_length=255)
    utmSource: str | None = Field(None, max_length=255)
    utmMedium: str | None = Field(None, max_length=255)
    utmCampaign: str | None = Field(None, max_length=255)
    userAgent: str | None = Field(None, max_length=500)
    createdAt: str | None = None  # Ignorado: el servidor genera el timestamp
    captchaToken: str | None = None
    leadSource: str | None = Field(None, max_length=80)
    website_url_hp: str | None = Field(None, max_length=120)  # Campo Honeypot anti-spam


class WhatsAppClickPayload(BaseModel):
    pageLocation: str | None = Field(None, max_length=500)
    trafficSource: str | None = Field(None, max_length=500)
    element: str | None = Field(None, max_length=120)
    cookieConsent: str | None = Field(None, max_length=50)
    utmSource: str | None = Field(None, max_length=255)
    utmMedium: str | None = Field(None, max_length=255)
    utmCampaign: str | None = Field(None, max_length=255)
    gclid: str | None = Field(None, max_length=255)


class DirectContactPayload(BaseModel):
    action: str = Field(..., max_length=50)  # 'email_click', 'email_copy', 'phone_click', 'phone_copy'
    targetValue: str | None = Field(None, max_length=120)  # e.g. 'info@datamaq.com.ar', '+54 11 5629 7160'
    pageLocation: str | None = Field(None, max_length=500)
    trafficSource: str | None = Field(None, max_length=500)
    element: str | None = Field(None, max_length=120)
    cookieConsent: str | None = Field(None, max_length=50)
    utmSource: str | None = Field(None, max_length=255)
    utmMedium: str | None = Field(None, max_length=255)
    utmCampaign: str | None = Field(None, max_length=255)
    gclid: str | None = Field(None, max_length=255)
