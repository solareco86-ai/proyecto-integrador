"""Pruebas RED del lead magnet: propagación de `lead_source` por el pipeline."""

from typing import Any

import pytest

from src.application.dtos import ContactSubmitPayload
from src.application.gateways.notification_gateway import NotificationGateway
from src.application.use_cases.submit_lead import SubmitLeadInput, SubmitLeadUseCase
from src.domain.entities.lead import Lead
from src.domain.repositories.lead_repository import LeadRepository
from src.domain.value_objects.contact_info import ContactInfo

LEAD_SOURCE = "lead_magnet_auditoria"


def test_contact_payload_accepts_lead_source():
    payload = ContactSubmitPayload.model_validate(
        {
            "name": "Agustín",
            "comment": "Quiero la auditoría energética",
            "leadSource": LEAD_SOURCE,
        }
    )
    assert payload.leadSource == LEAD_SOURCE


def test_contact_payload_lead_source_defaults_none():
    payload = ContactSubmitPayload.model_validate({"name": "Agustín", "comment": "Hola"})
    assert payload.leadSource is None


def test_lead_entity_stores_lead_source():
    lead = Lead.create(
        contact=ContactInfo(name="Agustín"),
        comment="Quiero la auditoría",
        lead_source=LEAD_SOURCE,
    )
    assert lead.lead_source == LEAD_SOURCE


def test_submit_lead_input_accepts_lead_source():
    input_ = SubmitLeadInput(name="Agustín", comment="Quiero la auditoría", lead_source=LEAD_SOURCE)
    assert input_.lead_source == LEAD_SOURCE


@pytest.mark.asyncio
async def test_submit_lead_use_case_propagates_lead_source():
    class InMemoryLeadRepo(LeadRepository):
        def __init__(self) -> None:
            self.saved: list[Lead] = []

        async def save(self, lead: Lead) -> None:
            self.saved.append(lead)

    class NoopNotificationGateway(NotificationGateway):
        async def notify_lead(self, lead_data: dict[str, Any]) -> dict[str, Any]:
            return {"status": "sent", "channel": "test"}

    repo = InMemoryLeadRepo()
    use_case = SubmitLeadUseCase(repository=repo, notification_gateway=NoopNotificationGateway())

    await use_case.execute(SubmitLeadInput(name="Agustín", comment="Quiero la auditoría", lead_source=LEAD_SOURCE))

    assert len(repo.saved) == 1
    assert repo.saved[0].lead_source == LEAD_SOURCE
