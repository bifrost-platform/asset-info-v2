from enum import Enum
from typing import Annotated, Type

from pydantic import BeforeValidator, RootModel


class _EngineEnum(str, Enum):
    """Enumerated values for the different engines of a blockchain network.

    Attributes:
        EVM: Ethereum Virtual Machine (EVM) Engine.
        UNKNOWN: Unknown engine.
    """

    EVM: str = "evm"
    UNKNOWN: str = "unknown"


__EngineType: Type = Annotated[
    _EngineEnum,
    BeforeValidator(lambda x: _EngineEnum(x) if isinstance(x, str) else x),
]
"""An annotated type for the engine of a blockchain network."""


class Engine(RootModel[__EngineType]):
    """An alias of `_EngineEnum`."""

    @property
    def is_evm(self) -> bool:
        """Check if the engine is an EVM engine.

        Returns:
            Whether the engine is an EVM engine.
        """
        return self.root == _EngineEnum.EVM

    @property
    def is_unknown(self) -> bool:
        """Check if the engine is an unknown engine.

        Returns:
            Whether the engine is an unknown engine.
        """
        return self.root == _EngineEnum.UNKNOWN
