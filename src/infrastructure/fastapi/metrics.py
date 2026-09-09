"""Registro de métricas operativas en memoria (formato Prometheus text exposition).

Sin dependencias externas: solo stdlib + `fastapi`/`starlette` para el middleware.
Las métricas se resetean en cada reinicio del proceso (contadores en memoria),
adecuado para el monitoreo liviano del flujo transaccional (OBS-06).
"""

import time

from fastapi import Request, Response
from starlette.middleware.base import RequestResponseEndpoint


class Counter:
    """Contador monótono con etiquetas opcionales."""

    def __init__(self, name: str, help_text: str, labels: tuple[str, ...] = ()) -> None:
        self.name = name
        self.help_text = help_text
        self.labels = labels
        self._values: dict[tuple[str, ...], float] = {}

    def inc(self, amount: float = 1.0, label_values: tuple[str, ...] = ()) -> None:
        if len(label_values) != len(self.labels):
            raise ValueError("label_values debe tener la misma longitud que labels")
        key = label_values if self.labels else ()
        self._values[key] = self._values.get(key, 0.0) + amount

    def get(self, label_values: tuple[str, ...] = ()) -> float:
        key = label_values if self.labels else ()
        return self._values.get(key, 0.0)

    def _render(self) -> list[str]:
        lines: list[str] = []
        if not self.labels:
            value = self._values.get((), 0.0)
            lines.append(f"{self.name} {value}")
            return lines
        for label_values, value in self._values.items():
            label_str = ",".join(f'{self.labels[i]}="{label_values[i]}"' for i in range(len(self.labels)))
            lines.append(f"{self.name}{{{label_str}}} {value}")
        return lines


class Summary:
    """Acumulador de duración (suma + conteo)."""

    def __init__(self, name: str, help_text: str) -> None:
        self.name = name
        self.help_text = help_text
        self._sum: float = 0.0
        self._count: float = 0.0

    def observe(self, value: float) -> None:
        self._sum += value
        self._count += 1.0

    def _render(self) -> list[str]:
        return [
            f"{self.name}_sum {self._sum}",
            f"{self.name}_count {self._count}",
        ]


class MetricsRegistry:
    """Contenedor singleton de los contadores del negocio."""

    def __init__(self) -> None:
        self.leads_created_total = Counter("leads_created_total", "Total de leads persistidos correctamente")
        self.smtp_send_failures_total = Counter(
            "smtp_send_failures_total", "Total de fallos de notificación (email o Telegram)"
        )
        self.http_requests_total = Counter(
            "http_requests_total",
            "Total de requests HTTP por método, ruta y estado",
            labels=("method", "path", "status"),
        )
        self.http_request_duration_seconds = Summary(
            "http_request_duration_seconds", "Duración de requests HTTP en segundos"
        )

    def render(self) -> str:
        """Serializa todos los contadores en formato Prometheus text exposition 0.0.4."""
        blocks: list[str] = []
        for counter in (self.leads_created_total, self.smtp_send_failures_total, self.http_requests_total):
            blocks.append(f"# HELP {counter.name} {counter.help_text}")
            blocks.append(f"# TYPE {counter.name} counter")
            blocks.extend(counter._render())
        summary = self.http_request_duration_seconds
        blocks.append(f"# HELP {summary.name} {summary.help_text}")
        blocks.append(f"# TYPE {summary.name} summary")
        blocks.extend(summary._render())
        return "\n".join(blocks) + "\n"


registry = MetricsRegistry()


async def metrics_middleware(request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Mide duración y registra http_requests_total; excluye el propio /metrics."""
    if request.url.path == "/metrics":
        return await call_next(request)

    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    registry.http_requests_total.inc(label_values=(request.method, request.url.path, str(response.status_code)))
    registry.http_request_duration_seconds.observe(duration)
    return response
