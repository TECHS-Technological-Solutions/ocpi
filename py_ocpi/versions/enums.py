from enum import Enum


class VersionNumber(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#125-versionnumber-enum
    """
    v_2_0 = '2.0'
    v_2_1 = '2.1'
    v_2_1_1 = '2.1.1'
    v_2_2 = '2.2'
    v_2_2_1 = '2.2.1'


class InterfaceRole(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#123-interfacerole-enum
    """
    # Sender Interface implementation.
    # Interface implemented by the owner of data,
    # so the Receiver can Pull information from the data Sender/owner.
    sender = 'SENDER'
    # Receiver Interface implementation.
    # Interface implemented by the receiver of data,
    # so the Sender/owner can Push information to the Receiver.
    receiver = 'RECEIVER'
