from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.infrastructure.gateways.datamaq_hub_gateway import DatamaqHubGateway


@pytest.mark.asyncio
async def test_datamaq_hub_gateway_notify_lead_success():
    gateway = DatamaqHubGateway(hub_url="https://hub.datamaq.com.ar", api_key="secret_token_123")
    lead_data = {
        "name": "Maria Lopez",
        "email": "maria@empresa.com",
        "phone": "+54 11 1234-5678",
        "company": "Industrias Metalicas",
        "comment": "Consulta por retrofit IoT",
        "traffic_source": "google_ads",
        "utm_campaign": "retrofit-iot",
    }

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.text = '{"status":"ok"}'

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_lead(lead_data)
        assert result["status"] == "sent"
        assert result["channel"] == "datamaq_hub"
        assert mock_post.called
        # Verificar que se envió el header de API key
        args, kwargs = mock_post.call_args
        assert kwargs["headers"]["X-Api-Key"] == "secret_token_123"


@pytest.mark.asyncio
async def test_datamaq_hub_gateway_notify_lead_failure():
    gateway = DatamaqHubGateway(hub_url="https://hub.datamaq.com.ar")
    lead_data = {"name": "Maria Lopez"}

    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_response.text = "Internal Server Error"

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response
        result = await gateway.notify_lead(lead_data)
        assert result["status"] == "failed"


@pytest.mark.asyncio
async def test_datamaq_hub_gateway_network_error():
    gateway = DatamaqHubGateway(hub_url="https://hub.datamaq.com.ar")
    lead_data = {"name": "Maria Lopez"}

    with patch("httpx.AsyncClient.post", side_effect=Exception("Timeout connecting to hub")):
        result = await gateway.notify_lead(lead_data)
        assert result["status"] == "error"
        assert "Timeout connecting to hub" in result["error"]
