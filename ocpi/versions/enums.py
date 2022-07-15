from enum import Enum


class VersionNumber(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/master/version_information_endpoint.asciidoc#125-versionnumber-enum
    """
    _2_0 = '2.0'
    _2_1 = '2.1'
    _2_1_1 = '2.1.1'
    _2_2 = '2.2'
    _2_2_1 = '2.2.1'


class InterfaceRole(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/master/version_information_endpoint.asciidoc#123-interfacerole-enum
    """
    # Sender Interface implementation.
    # Interface implemented by the owner of data,
    # so the Receiver can Pull information from the data Sender/owner.
    Sender = 'SENDER'
    # Receiver Interface implementation.
    # Interface implemented by the receiver of data,
    # so the Sender/owner can Push information to the Receiver.
    Receiver = 'RECEIVER'
