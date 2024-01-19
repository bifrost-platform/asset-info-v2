from enum import Enum
from typing import Type, Annotated

from pydantic import BeforeValidator


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
