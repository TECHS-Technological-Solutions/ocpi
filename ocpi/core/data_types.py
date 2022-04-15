"""
OCPI data types based on https://github.com/ocpi/ocpi/blob/master/types.asciidoc
"""

from datetime import datetime


class CiString(str):
    """
    Case Insensitive String. Only printable ASCII allowed.
    (Non-printable characters like: Carriage returns, Tabs, Line breaks, etc are not allowed)
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=['string'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, str):
            raise TypeError('string required')
        if not v.isascii():
            raise ValueError('invalid cistring format')
        return cls(v)

    def __repr__(self):
        return f'CiString({super().__repr__()})'


class DateTime(datetime):
    """
    All timestamps are formatted as string(25) following RFC 3339, with some additional limitations.
    All timestamps SHALL be in UTC.
    The absence of the timezone designator implies a UTC timestamp.
    Fractional seconds MAY be used.
    """
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=[str(datetime.now())],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, datetime):
            raise TypeError('datetime required')
        format_string = '%Y-%m-%dT%H:%M:%S.%f%z'
        formated_v = datetime.strptime(v, format_string)
        return cls(formated_v)

    def __repr__(self):
        return f'DateTime({super().__repr__()})'


class DisplayText(dict):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(
            examples=['link:examples/type_displaytext_example.json[]'],
        )

    @classmethod
    def validate(cls, v):
        if not isinstance(v, dict):
            raise TypeError('dictionary required')
        if 'language' not in v:
            raise TypeError('language not specified')
        if 'text' not in v:
            raise TypeError('text required')
        if len(v['text']) > 512:
            raise TypeError('text too long')
        return cls(v)

    def __repr__(self):
        return f'DateTime({super().__repr__()})'
