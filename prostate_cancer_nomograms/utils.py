import enum
from typing import Union


class ExtendedEnum(enum.Enum):

    @classmethod
    def list(cls):
        return list(map(lambda c: c.value, cls))
