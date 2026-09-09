"""Tests del watchdog de alerting sobre el flujo de leads (OBS-02)."""

from pathlib import Path

import pytest

import scripts.watchdog_leads as wd
from scripts.watchdog_leads import (
    CONSECUTIVE_FAILURES_REQUIRED,
    Alert,
    apply_debounce,
    evaluate_checks,
    format_http_diagnostic,
    parse_metrics_text,
    should_send_alert,
)


def test_parse_metrics_text_extrae_contadores() -> None:
    texto = (
        "# HELP leads_created_total Total de leads\n"
        "# TYPE leads_created_total counter\n"
        "leads_created_total 7.0\n"
        "# HELP smtp_send_failures_total Fallos\n"
        "# TYPE smtp_send_failures_total counter\n"
        "smtp_send_failures_total 1.0\n"
    )
    resultado = parse_metrics_text(texto)
    assert resultado == {"leads_created_total": 7.0, "smtp_send_failures_total": 1.0}


def test_parse_metrics_text_ignora_comentarios() -> None:
    assert parse_metrics_text("# solo un comentario\n") == {}


def test_evaluate_checks_todo_ok_sin_alertas() -> None:
    assert evaluate_checks(healthz_ok=True, ready_ok=True, smtp_failures_delta=0) == []


def test_evaluate_checks_site_down_emite_solo_site_down() -> None:
    alertas = evaluate_checks(healthz_ok=False, ready_ok=False, smtp_failures_delta=0)
    assert len(alertas) == 1
    assert alertas[0].alert_type == "site_down"


def test_evaluate_checks_db_not_ready() -> None:
    alertas = evaluate_checks(healthz_ok=True, ready_ok=False, smtp_failures_delta=0)
    assert [a.alert_type for a in alertas] == ["db_not_ready"]


def test_evaluate_checks_notification_failures() -> None:
    alertas = evaluate_checks(healthz_ok=True, ready_ok=True, smtp_failures_delta=3)
    assert len(alertas) == 1
    assert alertas[0].alert_type == "notification_failures"
    assert "3" in alertas[0].message


def test_should_send_alert_sin_historial_envia() -> None:
    assert should_send_alert("site_down", last_sent_at=None, now=100.0, cooldown_seconds=300.0) is True


def test_should_send_alert_dentro_de_cooldown_no_envia() -> None:
    assert should_send_alert("site_down", last_sent_at=100.0, now=200.0, cooldown_seconds=300.0) is False


def test_should_send_alert_fuera_de_cooldown_envia() -> None:
    assert should_send_alert("site_down", last_sent_at=100.0, now=500.0, cooldown_seconds=300.0) is True


def test_alert_es_dataclass() -> None:
    a = Alert(alert_type="site_down", message="El sitio no responde")
    assert a.alert_type == "site_down"
    assert a.message == "El sitio no responde"


# ---- Debounce anti-falso-positivo ----


def test_debounce_un_fallo_no_emite() -> None:
    emitir, nuevo = apply_debounce("db_not_ready", is_ok=False, consecutive=0, required=CONSECUTIVE_FAILURES_REQUIRED)
    assert emitir is False
    assert nuevo == 1


def test_debounce_dos_fallos_consecutivos_emite() -> None:
    emitir, nuevo = apply_debounce("db_not_ready", is_ok=False, consecutive=1, required=CONSECUTIVE_FAILURES_REQUIRED)
    assert emitir is True
    assert nuevo == 2


def test_debounce_ok_intermedio_resetea() -> None:
    # Primer fallo: 0 -> 1
    emitir, nuevo = apply_debounce("db_not_ready", is_ok=False, consecutive=0, required=CONSECUTIVE_FAILURES_REQUIRED)
    assert emitir is False and nuevo == 1
    # Check OK entre medio: resetea a 0
    emitir, nuevo = apply_debounce("db_not_ready", is_ok=True, consecutive=1, required=CONSECUTIVE_FAILURES_REQUIRED)
    assert emitir is False and nuevo == 0
    # Fallo tras el OK: vuelve a empezar en 1, sin alertar
    emitir, nuevo = apply_debounce("db_not_ready", is_ok=False, consecutive=0, required=CONSECUTIVE_FAILURES_REQUIRED)
    assert emitir is False and nuevo == 1


def test_debounce_contador_independiente_por_tipo() -> None:
    _, n_db = apply_debounce("db_not_ready", is_ok=False, consecutive=0, required=CONSECUTIVE_FAILURES_REQUIRED)
    _, n_site = apply_debounce("site_down", is_ok=False, consecutive=0, required=CONSECUTIVE_FAILURES_REQUIRED)
    assert n_db == 1
    assert n_site == 1


def test_debounce_requerido_personalizable() -> None:
    # Con required=3, dos fallos aún no emiten.
    emitir, nuevo = apply_debounce("notification_failures", is_ok=False, consecutive=1, required=3)
    assert emitir is False and nuevo == 2


# ---- Logging de diagnóstico ----


def test_format_http_diagnostic_incluye_status_y_body() -> None:
    msg = format_http_diagnostic("/ready", 503, '{"status":"error","db":"down"}')
    assert msg == '[watchdog] /ready -> HTTP 503: {"status":"error","db":"down"}'


def test_format_http_diagnostic_recorta_body_largo() -> None:
    body = "x" * 2000
    msg = format_http_diagnostic("/metrics", 500, body)
    assert len(msg) < 2000
    assert msg.endswith("...")


# ---- Compatibilidad con state viejo ----


def test_state_viejo_sin_claves_nuevas_arranca_con_contadores_en_cero(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(wd, "STATE_FILE", str(tmp_path / "watchdog_state.json"))
    monkeypatch.setattr(wd, "OLD_STATE_FILE", str(tmp_path / "old_state.json"))
    # State viejo: solo tenía smtp_failures_total y last_alerted.
    (tmp_path / "watchdog_state.json").write_text(
        '{"smtp_failures_total": 3.0, "last_alerted": {"db_not_ready": 123.0}}',
        encoding="utf-8",
    )
    state = wd._load_state()
    assert state["consecutive_failures"] == {}
    assert state["smtp_failures_total"] == 3.0
    assert state["last_alerted"] == {"db_not_ready": 123.0}


def test_load_state_migra_desde_ruta_vieja(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    new_path = tmp_path / "new_state.json"
    old_path = tmp_path / "old_state.json"
    monkeypatch.setattr(wd, "STATE_FILE", str(new_path))
    monkeypatch.setattr(wd, "OLD_STATE_FILE", str(old_path))
    old_path.write_text('{"smtp_failures_total": 2.0, "last_alerted": {}}', encoding="utf-8")
    state = wd._load_state()
    assert state["smtp_failures_total"] == 2.0
    assert state["consecutive_failures"] == {}


def test_load_state_sin_archivos_devuelve_defaults(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(wd, "STATE_FILE", str(tmp_path / "no.json"))
    monkeypatch.setattr(wd, "OLD_STATE_FILE", str(tmp_path / "no_old.json"))
    state = wd._load_state()
    assert state == {"smtp_failures_total": 0.0, "last_alerted": {}, "consecutive_failures": {}}
