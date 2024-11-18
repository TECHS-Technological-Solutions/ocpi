from enum import Enum


class ParkingRestriction(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#417-parkingrestriction-enum
    """

    # Reserved parking spot for electric vehicles.
    ev_only = "EV_ONLY"
    # Parking is only allowed while plugged in (charging).
    plugged = "PLUGGED"
    # Reserved parking spot for disabled people with valid ID.
    disables = "DISABLED"
    # Parking spot for customers/guests only,
    # for example in case of a hotel or shop.
    customers = "CUSTOMERS"
    # Parking spot only suitable for (electric) motorcycles or scooters.
    motorcycle = "MOTORCYCLES"


class Status(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#420-status-enum
    """

    # The EVSE/Connector is able to start a new charging session.
    available = "AVAILABLE"
    # The EVSE/Connector is not accessible
    # because of a physical barrier, i.e. a car.
    blocked = "BLOCKED"
    # The EVSE/Connector is in use.
    charging = "CHARGING"
    # The EVSE/Connector is not yet active,
    # or temporarily not available for use, but not broken or defect.
    inoperative = "INOPERATIVE"
    # The EVSE/Connector is currently out of order,
    # some part/components may be broken/defect.
    outoforder = "OUTOFORDER"
    # The EVSE/Connector is planned, will be operating soon.
    planned = "PLANNED"
    # The EVSE/Connector was discontinued/removed.
    removed = "REMOVED"
    # The EVSE/Connector is reserved for a particular EV driver
    # and is unavailable for other drivers.
    reserved = "RESERVED"
    # No status information available (also used when offline).
    unknown = "UNKNOWN"


class ConnectorFormat(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#144-connectorformat-enum
    """

    # The connector is a socket; the EV user needs to bring a fitting plug.
    socket = "SOCKET"
    # The connector is an attached cable;
    # the EV users car needs to have a fitting inlet.
    cable = "CABLE"


class ImageCategory(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#415-imagecategory-enum
    """

    # Photo of the physical device that contains one or more EVSEs.
    charger = "CHARGER"
    # Location entrance photo. Should show the car entrance
    # to the location from street side.
    entrance = "ENTRANCE"
    # Location overview photo.
    location = "LOCATION"
    # Logo of an associated roaming network to be displayed
    # with the EVSE for example in lists,
    # maps and detailed information views.
    network = "NETWORK"
    # Logo of the charge point operator, for example a municipality,
    # to be displayed in the EVSEs detailed information
    # view or in lists and maps, if no network logo is present.
    operator = "OPERATOR"
    # Other
    other = "OTHER"
    # Logo of the charge point owner, for example a local store,
    # to be displayed in the EVSEs detailed information view.
    owner = "OWNER"


class EnergySourceCategory(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#148-energysourcecategory-enum
    """

    # Nuclear power sources.
    nuclear = "NUCLEAR"
    # All kinds of fossil power sources.
    general_fossil = "GENERAL_FOSSIL"
    # Fossil power from coal.
    coal = "COAL"
    # Fossil power from gas.
    gas = "GAS"
    # All kinds of regenerative power sources.
    general_green = "GENERAL_GREEN"
    # Regenerative power from PV.
    solar = "SOLAR"
    # Regenerative power from wind turbines.
    wind = "WIND"
    # Regenerative power from water turbines.
    water = "WATER"


class EnvironmentalImpactCategory(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1410-environmentalimpactcategory-enum
    """

    # Produced nuclear waste in grams per kilowatthour.
    nuclear_waste = "NUCLEAR_WASTE"
    # Exhausted carbon dioxide in grams per kilowatthour.
    carbon_dioxide = "CARBON_DIOXIDE"
