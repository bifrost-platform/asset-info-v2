from enum import Enum
from typing import Type, Annotated

from pydantic import BeforeValidator


class EnumTypeEnum(str, Enum):
    """Enumerated values for the different types of enumerated information.

    Attributes:
        ID: enumerated value for ID.
        TAG: enumerated value for tag.
    """

    ID: str = "ids"
    TAG: str = "tags"


EnumType: Type = Annotated[
    EnumTypeEnum,
    BeforeValidator(lambda x: EnumTypeEnum(x) if isinstance(x, str) else x),
]
"""A alias of :class:`EnumTypeEnum`."""
