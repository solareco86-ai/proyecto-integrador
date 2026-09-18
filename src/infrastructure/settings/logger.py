import logging
import sys

COLORS = {
    "DEBUG": "\033[36m",
    "INFO": "\033[92m",
    "WARNING": "\033[93m",
    "ERROR": "\033[91m",
    "CRITICAL": "\033[91m",
    "RESET": "\033[0m",
}


class ColorFormatter(logging.Formatter):
    """Formatter con colores ANSI para terminal interactiva."""

    def format(self, record: logging.LogRecord) -> str:
        record.levelname = f"{COLORS.get(record.levelname, COLORS['RESET'])}{record.levelname}{COLORS['RESET']}"
        return super().format(record)


class PlainFormatter(logging.Formatter):
    """Formatter sin ANSI para journald/logs en producción."""


def setup_logger(name: str = "app", debug: bool = False) -> logging.Logger:
    l = logging.getLogger(name)
    l.setLevel(logging.DEBUG if debug else logging.INFO)

    if not l.handlers:
        h = logging.StreamHandler(sys.stdout)
        is_tty = hasattr(sys.stdout, "isatty") and sys.stdout.isatty()
        if is_tty:
            h.setFormatter(
                ColorFormatter("%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
            )
        else:
            h.setFormatter(
                PlainFormatter("%(asctime)s %(levelname)s %(name)s: %(message)s", datefmt="%Y-%m-%dT%H:%M:%S")
            )
        l.addHandler(h)

    return l


def get_logger(name: str = "app", debug: bool = False) -> logging.Logger:
    """Convenience wrapper que devuelve un logger configurado desde el módulo central.

    Llamar a `get_logger(__name__)` desde otros módulos mantiene un único
    `import logging` (en este fichero) mientras ofrecemos una API simple.
    """
    return setup_logger(name=name, debug=debug)
