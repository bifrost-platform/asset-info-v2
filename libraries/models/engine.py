from enum import Enum

from pydantic import BeforeValidator
from typing_extensions import Type, Annotated


class EngineEnum(str, Enum):
    """Enumerated values for the different engines of a blockchain network.

    Attributes:
        EVM: Ethereum Virtual Machine (EVM) Engine.
    """

    EVM: str = "evm"
    UNKNOWN: str = "unknown"


Engine: Type = Annotated[
    EngineEnum, BeforeValidator(lambda x: EngineEnum(x) if isinstance(x, str) else x)
]
"""A alias of :class:`EngineEnum`."""
