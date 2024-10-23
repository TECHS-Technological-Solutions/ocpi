from enum import Enum


class DayOfWeek(str, Enum):
    """
    https://github.com/ocpi/ocpi/blob/2.2.1/mod_tariffs.asciidoc#141-dayofweek-enum
    """
    monday = "MONDAY"
    tuesday = "TUESDAY"
    wednesday = "WEDNESDAY"
    thursday = "THURSDAY"
    friday = "FRIDAY"
    saturday = "SATURDAY"
    sunday = "SUNDAY"
