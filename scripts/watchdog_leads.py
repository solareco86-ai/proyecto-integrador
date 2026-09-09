"""Watchdog de alerting sobre el flujo transaccional (OBS-02).

Script standalone que corre por systemd timer/cron FUERA del proceso de la app.
Consulta `/healthz`, `/ready` y `/metrics` del sitio y emite alertas por Telegram
con cooldown anti-spam. La lógica de negocio (parseo, evaluación, cooldown) está
desacoplada de la red para ser testeable sin infraestructura.
"""

import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any

import httpx

try:
    import pwd
except ImportError:
    pwd = None

# Ruta persistente (NO en /tmp: se borra en reboot y se pierde el debounce/cooldown,
# provocando falsos positivos en serie).
STATE_FILE = "/var/www/www-datamaq/var/watchdog_state.json"
OLD_STATE_FILE = "/tmp/datamaq_watchdog_state.json"
STATE_DIR = os.path.dirname(STATE_FILE)
COOLDOWN_SECONDS = 300.0
CONSECUTIVE_FAILURES_REQUIRED = int(os.getenv("WATCHDOG_CONSECUTIVE_FAILURES_REQUIRED", "2"))
DIAGNOSTIC_BODY_MAX_CHARS = 500


@dataclass(frozen=True)
class Alert:
    """Alerta emitida por el watchdog."""

    alert_type: str
    message: str


def parse_metrics_text(text: str) -> dict[str, float]:
    """Parsea líneas `<nombre>{...} <valor>` y devuelve `{nombre: valor}`.

    Ignora comentarios (`#`) y líneas HELP/TYPE. En caso de duplicados con
    labels, prevalece la última línea por nombre.
    """
    result: dict[str, float] = {}
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        # Extraer nombre: antes de `{` si hay labels, o primer token si no.
        if "{" in stripped:
            name = stripped.split("{", 1)[0]
        else:
            name = stripped.split()[0]
        # Extraer valor: último token.
        parts = stripped.split()
        if len(parts) < 2:
            continue
        try:
            result[name] = float(parts[-1])
        except ValueError:
            continue
    return result


def evaluate_checks(healthz_ok: bool, ready_ok: bool, smtp_failures_delta: int) -> list[Alert]:
    """Evalúa el estado del sitio y emite alertas priorizadas.

    `site_down` (healthz caído) corta la evaluación para evitar doble alerta
    con `db_not_ready`.
    """
    alerts: list[Alert] = []
    if not healthz_ok:
        alerts.append(Alert(alert_type="site_down", message="El sitio no responde en /healthz"))
        return alerts
    if not ready_ok:
        alerts.append(Alert(alert_type="db_not_ready", message="La base de datos de leads no está accesible (/ready)"))
    if smtp_failures_delta > 0:
        alerts.append(
            Alert(
                alert_type="notification_failures",
                message=f"Se detectaron {smtp_failures_delta} fallos de notificación desde la última ejecución",
            )
        )
    return alerts


def should_send_alert(alert_key: str, last_sent_at: float | None, now: float, cooldown_seconds: float) -> bool:
    """True si la alerta debe enviarse (sin historial o fuera del cooldown)."""
    if last_sent_at is None:
        return True
    return now - last_sent_at >= cooldown_seconds


def format_http_diagnostic(path: str, status: int, body: str) -> str:
    """Formatea un mensaje de diagnóstico para un endpoint con status != 200."""
    recortado = body.strip()
    if len(recortado) > DIAGNOSTIC_BODY_MAX_CHARS:
        recortado = recortado[:DIAGNOSTIC_BODY_MAX_CHARS] + "..."
    return f"[watchdog] {path} -> HTTP {status}: {recortado}"


def apply_debounce(alert_type: str, is_ok: bool, consecutive: int, required: int) -> tuple[bool, int]:
    """Aplica el debounce anti-falso-positivo.

    Devuelve `(emitir, nuevo_conteo)`. `emitir` es True solo cuando el check
    falló el número requerido de corridas consecutivas. Un check OK resetea el
    contador a 0.
    """
    if is_ok:
        return False, 0
    nuevo = consecutive + 1
    return nuevo >= required, nuevo


def _ensure_state_dir() -> None:
    """Crea el directorio del state file con permisos para datamaq."""
    os.makedirs(STATE_DIR, exist_ok=True)
    if pwd is None or not hasattr(os, "chown"):
        return
    try:
        uid = pwd.getpwnam("datamaq").pw_uid
        gid = pwd.getpwnam("datamaq").pw_gid
        os.chown(STATE_DIR, uid, gid)
    except (KeyError, OSError):
        pass


def _migrate_old_state() -> dict[str, Any]:
    """Migra el state desde la ruta antigua (/tmp) si existe y la nueva no."""
    if os.path.exists(STATE_FILE):
        return {}
    try:
        with open(OLD_STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}


def _load_state() -> dict[str, Any]:
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            state = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        state = {}
    if not state:
        state = _migrate_old_state()
    # Compatibilidad: state viejo sin claves nuevas arranca con contadores en 0.
    state.setdefault("smtp_failures_total", 0.0)
    state.setdefault("last_alerted", {})
    state.setdefault("consecutive_failures", {})
    return state


def _save_state(state: dict[str, Any]) -> None:
    _ensure_state_dir()
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f)


def send_alerts(alerts: list[Alert], bot_token: str, chat_id: str) -> None:
    """Envía alertas a Telegram vía Bot API. Silencioso si no hay configuración."""
    if not bot_token or not chat_id:
        print("[watchdog] Telegram no configurado; omitiendo envío.", file=sys.stderr)
        return
    for alert in alerts:
        text = f"⚠️ DataMaq alert: {alert.message}"
        try:
            httpx.post(
                f"https://api.telegram.org/bot{bot_token}/sendMessage",
                json={"chat_id": chat_id, "text": text},
                timeout=10.0,
            )
        except httpx.HTTPError as exc:
            print(f"[watchdog] Error enviando alerta {alert.alert_type}: {exc}", file=sys.stderr)


def main() -> int:
    """Orquesta la verificación de endpoints y el envío de alertas por Telegram."""
    base_url = os.getenv("WATCHDOG_BASE_URL", "https://datamaq.com.ar")
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.getenv("TELEGRAM_CHAT_ID", "")

    state = _load_state()
    previous_smtp_failures = float(state.get("smtp_failures_total", 0.0))
    last_alerted: dict[str, float] = state.get("last_alerted", {})
    consecutive_failures: dict[str, int] = state.get("consecutive_failures", {})

    try:
        with httpx.Client(timeout=10.0) as client:
            healthz_resp = client.get(f"{base_url}/healthz")
            ready_resp = client.get(f"{base_url}/ready")
            metrics_resp = client.get(f"{base_url}/metrics")
    except httpx.HTTPError:
        send_alerts(
            [Alert(alert_type="site_down", message="No se pudo conectar con el sitio")],
            bot_token,
            chat_id,
        )
        return 1

    now = time.time()

    healthz_ok = healthz_resp.status_code == 200
    ready_ok = ready_resp.status_code == 200

    if healthz_resp.status_code != 200:
        print(
            format_http_diagnostic("/healthz", healthz_resp.status_code, healthz_resp.text),
            file=sys.stderr,
        )
    if ready_resp.status_code != 200:
        print(
            format_http_diagnostic("/ready", ready_resp.status_code, ready_resp.text),
            file=sys.stderr,
        )
    if metrics_resp.status_code != 200:
        print(
            format_http_diagnostic("/metrics", metrics_resp.status_code, metrics_resp.text),
            file=sys.stderr,
        )

    smtp_failures = parse_metrics_text(metrics_resp.text).get("smtp_send_failures_total", 0.0)
    if smtp_failures >= previous_smtp_failures:
        smtp_failures_delta = int(smtp_failures - previous_smtp_failures)
    else:
        # Reinicio del proceso (contadores reseteados): no reportar delta negativo.
        smtp_failures_delta = 0

    alerts = evaluate_checks(healthz_ok=healthz_ok, ready_ok=ready_ok, smtp_failures_delta=smtp_failures_delta)

    # Debounce anti-falso-positivo: solo se alerta tras N fallos consecutivos.
    checks_ok: dict[str, bool] = {
        "site_down": healthz_ok,
        "db_not_ready": ready_ok,
        "notification_failures": smtp_failures_delta <= 0,
    }

    debounced_alerts: list[Alert] = []
    for alert in alerts:
        is_ok = checks_ok[alert.alert_type]
        current = consecutive_failures.get(alert.alert_type, 0)
        emitir, nuevo = apply_debounce(alert.alert_type, is_ok, current, CONSECUTIVE_FAILURES_REQUIRED)
        consecutive_failures[alert.alert_type] = nuevo
        if not emitir:
            print(
                f"[watchdog] {alert.alert_type}: fallo {nuevo}/{CONSECUTIVE_FAILURES_REQUIRED}, aún no se alerta",
                file=sys.stderr,
            )
            continue
        debounced_alerts.append(alert)

    # Reset de contadores de debounce para checks que quedaron OK (no presentes en alerts).
    for alert_type in checks_ok:
        if checks_ok[alert_type]:
            consecutive_failures.pop(alert_type, None)

    pending: list[Alert] = []
    for alert in debounced_alerts:
        if should_send_alert(alert.alert_type, last_alerted.get(alert.alert_type), now, COOLDOWN_SECONDS):
            pending.append(alert)
            last_alerted[alert.alert_type] = now

    if pending:
        send_alerts(pending, bot_token, chat_id)

    state["smtp_failures_total"] = smtp_failures
    state["last_alerted"] = last_alerted
    state["consecutive_failures"] = consecutive_failures
    _save_state(state)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
