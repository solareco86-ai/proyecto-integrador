"""Construcción declarativa del header Content-Security-Policy (CSP).

Centraliza la lista blanca de orígenes autorizados en un diccionario legible
para facilitar la auditoría, el mantenimiento y las pruebas unitarias por
directiva, evitando la edición manual de un string monolítico.
"""

_CSP_DIRECTIVES: dict[str, list[str]] = {
    "default-src": ["'self'"],
    "script-src": [
        "'self'",
        "'unsafe-inline'",
        "https://cdn.jsdelivr.net",
        "https://www.googletagmanager.com",
        "https://www.google-analytics.com",
        "https://www.googleadservices.com",
        "https://googleads.g.doubleclick.net",
        "https://www.google.com",
        "https://www.google.com.ar",
        "https://www.clarity.ms",
        "https://scripts.clarity.ms",
        "https://*.clarity.ms",
    ],
    "style-src": ["'self'", "'unsafe-inline'", "https://cdn.jsdelivr.net"],
    "img-src": [
        "'self'",
        "data:",
        "https://www.google-analytics.com",
        "https://analytics.google.com",
        "https://www.googletagmanager.com",
        "https://www.googleadservices.com",
        "https://googleads.g.doubleclick.net",
        "https://ad.doubleclick.net",
        "https://*.doubleclick.net",
        "https://www.google.com",
        "https://www.google.com.ar",
        "https://*.google.com",
        "https://*.google.com.ar",
        "https://www.clarity.ms",
        "https://*.clarity.ms",
        "https://c.clarity.ms",
        "https://c.bing.com",
        "https://*.bing.com",
    ],
    "connect-src": [
        "'self'",
        "ws:",
        "wss:",
        "http://localhost:*",
        "http://127.0.0.1:*",
        "ws://localhost:*",
        "ws://127.0.0.1:*",
        "https://www.google-analytics.com",
        "https://analytics.google.com",
        "https://*.google-analytics.com",
        "https://www.googletagmanager.com",
        "https://www.googleadservices.com",
        "https://googleads.g.doubleclick.net",
        "https://stats.g.doubleclick.net",
        "https://ad.doubleclick.net",
        "https://*.doubleclick.net",
        "https://www.google.com",
        "https://www.google.com.ar",
        "https://*.google.com",
        "https://*.google.com.ar",
        "https://www.clarity.ms",
        "https://scripts.clarity.ms",
        "https://*.clarity.ms",
        "https://c.clarity.ms",
        "https://c.bing.com",
        "https://*.bing.com",
    ],
    "font-src": ["'self'", "https://cdn.jsdelivr.net"],
    "frame-src": ["'self'", "https://www.clarity.ms", "https://*.clarity.ms"],
    "report-uri": ["/csp-report"],
}


def build_csp(telemetry_hosts: tuple[str, ...] = ()) -> str:
    """Construye el header Content-Security-Policy.

    ``telemetry_hosts`` son los orígenes de telemetría (API + WebSocket) que se
    añaden al final de ``connect-src``. El orden de directivas es estable y el
    resultado es determinista.
    """
    parts: list[str] = []
    for directive, sources in _CSP_DIRECTIVES.items():
        directive_sources = list(sources)
        if directive == "connect-src":
            directive_sources.extend(telemetry_hosts)
        parts.append(f"{directive} {' '.join(directive_sources)}")
    return "; ".join(parts)
