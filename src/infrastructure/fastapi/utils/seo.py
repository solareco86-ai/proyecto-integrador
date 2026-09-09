from typing import Any
from urllib.parse import urlsplit, urlunsplit

from src.infrastructure.settings import config


def canonical_url(request_url: Any, force_https: bool = True, strip_query: bool = True) -> str:
    """
    Build a canonical URL from a request URL.

    - Forces the configured BASE_URL scheme and netloc.
    - Strips query params if requested.
    - Keeps path and fragment as-is.
    """
    url = str(request_url)
    _, _, path, query, fragment = urlsplit(url)

    # Reemplazar esquema y netloc con los configurados en BASE_URL
    base_scheme, base_netloc, _, _, _ = urlsplit(config.BASE_URL)
    scheme = base_scheme
    netloc = base_netloc

    if force_https:
        scheme = "https"
    if strip_query:
        query = ""
    return urlunsplit((scheme, netloc, path, query, fragment))
