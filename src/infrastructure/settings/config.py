import os

from dotenv import load_dotenv

load_dotenv()

APP_TITLE = "Portal ISFT N° 199 API"
STATIC_DIR = os.getenv("STATIC_DIR", "static")
STATIC_CACHE_SECONDS = int(os.getenv("STATIC_CACHE_SECONDS", "604800"))
# TTL (segundos) para recursos estáticos SIN versión (?v=): módulos internos
# importados relativamente y assets. Revalidación 304 vía ETag/Last-Modified.
STATIC_MODULE_MAX_AGE = int(os.getenv("STATIC_MODULE_MAX_AGE", "3600"))
TEMPLATES_DIR = os.getenv("TEMPLATES_DIR", "templates")
DATA_DIR = os.getenv("DATA_DIR", "data")
LOGGER_NAME = "app"
GOOGLE_ANALYTICS_ID = os.environ.get("GOOGLE_ANALYTICS_ID", None)
GOOGLE_ADS_ID = os.environ.get("GOOGLE_ADS_ID", None)
GOOGLE_ADS_CONVERSION_ID = os.environ.get("GOOGLE_ADS_CONVERSION_ID", None)
GOOGLE_ADS_WHATSAPP_CONVERSION_ID = os.environ.get("GOOGLE_ADS_WHATSAPP_CONVERSION_ID", None)
CLARITY_ID = os.environ.get("CLARITY_ID", None)
ROBOTS_TXT_PATH = os.getenv("ROBOTS_TXT_PATH", "static/robots.txt")
HUMANS_TXT_PATH = os.getenv("HUMANS_TXT_PATH", "static/humans.txt")
LLMS_TXT_PATH = os.getenv("LLMS_TXT_PATH", "static/llms.txt")
LLMS_FULL_TXT_PATH = os.getenv("LLMS_FULL_TXT_PATH", "static/llms-full.txt")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# SMTP para notificaciones de leads por email
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
NOTIFICATION_EMAIL = os.getenv("NOTIFICATION_EMAIL", "")

WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE", "541156297160")
WHATSAPP_MESSAGE = os.getenv(
    "WHATSAPP_MESSAGE",
    "Hola! Quisiera realizar una consulta sobre las carreras e inscripciones del ISFT N° 199.",
)

BASE_URL = os.getenv("BASE_URL", "https://datamaq.com.ar")

# SPA de telemetría desacoplada (app.datamaq.com.ar)
APP_DATAMAQ_URL = os.getenv("APP_DATAMAQ_URL", "https://app.datamaq.com.ar")

# MySQL para persistencia de leads
DATABASE_URL = os.getenv("DATABASE_URL", "")

# Telegram para notificaciones instantáneas de leads
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Backend de Telemetría e IoT Industrial
TELEMETRY_API_URL = os.getenv(
    "TELEMETRY_API_URL",
    "https://api.datamaq.com.ar" if not DEBUG else "http://localhost:8000",
)
TELEMETRY_WS_URL = os.getenv(
    "TELEMETRY_WS_URL",
    "wss://api.datamaq.com.ar/ws/live" if not DEBUG else "ws://localhost:8000/ws/live",
)

# GA4 Measurement Protocol (Server-Side Conversion Tracking)
GA4_MEASUREMENT_ID = os.getenv("GA4_MEASUREMENT_ID", None)
GA4_API_SECRET = os.getenv("GA4_API_SECRET", None)

# Datamaq Hub Webhook Ingest
DATAMAQ_HUB_URL = os.getenv("DATAMAQ_HUB_URL", None)
DATAMAQ_HUB_API_KEY = os.getenv("DATAMAQ_HUB_API_KEY", None)

# Rate Limiting para formularios
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
RATE_LIMIT_MAX_REQUESTS = int(os.getenv("RATE_LIMIT_MAX_REQUESTS", "3"))

# Caché HTTP para HTML y Sitemaps
# `no-cache` fuerza revalidación en cada navegación: el HTML siempre se sirve fresco
# (evita servir plantillas viejas cacheadas por CDN/proxy durante horas).
HTML_CACHE_CONTROL = os.getenv(
    "HTML_CACHE_CONTROL",
    "no-cache, must-revalidate",
)

# Cabeceras de Seguridad
HSTS_HEADER = os.getenv("HSTS_HEADER", "max-age=31536000; includeSubDomains")


def _get_git_commit_sha() -> str:
    """Obtiene el hash SHA corto del commit actual vía variable de entorno o git."""
    sha = os.getenv("GIT_COMMIT_SHA") or os.getenv("GITHUB_SHA")
    if sha:
        return sha[:7]
    try:
        import subprocess

        res = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2.0,
            check=False,
        )
        if res.returncode == 0 and res.stdout.strip():
            return res.stdout.strip()
    except Exception:
        pass
    return "dev"


GIT_COMMIT_SHA = _get_git_commit_sha()

