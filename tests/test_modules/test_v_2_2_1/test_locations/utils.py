from uuid import uuid4

from py_ocpi.core import enums
from tests.test_modules.utils import (
    ENCODED_AUTH_TOKEN,
    ENCODED_RANDOM_AUTH_TOKEN,
    ClientAuthenticator,
)

CPO_BASE_URL = "/ocpi/cpo/2.2.1/locations/"
EMSP_BASE_URL = "/ocpi/emsp/2.2.1/locations/"
AUTH_HEADERS = {"Authorization": f"Token {ENCODED_AUTH_TOKEN}"}
WRONG_AUTH_HEADERS = {"Authorization": f"Token {ENCODED_RANDOM_AUTH_TOKEN}"}


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


class Crud:
    @classmethod
    async def get(
        cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs
    ):
        return LOCATIONS[0]

    @classmethod
    async def update(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        id,
        *args,
        **kwargs,
    ):
        return data

    @classmethod
    async def create(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        data: dict,
        *args,
        **kwargs,
    ):
        return data

    @classmethod
    async def list(
        cls,
        module: enums.ModuleID,
        role: enums.RoleEnum,
        filters: dict,
        *args,
        **kwargs,
    ) -> list:
        return LOCATIONS, 1, True
