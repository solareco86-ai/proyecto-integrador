/**
 * @fileoverview Definiciones centrales de tipos (JSDoc Type Contracts) para DataMaq.
 * Sincronizados con los DTOs de dominio/aplicación en Python (Clean Architecture).
 */

/**
 * @typedef {Object} WindowAppConfig
 * @property {string} [apiUrl] - URL base para la API.
 * @property {string} [contactApiUrl] - Endpoint para el envío de formularios de contacto.
 * @property {string} [gaId] - ID de medición de Google Analytics 4 (G-XXXXXXXXXX).
 * @property {string} [googleAdsId] - ID de conversión de Google Ads (AW-XXXXXXXXXX).
 * @property {string} [googleAdsConversionId] - Etiqueta de conversión para leads de Google Ads.
 * @property {string} [googleAdsWhatsappConversionId] - Etiqueta de conversión para clics de WhatsApp.
 * @property {string} [clarityId] - ID de proyecto de Microsoft Clarity.
 * @property {boolean} [debug] - Habilita logging verboso (solo desarrollo).
 */

/**
 * @typedef {Object} AppConfig
 * @property {string} apiUrl - URL del endpoint de recepción de formularios de contacto.
 */

/**
 * @typedef {Object} ContactSubmitPayload
 * @description DTO de envío de prospectos/leads comerciales hacia el backend (POST /api/v1/leads).
 * Espejo del DTO Python `ContactSubmitPayload` en `src/application/dtos/lead_dto.py`.
 * @property {string} name - Nombre completo o de fantasía del contacto (2-120 chars).
 * @property {string | null} [firstName] - Nombre de pila.
 * @property {string | null} [lastName] - Apellido.
 * @property {string | null} [email] - Correo electrónico de contacto corporativo.
 * @property {string | null} [phone] - Teléfono o número de WhatsApp con prefijo.
 * @property {string | null} [company] - Razón social o nombre de la empresa/planta.
 * @property {string | null} [geographicLocation] - Localidad, parque industrial o zona (ej. Garín, Pilar, AMBA).
 * @property {string} comment - Detalle técnico de la necesidad o consulta comercial.
 * @property {string | null} [preferredContactChannel] - Canal preferido ('whatsapp', 'email', 'phone').
 * @property {string | null} [pageLocation] - URL completa donde se originó la conversión.
 * @property {string | null} [trafficSource] - Etiqueta calculada de atribución first-touch.
 * @property {string | null} [gclid] - Identificador de clic de Google Ads.
 * @property {string | null} [fbclid] - Identificador de clic de Meta / Facebook.
 * @property {string | null} [utmSource] - Fuente de campaña (ej. google, linkedin, newsletter).
 * @property {string | null} [utmMedium] - Medio de campaña (ej. cpc, social, referral).
 * @property {string | null} [utmCampaign] - Nombre de la campaña SEM o contenido.
 * @property {string | null} [userAgent] - User Agent del navegador cliente.
 * @property {string | null} [createdAt] - Marca de tiempo ISO generada en cliente.
 * @property {string | null} [captchaToken] - Token de verificación antispam si aplicase.
 * @property {string | null} [leadSource] - Origen del lead ('formulario_contacto', 'whatsapp_click', etc.).
 * @property {string | null} [website_url_hp] - Campo señuelo Honeypot para detección de bots antispam.
 */

/**
 * @typedef {Object} WhatsAppClickPayload
 * @description DTO para notificación de eventos de clic en enlaces de WhatsApp a Telegram / Backend.
 * @property {string | null} [pageLocation] - URL actual del usuario al hacer clic.
 * @property {string | null} [trafficSource] - Fuente de tráfico calculada (atribución).
 * @property {string | null} [element] - Elemento o botón específico presionado (FAB, Hero, etc.).
 * @property {string | null} [cookieConsent] - Estado de consentimiento de cookies ('accepted', 'rejected', 'pending').
 * @property {string | null} [utmSource] - Fuente UTM de campaña.
 * @property {string | null} [utmMedium] - Medio UTM de campaña.
 * @property {string | null} [utmCampaign] - Nombre UTM de la campaña.
 * @property {string | null} [gclid] - ID de clic de Google Ads.
 */

/**
 * @typedef {'email_click' | 'email_copy' | 'phone_click' | 'phone_copy'} DirectContactAction
 */

/**
 * @typedef {Object} DirectContactPayload
 * @description DTO para notificación de interacciones directas con email/teléfono hacia el backend.
 * Espejo del DTO Python `DirectContactPayload` en `src/application/dtos/lead_dto.py`.
 * @property {DirectContactAction} action - Tipo de interacción efectuada.
 * @property {string | null} [targetValue] - Valor con el que se interactuó (ej. 'ifst199alumnos@gmail.com', '+54 11 5629 7160').
 * @property {string | null} [pageLocation] - URL actual del usuario al interactuar.
 * @property {string | null} [trafficSource] - Fuente de tráfico calculada (atribución first-touch).
 * @property {string | null} [element] - Elemento del DOM o contexto (Navbar, Footer, Contact, etc.).
 * @property {string | null} [cookieConsent] - Estado de consentimiento de cookies.
 * @property {string | null} [utmSource] - Fuente UTM de campaña.
 * @property {string | null} [utmMedium] - Medio UTM de campaña.
 * @property {string | null} [utmCampaign] - Nombre UTM de la campaña.
 * @property {string | null} [gclid] - ID de clic de Google Ads.
 */

/**
 * @typedef {Object} AttributionRecord
 * @property {string} source - Etiqueta descriptiva calculada de atribución.
 * @property {number} timestamp - Timestamp Unix del primer contacto (First-touch).
 * @property {string} [landingPage] - Página de primer acceso.
 * @property {string | null} [utmCampaign] - Campaña publicitaria.
 * @property {string | null} [utmSource] - Fuente publicitaria.
 * @property {string | null} [utmMedium] - Medio publicitario.
 * @property {string | null} [gclid] - ID de clic de Google Ads.
 */

/**
 * @typedef {Object} CampaignData
 * @description Estructura de persistencia de sesión para campañas publicitarias (SEM / Paid Social).
 * @property {string | null} utmCampaign - Nombre o slug de la campaña.
 * @property {string | null} utmSource - Plataforma de origen (google, linkedin, meta).
 * @property {string | null} utmMedium - Medio de adquisición (cpc, social, referral).
 * @property {string | null} gclid - Identificador de clic de Google Ads.
 * @property {string | null} fbclid - Identificador de clic de Meta Ads.
 * @property {string | null} liFatId - Identificador de clic de LinkedIn Ads.
 * @property {number} timestamp - Marca de tiempo Unix en milisegundos de la captura.
 */

/**
 * @typedef {Record<string, string>} CampaignMapping
 * @description Mapa de slugs de campañas conocidas a mensajes predeterminados de WhatsApp.
 */

/**
 * @typedef {'accepted' | 'rejected' | null} ConsentStatus
 * @description Estado de consentimiento para cookies y analítica de terceros según GDPR/LGPD.
 */

/**
 * @typedef {() => void} ScriptLoaderCallback
 * @description Función callback ejecutada tras la aprobación del consentimiento de cookies.
 */

/**
 * @typedef {string[]} CourseProgress
 * @description Array de identificadores o slugs de lecciones completadas por el estudiante.
 */

/**
 * @typedef {Object} QuizQuestionFeedback
 * @property {string} questionId - ID de la pregunta evaluada.
 * @property {number} correctOption - Índice o valor de la opción correcta.
 * @property {number} selectedValue - Valor seleccionado por el usuario.
 * @property {boolean} isCorrect - Indica si la respuesta coincide con la opción correcta.
 */

/**
 * @typedef {Object} QuizEvaluationResult
 * @property {number} totalQuestions - Cantidad total de preguntas en el cuestionario.
 * @property {number} correctAnswersCount - Cantidad de aciertos.
 * @property {number} scorePercentage - Calificación porcentual obtenida (0-100).
 */

export {};
