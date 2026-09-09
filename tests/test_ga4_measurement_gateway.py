from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.infrastructure.gateways.ga4_measurement_gateway import GA4MeasurementGateway


@pytest.mark.asyncio
async def test_ga4_measurement_gateway_notify_lead_success():
    gateway = GA4MeasurementGateway(measurement_id="G-TEST123", api_secret="SECRET123")
    lead_data = {
        "name": "Juan Perez",
        "email": "juan@test.com",
        "lead_source": "landing_calidad_energia",
        "traffic_source": "google_ads",
        "utm_campaign": "calidad-energia",
        "gclid": "gclid_test_123",
        "page_location": "https://datamaq.com.ar/landing/calidad-energia",
    }

    mock_response = MagicMock()
    mock_response.status_code = 204
    mock_response.text = ""

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_lead(lead_data)
        assert result["status"] == "sent"
        assert result["channel"] == "ga4_measurement_protocol"
        assert mock_post.called


@pytest.mark.asyncio
async def test_ga4_measurement_gateway_notify_lead_failure():
    gateway = GA4MeasurementGateway(measurement_id="G-TEST123", api_secret="SECRET123")
    lead_data = {"name": "Juan Perez"}

    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_response.text = "Bad Request"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_lead(lead_data)
        assert result["status"] == "failed"


@pytest.mark.asyncio
async def test_ga4_measurement_gateway_network_error():
    gateway = GA4MeasurementGateway(measurement_id="G-TEST123", api_secret="SECRET123")
    lead_data = {"name": "Juan Perez"}

    with patch("httpx.AsyncClient.post", side_effect=Exception("Connection refused")):
        result = await gateway.notify_lead(lead_data)
        assert result["status"] == "error"
        assert "Connection refused" in result["error"]


@pytest.mark.asyncio
async def test_ga4_measurement_gateway_notify_whatsapp_click():
    gateway = GA4MeasurementGateway(measurement_id="G-TEST123", api_secret="SECRET123")
    click_data = {
        "element": "Hero CTA",
        "page_location": "https://datamaq.com.ar/landing/calidad-energia",
        "utm_campaign": "calidad-energia",
    }

    mock_response = MagicMock()
    mock_response.status_code = 204

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_whatsapp_click(click_data)
        assert result["status"] == "sent"
