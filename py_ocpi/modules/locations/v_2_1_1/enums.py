from py_ocpi.modules.locations.enums import *  # noqa


class LocationType(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#416-locationtype-enum
    """

    # Parking in public space.
    on_street = "ON_STREET"
    # Multistorey car park.
    parking_garage = "PARKING_GARAGE"
    # Multistorey car park, mainly underground.
    underground_garage = "UNDERGROUND_GARAGE"
    # A cleared area that is intended for parking vehicles, i.e. at super
    # markets, bars, etc.
    parking_lot = "PARKING_LOT"
    # None of the given possibilities.
    other = "OTHER"
    # Parking location type is not known by the operator (default).
    unknown = "UNKNOWN"


class Facility(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#411-facility-enum
    """

    # A hotel.
    hotel = "HOTEL"
    # A restaurant.
    restaurant = "RESTAURANT"
    # A cafe.
    cafe = "CAFE"
    # A mall or shopping center.
    mall = "MALL"
    # A supermarket.
    supermarket = "SUPERMARKET"
    # Sport facilities: gym, field etc.
    sport = "SPORT"
    # A recreation area.
    recreation_area = "RECREATION_AREA"
    # Located in, or close to, a park, nature reserve etc.
    nature = "NATURE"
    # A museum.
    museum = "MUSEUM"
    # A bus stop.
    bus_stop = "BUS_STOP"
    # A taxi stand.
    taxi_stand = "TAXI_STAND"
    # A train station.
    train_station = "TRAIN_STATION"
    # An airport.
    airport = "AIRPORT"
    # A carpool parking.
    carpool_parking = "CARPOOL_PARKING"
    # A Fuel station.
    fuel_station = "FUEL_STATION"
    # Wifi or other type of internet available.
    wifi = "WIFI"


class Capability(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#42-capability-enum
    """

    # The EVSE supports charging profiles. Sending Charging Profiles
    # is not yet supported by OCPI.
    charging_profile_capable = "CHARGING_PROFILE_CAPABLE"
    # Charging at this EVSE can be payed with credit card.
    credit_card_payable = "CREDIT_CARD_PAYABLE"
    # The EVSE can remotely be started/stopped.
    remote_start_stop_capable = "REMOTE_START_STOP_CAPABLE"
    # The EVSE can be reserved.
    reservable = "RESERVABLE"
    # Charging at this EVSE can be authorized with a RFID token
    rfid_reader = "RFID_READER"
    # Connectors have mechanical lock that can be requested by the eMSP
    # to be unlocked.
    unlock_capable = "UNLOCK_CAPABLE"


class ConnectorType(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#44-connectortype-enum
    """

    # The connector type is CHAdeMO, DC
    chademo = "CHADEMO"
    # Standard/Domestic household, type "A", NEMA 1-15, 2 pins
    domestic_a = "DOMESTIC_A"
    # Standard/Domestic household, type "B", NEMA 5-15, 3 pins
    domestic_b = "DOMESTIC_B"
    # Standard/Domestic household, type "C", CEE 7/17, 2 pins
    domestic_c = "DOMESTIC_C"
    # Standard/Domestic household, type "D", 3 pin
    domestic_d = "DOMESTIC_D"
    # Standard/Domestic household, type "E", CEE 7/5 3 pins
    domestic_e = "DOMESTIC_E"
    # Standard/Domestic household, type "F", CEE 7/4, Schuko, 3 pins
    domestic_f = "DOMESTIC_F"
    # Standard/Domestic household, type "G", BS 1363, Commonwealth, 3 pins
    domestic_g = "DOMESTIC_G"
    # Standard/Domestic household, type "H", SI-32, 3 pins
    domestic_h = "DOMESTIC_H"
    # Standard/Domestic household, type "I", AS 3112, 3 pins
    domestic_i = "DOMESTIC_I"
    # Standard/Domestic household, type "J", SEV 1011, 3 pins
    domestic_j = "DOMESTIC_J"
    # Standard/Domestic household, type "K", DS 60884-2-D1, 3 pins
    domestic_k = "DOMESTIC_K"
    # Standard/Domestic household, type "L", CEI 23-16-VII, 3 pins
    domestic_l = "DOMESTIC_L"
    # IEC 60309-2 Industrial Connector single phase 16 amperes (usually blue)
    iec_60309_2_single_16 = "IEC_60309_2_single_16"
    # IEC 60309-2 Industrial Connector three phases 16 amperes (usually red)
    iec_60309_2_three_16 = "IEC_60309_2_three_16"
    # IEC 60309-2 Industrial Connector three phases 32 amperes (usually red)
    iec_60309_2_three_32 = "IEC_60309_2_three_32"
    # IEC 60309-2 Industrial Connector three phases 64 amperes (usually red)
    iec_60309_2_three_64 = "IEC_60309_2_three_64"
    # IEC 62196 Type 1 "SAE J1772"
    iec_62196_t1 = "IEC_62196_T1"
    # Combo Type 1 based, DC
    iec_62196_t1_combo = "IEC_62196_T1_COMBO"
    # IEC 62196 Type 2 "Mennekes"
    iec_62196_t2 = "IEC_62196_T2"
    # Combo Type 2 based, DC
    iec_62196_t2_combo = "IEC_62196_T2_COMBO"
    # IEC 62196 Type 3A
    iec_62196_t3a = "IEC_62196_T3A"
    # IEC 62196 Type 3C "Scame"
    iec_62196_t3c = "IEC_62196_T3C"
    # Tesla Connector "Roadster"-type (round, 4 pin)
    tesla_r = "TESLA_R"
    # Tesla Connector "Model-S"-type (oval, 5 pin)
    tesla_s = "TESLA_S"


class PowerType(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/release-2.1.1-bugfixes/mod_locations.md#418-powertype-enum
    """

    # AC single phase.
    ac_1_phase = "AC_1_PHASE"
    # AC three phases.
    ac_3_phase = "AC_3_PHASE"
    # Direct Current.
    dc = "DC"
