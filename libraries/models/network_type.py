from enum import Enum

from pydantic import BeforeValidator
from typing_extensions import Type, Annotated


class NetworkTypeEnum(str, Enum):
    """Enumerated values for the different types of blockchain networks.

    Attributes:
        MAINNET: enumerated value for mainnet.
        TESTNET: enumerated value for testnet.
    """

    MAINNET: str = "mainnet"
    TESTNET: str = "testnet"
    UNKNOWN: str = "unknown"


NetworkType: Type = Annotated[
    NetworkTypeEnum,
    BeforeValidator(lambda x: NetworkTypeEnum(x) if isinstance(x, str) else x),
]
"""A alias of :class:`NetworkTypeEnum`."""
