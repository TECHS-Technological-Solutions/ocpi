from uuid import uuid4
from unittest.mock import AsyncMock, MagicMock, patch

from fastapi.testclient import TestClient

from py_ocpi import get_application
from py_ocpi.core import enums, schemas
from py_ocpi.modules.locations.v_2_2_1.schemas import Location
from py_ocpi.modules.versions.enums import VersionNumber
from tests.test_modules.mocks.async_client import (
    MockAsyncClientGeneratorVersionsAndEndpoints,
)

from tests.test_modules.utils import (
    ClientAuthenticator,
    ENCODED_AUTH_TOKEN,
)

LOCATIONS = [
    {
        "country_code": "us",
        "party_id": "AAA",
        "id": str(uuid4()),
        "publish": True,
        "publish_allowed_to": [
            {
                "uid": str(uuid4()),
                "type": "APP_USER",
                "visual_number": "1",
                "issuer": "issuer",
                "group_id": "group_id",
            },
        ],
        "name": "name",
        "address": "address",
        "city": "city",
        "postal_code": "111111",
        "state": "state",
        "country": "USA",
        "coordinates": {
            "latitude": "latitude",
            "longitude": "longitude",
        },
        "related_locations": [
            {
                "latitude": "latitude",
                "longitude": "longitude",
                "name": {"language": "en", "text": "name"},
            },
        ],
        "parking_type": "ON_STREET",
        "evses": [
            {
                "uid": str(uuid4()),
                "evse_id": str(uuid4()),
                "status": "AVAILABLE",
                "status_schedule": {
                    "period_begin": "2022-01-01T00:00:00+00:00",
                    "period_end": "2022-01-01T00:00:00+00:00",
                    "status": "AVAILABLE",
                },
                "capabilities": [
                    "CREDIT_CARD_PAYABLE",
                ],
                "connectors": [
                    {
                        "id": str(uuid4()),
                        "standard": "DOMESTIC_A",
                        "format": "SOCKET",
                        "power_type": "DC",
                        "max_voltage": 100,
                        "max_amperage": 100,
                        "max_electric_power": 100,
                        "tariff_ids": [
                            str(uuid4()),
                        ],
                        "terms_and_conditions": "https://www.example.com",
                        "last_updated": "2022-01-01T00:00:00+00:00",
                    }
                ],
                "floor_level": "3",
                "coordinates": {
                    "latitude": "latitude",
                    "longitude": "longitude",
                },
                "physical_reference": "pr",
                "directions": [
                    {"language": "en", "text": "directions"},
                ],
                "parking_restrictions": [
                    "EV_ONLY",
                ],
                "images": [
                    {
                        "url": "https://www.example.com",
                        "thumbnail": "https://www.example.com",
                        "category": "CHARGER",
                        "type": "type",
                        "width": 10,
                        "height": 10,
                    },
                ],
                "last_updated": "2022-01-01T00:00:00+00:00",
            }
        ],
        "directions": [
            {"language": "en", "text": "directions"},
        ],
        "operator": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "suboperator": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "owner": {
            "name": "name",
            "website": "https://www.example.com",
            "logo": {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        },
        "facilities": ["MALL"],
        "time_zone": "UTC+2",
        "opening_times": {
            "twentyfourseven": True,
            "regular_hours": [
                {
                    "weekday": 1,
                    "period_begin": "8:00",
                    "period_end": "22:00",
                },
                {
                    "weekday": 2,
                    "period_begin": "8:00",
                    "period_end": "22:00",
                },
            ],
            "exceptional_openings": [
                {
                    "period_begin": "2022-01-01T00:00:00+00:00",
                    "period_end": "2022-01-02T00:00:00+00:00",
                },
            ],
            "exceptional_closings": [],
        },
        "charging_when_closed": False,
        "images": [
            {
                "url": "https://www.example.com",
                "thumbnail": "https://www.example.com",
                "category": "CHARGER",
                "type": "type",
                "width": 10,
                "height": 10,
            },
        ],
        "energy_mix": {
            "is_green_energy": True,
            "energy_sources": [
                {"source": "SOLAR", "percentage": 100},
            ],
            "supplier_name": "supplier_name",
            "energy_product_name": "energy_product_name",
        },
        "last_updated": "2022-01-02 00:00:00+00:00",
    }
]


@patch(
    "py_ocpi.core.push.httpx.AsyncClient",
    side_effect=MockAsyncClientGeneratorVersionsAndEndpoints,
)
def test_push(async_client):
    crud = AsyncMock()
    adapter = MagicMock()

    crud.get.return_value = LOCATIONS[0]
    adapter.location_adapter.return_value = Location(**LOCATIONS[0])

    app = get_application(
        version_numbers=[VersionNumber.v_2_2_1],
        roles=[enums.RoleEnum.cpo],
        crud=crud,
        adapter=adapter,
        authenticator=ClientAuthenticator,
        modules=[],
        http_push=True,
    )

    client = TestClient(app)
    data = schemas.Push(
        module_id=enums.ModuleID.locations,
        object_id="1",
        receivers=[
            schemas.Receiver(
                endpoints_url="http://example.com", auth_token="token"
            ),
        ],
    ).dict()
    client.post(
        "/push/2.2.1",
        json=data,
        headers={"Authorization": f"Token {ENCODED_AUTH_TOKEN}"},
    )

    crud.get.assert_awaited_once()
    adapter.location_adapter.assert_called_once()
