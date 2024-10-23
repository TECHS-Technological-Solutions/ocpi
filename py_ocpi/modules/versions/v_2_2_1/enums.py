from py_ocpi.modules.versions.enums import *  # noqa


class InterfaceRole(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/version_information_endpoint.asciidoc#123-interfacerole-enum
    """

    # Sender Interface implementation.
    # Interface implemented by the owner of data,
    # so the Receiver can Pull information from the data Sender/owner.
    sender = "SENDER"
    # Receiver Interface implementation.
    # Interface implemented by the receiver of data,
    # so the Sender/owner can Push information to the Receiver.
    receiver = "RECEIVER"
