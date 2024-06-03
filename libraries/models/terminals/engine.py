from enum import StrEnum
from typing import Self

from libraries.models.templates.enum_model import EnumModel


class _EngineEnum(StrEnum):
    """Enumerated values for the different engines of a blockchain network.

    Attributes:
        EVM: Ethereum Virtual Machine (EVM) Engine.
        UNKNOWN: Unknown engine.
    """

    EVM: str = "evm"
    UNKNOWN: str = "unknown"


class Engine(EnumModel[_EngineEnum]):
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

    @classmethod
    def ascending_list(cls) -> list[Self]:
        return [Engine(engine) for engine in _EngineEnum]
