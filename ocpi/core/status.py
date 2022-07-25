"""
OCPI status codes based on https://github.com/ocpi/ocpi/blob/2.2.1/status_codes.asciidoc
"""

# 1xxx: Success
OCPI_1000_GENERIC_SUCESS_CODE = {
    'status_code': 1000,
    'status_message': 'Generic success code'
}

# 2xxx: Client errors
OCPI_2000_GENERIC_CLIENT_ERROR = {
    'status_code': 2000,
    'status_message': 'Generic client error'
}
OCPI_2001_INVALID_OR_MISSING_PARAMETERS = {
    'status_code': 2001,
    'status_message': 'Invalid or missing parameters'
}
OCPI_2002_NOT_ENOUGH_INFORMATION = {
    'status_code': 2002,
    'status_message': 'Not enough information'
}
OCPI_2003_UNKNOWN_LOCATION = {
    'status_code': 2003,
    'status_message': 'Unknown Location'
}
OCPI_2004_UNKNOWN_TOKEN = {
    'status_code': 2004,
    'status_message': 'Unknown Token'
}

# 3xxx: Server errors
OCPI_3000_GENERIC_SERVER_ERROR = {
    'status_code': 3000,
    'status_message': 'Generic server error'
}
OCPI_3001_UNABLE_TO_USE_CLIENTS_API = {
    'status_code': 3001,
    'status_message': 'Unable to use the client’s API'
}
OCPI_3002_UNSUPPORTED_VERSION = {
    'status_code': 3002,
    'status_message': 'Unsupported version'
}
OCPI_3003_NO_MATCHING_ENDPOINT = {
    'status_code': 3003,
    'status_message': 'No matching endpoints or expected endpoints missing between parties'
}

# 4xxx: Hub errors
OCPI_4000_GENERIC_ERROR = {
    'status_code': 4000,
    'status_message': 'Generic error'
}
OCPI_4001_UNKNOWN_RECEIVER = {
    'status_code': 4001,
    'status_message': 'Unknown receiver (TO address is unknown)'
}
OCPI_4002_TIMEOUT_ON_FORWARDED_REQUEST = {
    'status_code': 4002,
    'status_message': 'Timeout on forwarded request (message is forwarded, but request times out)'
}
OCPI_4003_CONNECTION_PROBLEM = {
    'status_code': 4003,
    'status_message': 'Connection problem (receiving party is not connected)'
}
