from enum import Enum


class DayOfWeek(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#141-dayofweek-enum
    """
    monday = 'MONDAY'
    tuesday = 'TUESDAY'
    wednesday = 'WEDNESDAY'
    thursday = 'THURSDAY'
    friday = 'FRIDAY'
    saturday = 'SATURDAY'
    sunday = 'SUNDAY'


class ReservationRestrictionType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#143-reservationrestrictiontype-enum
    """
    # Used in TariffElements to describe costs for a reservation.
    reservation = 'RESERVATION'
    # Used in TariffElements to describe costs for a reservation that expires
    # (i.e. driver does not start a charging session before expiry_date of the reservation).
    reservation_expires = 'RESERVATION_EXPIRES'


class TariffDimensionType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#145-tariffdimensiontype-enum
    """
    # Defined in kWh, step_size multiplier: 1 Wh
    energy = 'ENERGY'
    # Flat fee without unit for step_size
    flat = 'FLAT'
    # Time not charging: defined in hours, step_size multiplier: 1 second
    parking_time = 'PARKING_TIME'
    # Time charging: defined in hours, step_size multiplier: 1 second
    # Can also be used in combination with a RESERVATION restriction to describe the price of the reservation time.
    time = 'TIME'


class TariffType(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#147-tarifftype-enum
    """
    # Used to describe that a Tariff is valid when ad-hoc payment is used at the Charge Point
    # (for example: Debit or Credit card payment terminal).
    ad_hoc_payment = 'AD_HOC_PAYMENT'
    # Used to describe that a Tariff is valid when Charging Preference: CHEAP is set for the session.
    profile_cheap = 'PROFILE_CHEAP'
    # Used to describe that a Tariff is valid when Charging Preference: FAST is set for the session.
    profile_fast = 'PROFILE_FAST'
    # Used to describe that a Tariff is valid when Charging Preference: GREEN is set for the session.
    profile_green = 'PROFILE_GREEN'
    # Used to describe that a Tariff is valid when using an RFID, without any Charging Preference,
    # or when Charging Preference: REGULAR is set for the session.
    regular = 'REGULAR'
