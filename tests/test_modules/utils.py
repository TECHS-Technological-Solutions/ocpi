from uuid import uuid4

from py_ocpi.core.authentication.authenticator import Authenticator
from py_ocpi.core.utils import encode_string_base64

AUTH_TOKEN = str(uuid4())
AUTH_TOKEN_A = str(uuid4())
RANDOM_AUTH_TOKEN = str(uuid4())

AUTH_TOKEN_V_2_2_1 = str(uuid4())
AUTH_TOKEN_A_V_2_2_1 = str(uuid4())
RANDOM_AUTH_TOKEN_V_2_2_1 = str(uuid4())
ENCODED_AUTH_TOKEN = encode_string_base64(AUTH_TOKEN_V_2_2_1)
ENCODED_AUTH_TOKEN_A = encode_string_base64(AUTH_TOKEN_A_V_2_2_1)
ENCODED_RANDOM_AUTH_TOKEN = encode_string_base64(RANDOM_AUTH_TOKEN_V_2_2_1)


class ClientAuthenticator(Authenticator):
    @classmethod
    async def get_valid_token_c(cls):
        """Return a list of valid tokens."""
        return [AUTH_TOKEN, AUTH_TOKEN_V_2_2_1]

    @classmethod
    async def get_valid_token_a(cls):
        """Return a list of valid tokens."""
        return [AUTH_TOKEN_A, AUTH_TOKEN_A_V_2_2_1]
