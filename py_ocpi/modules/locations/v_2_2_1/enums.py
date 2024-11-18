from py_ocpi.modules.locations.enums import *  # noqa


class ParkingType(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1418-parkingtype-enum
    """
    # Location on a parking facility/rest area
    # along a motorway, freeway, interstate, highway etc.
    along_motorway = "ALONG_MOTORWAY"
    # Multistorey car park.
    parking_garage = "PARKING_GARAGE"
    # A cleared area that is intended
    # for parking vehicles, i.e. at super markets, bars, etc.
    parking_lot = "PARKING_LOT"
    # Location is on the driveway of a house/building.
    on_driveway = "ON_DRIVEWAY"
    # Parking in public space along a street.
    on_street = "ON_STREET"
    # Multistorey car park, mainly underground.
    underground_garage = "UNDERGROUND_GARAGE"


class Facility(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1412-facility-enum
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
    # A bike/e-bike/e-scooter sharing location.
    bike_sharing = "BIKE_SHARING"
    # A bus stop.
    bus_stop = "BUS_STOP"
    # A taxi stand.
    taxi_stand = "TAXI_STAND"
    # A tram stop/station.
    tram_shop = "TRAM_STOP"
    # A metro station.
    metro_station = "METRO_STATION"
    # A train station.
    train_station = "TRAIN_STATION"
    # An airport.
    airport = "AIRPORT"
    # A parking lot.
    parking_lot = "PARKING_LOT"
    # A carpool parking.
    carpool_parking = "CARPOOL_PARKING"
    # A Fuel station.
    fuel_station = "FUEL_STATION"
    # Wifi or other type of internet available.
    wifi = "WIFI"


class Capability(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#143-capability-enum
    """
    # The EVSE supports charging profiles.
    charging_profile_capable = "CHARGING_PROFILE_CAPABLE"
    # The EVSE supports charging preferences.
    charging_preferences_capable = "CHARGING_PREFERENCES_CAPABLE"
    # EVSE has a payment terminal that supports chip cards.
    chip_card_support = "CHIP_CARD_SUPPORT"
    # EVSE has a payment terminal that supports contactless cards.
    contactless_card_support = "CONTACTLESS_CARD_SUPPORT"
    # EVSE has a payment terminal
    # that makes it possible to pay for charging using a credit card.
    credit_card_payable = "CREDIT_CARD_PAYABLE"
    # EVSE has a payment terminal
    # that makes it possible to pay for charging using a debit card.
    debit_card_payable = "DEBIT_CARD_PAYABLE"
    # EVSE has a payment terminal with a pin-code entry device.
    ped_terminal = "PED_TERMINAL"
    # The EVSE can remotely be started/stopped.
    remote_start_stop_capable = "REMOTE_START_STOP_CAPABLE"
    # The EVSE can be reserved.
    reservable = "RESERVABLE"
    # Charging at this EVSE can be authorized with an RFID token.
    rfid_reader = "RFID_READER"
    # When a StartSession is sent to this EVSE, the MSP is required to add
    # the optional connector_id field in the StartSession object.
    start_session_connector_required = "START_SESSION_CONNECTOR_REQUIRED"
    # This EVSE supports token groups, two or more tokens work as one,
    # so that a session can be started with one token and stopped with another
    # (handy when a card and key-fob are given to the EV-driver).
    token_group_capable = "TOKEN_GROUP_CAPABLE"  # nosec
    # Connectors have mechanical lock that
    # can be requested by the eMSP to be unlocked.
    unlook_capable = "UNLOCK_CAPABLE"


class ConnectorType(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#145-connectortype-enum
    """
    # The connector type is CHAdeMO, DC
    chademo = "CHADEMO"
    # The ChaoJi connector. The new generation charging connector,
    # harmonized between CHAdeMO and GB/T. DC.
    chaoji = "CHAOJI"
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
    # Standard/Domestic household, type "M", BS 546, 3 pins
    domestic_m = "DOMESTIC_M"
    # Standard/Domestic household, type "N", NBR 14136, 3 pins
    domestic_n = "DOMESTIC_N"
    # Standard/Domestic household, type "O", TIS 166-2549, 3 pins
    domestic_o = "DOMESTIC_O"
    # Guobiao GB/T 20234.2 AC socket/connector
    gbt_ac = "GBT_AC"
    # Guobiao GB/T 20234.3 DC connector
    gbt_dc = "GBT_DC"
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
    # NEMA 5-20, 3 pins
    nema_5_20 = "NEMA_5_20"
    # NEMA 6-30, 3 pins
    nema_6_30 = "NEMA_6_30"
    # NEMA 6-50, 3 pins
    nema_6_50 = "NEMA_6_50"
    # NEMA 10-30, 3 pins
    nema_10_30 = "NEMA_10_30"
    # NEMA 10-50, 3 pins
    nema_10_50 = "NEMA_10_50"
    # NEMA 14-30, 3 pins, rating of 30 A
    nema_14_30 = "NEMA_14_30"
    # NEMA 14-50, 3 pins, rating of 50 A
    nema_14_50 = "NEMA_14_50"
    # On-board Bottom-up-Pantograph typically for bus charging
    pantograph_bottom_up = "PANTOGRAPH_BOTTOM_UP"
    # Off-board Top-down-Pantograph typically for bus charging
    pantograph_top_down = "PANTOGRAPH_TOP_DOWN"
    # Tesla Connector "Roadster"-type (round, 4 pin)
    tesla_r = "TESLA_R"
    # Tesla Connector "Model-S"-type (oval, 5 pin)
    tesla_s = "TESLA_S"


class PowerType(str, Enum):  # noqa
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_locations.asciidoc#1419-powertype-enum
    """

    # AC single phase.
    ac_1_phase = "AC_1_PHASE"
    # AC two phases, only two of the three available phases connected.
    ac_2_phase = "AC_2_PHASE"
    # AC two phases using split phase system.
    ac_2_phase_split = "AC_2_PHASE_SPLIT"
    # AC three phases.
    ac_3_phase = "AC_3_PHASE"
    # Direct Current.
    dc = "DC"
