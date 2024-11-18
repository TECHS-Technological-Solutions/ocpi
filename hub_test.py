from uuid import uuid4

from py_ocpi import get_application
from py_ocpi.core import enums
from py_ocpi.modules.versions.enums import VersionNumber
from py_ocpi.modules.locations.v_2_2_1.schemas import Location
from py_ocpi.modules.hubclientinfo.utils import HubTopologyHandler
from py_ocpi.core.exceptions import AuthorizationOCPIError


LOCATIONS = [
    {
        'country_code': 'us',
        'party_id': 'AAA',
        'id': str(uuid4()),
        'publish': True,
        'publish_allowed_to': [
            {
                'uid': str(uuid4()),
                'type': 'APP_USER',
                'visual_number': '1',
                'issuer': 'issuer',
                'group_id': 'group_id',
            },
        ],
        'name': 'name',
        'address': 'address',
        'city': 'city',
        'postal_code': '111111',
        'state': 'state',
        'country': 'USA',
        'coordinates': {
            'latitude': 'latitude',
            'longitude': 'longitude',
        },
        'related_locations': [
            {
                'latitude': 'latitude',
                'longitude': 'longitude',
                'name': {
                    'language': 'en',
                    'text': 'name'
                }
            },
        ],
        'parking_type': 'ON_STREET',
        'evses': [
            {
                'uid': str(uuid4()),
                'evse_id': str(uuid4()),
                'status': 'AVAILABLE',
                'status_schedule': {
                    'period_begin': '2022-01-01T00:00:00+00:00',
                    'period_end': '2022-01-01T00:00:00+00:00',
                    'status': 'AVAILABLE'
                },
                'capabilities': [
                    'CREDIT_CARD_PAYABLE',
                ],
                'connectors': [
                    {
                        'id': str(uuid4()),
                        'standard': 'DOMESTIC_A',
                        'format': 'SOCKET',
                        'power_type': 'DC',
                        'max_voltage': 100,
                        'max_amperage': 100,
                        'max_electric_power': 100,
                        'tariff_ids': [str(uuid4()), ],
                        'terms_and_conditions': 'https://www.example.com',
                        'last_updated': '2022-01-01T00:00:00+00:00',
                    }
                ],
                'floor_level': '3',
                'coordinates': {
                    'latitude': 'latitude',
                    'longitude': 'longitude',
                },
                'physical_reference': 'pr',
                'directions': [
                    {
                        'language': 'en',
                        'text': 'directions'
                    },
                ],
                'parking_restrictions': ['EV_ONLY', ],
                'images': [
                    {
                        'url': 'https://www.example.com',
                        'thumbnail': 'https://www.example.com',
                        'category': 'CHARGER',
                        'type': 'type',
                        'width': 10,
                        'height': 10
                    },
                ],
                'last_updated': '2022-01-01T00:00:00+00:00'
            }
        ],
        'directions': [
            {
                'language': 'en',
                'text': 'directions'
            },
        ],
        'operator': {
            'name': 'name',
            'website': 'https://www.example.com',
            'logo': {
                'url': 'https://www.example.com',
                'thumbnail': 'https://www.example.com',
                'category': 'CHARGER',
                'type': 'type',
                'width': 10,
                'height': 10
            }
        },
        'suboperator': {
            'name': 'name',
            'website': 'https://www.example.com',
            'logo': {
                'url': 'https://www.example.com',
                'thumbnail': 'https://www.example.com',
                'category': 'CHARGER',
                'type': 'type',
                'width': 10,
                'height': 10
            }
        },
        'owner': {
            'name': 'name',
            'website': 'https://www.example.com',
            'logo': {
                'url': 'https://www.example.com',
                'thumbnail': 'https://www.example.com',
                'category': 'CHARGER',
                'type': 'type',
                'width': 10,
                'height': 10
            }
        },
        'facilities': ['MALL'],
        'time_zone': 'UTC+2',
        'opening_times': {
            'twentyfourseven': True,
            'regular_hours': [
                {
                    'weekday': 1,
                    'period_begin': '8:00',
                    'period_end': '22:00',
                },
                {
                    'weekday': 2,
                    'period_begin': '8:00',
                    'period_end': '22:00',
                },
            ],
            'exceptional_openings': [
                {
                    'period_begin': '2022-01-01T00:00:00+00:00',
                    'period_end': '2022-01-02T00:00:00+00:00',
                },
            ],
            'exceptional_closings': [],
        },
        'charging_when_closed': False,
        'images': [
            {
                'url': 'https://www.example.com',
                'thumbnail': 'https://www.example.com',
                'category': 'CHARGER',
                'type': 'type',
                'width': 10,
                'height': 10
            },
        ],
        'energy_mix': {
            'is_green_energy': True,
            'energy_sources': [
                {
                    'source': 'SOLAR',
                    'percentage': 100
                },
            ],
            'supplier_name': 'supplier_name',
            'energy_product_name': 'energy_product_name'
        },
        'last_updated': '2022-01-02 00:00:00+00:00',
    }
]


class Crud:
    @classmethod
    async def get(cls, module: enums.ModuleID, role: enums.RoleEnum, id, *args, **kwargs):
        return LOCATIONS[0]

    @classmethod
    async def list(cls, module: enums.ModuleID, role: enums.RoleEnum, filters: dict, *args, **kwargs) -> list:
        return LOCATIONS, 1, True


class Authenticator:
    """Base class responsible for verifying authorization tokens."""

    @classmethod
    async def authenticate(cls, auth_token: str) -> None:
        """Authenticate given auth token.

        :raises AuthorizationOCPIError: If auth_token is not in a given
          list of verified tokens C.
        """
        list_token_c = await cls.get_valid_token_c()
        if auth_token not in list_token_c:
            print(f"Given `{auth_token}` token is not valid")
            raise AuthorizationOCPIError

    @classmethod
    async def authenticate_credentials(
        cls,
        auth_token: str,
    ):
        """Authenticate given auth token where both tokens valid."""
        if auth_token:
            list_token_a = await cls.get_valid_token_a()
            if auth_token in list_token_a:
                print(f"Token A `{auth_token}` is used.")
                return {}

            list_token_c = await cls.get_valid_token_c()
            if auth_token in list_token_c:
                print(f"Token C `{auth_token}` is used.")
                return auth_token
        print(f"Token `{auth_token}` is not of type A or C.")
        return None

    @classmethod
    async def get_valid_token_a(cls):
        return ['test']

    @classmethod
    async def get_valid_token_c(cls):
        return ['test']


class Adapter:
    @classmethod
    def location_adapter(cls, data, version: VersionNumber) -> Location:
        return Location(**data)

    @classmethod
    async def get_valid_token_a(cls):
        return ['test']

    @classmethod
    async def get_valid_token_c(cls):
        return ['test']

    @classmethod
    async def authenticate_credentials(
        cls,
        auth_token: str,
    ):
        """Authenticate given auth token where both tokens valid."""
        if auth_token:
            list_token_a = await cls.get_valid_token_a()
            if auth_token in list_token_a:
                print(f"Token A `{auth_token}` is used.")
                return {}

            list_token_c = await cls.get_valid_token_c()
            if auth_token in list_token_c:
                print(f"Token C `{auth_token}` is used.")
                return auth_token
        print(f"Token `{auth_token}` is not of type A or C.")
        return None


app = get_application([VersionNumber.v_2_2_1], [enums.RoleEnum.cpo], Crud, [], Adapter, Authenticator)


handler = HubTopologyHandler(
    hub_url="https://roaming.staging.enapi.com/ocpi",
    party_id="ENA",
    country_code="DE",
    token="Mzc5Y2NiYjktOGIzZi00NTk2LTliOTctMThhYTY4NThlOTVl"
)


def handshake_with_hub():
    response = handler.handshake_with_hub()
    print(response)


if __name__ == '__main__':
    handshake_with_hub()
