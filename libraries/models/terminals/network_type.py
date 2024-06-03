from enum import StrEnum
from typing import Self

from libraries.models.templates.enum_model import EnumModel


class _NetworkTypeEnum(StrEnum):
    """Enumerated values for the different types of blockchain networks.

    Attributes:
        MAINNET: enumerated value for mainnet.
        TESTNET: enumerated value for testnet.
        UNKNOWN: enumerated value for unknown network.
    """

    MAINNET: str = "mainnet"
    TESTNET: str = "testnet"
    UNKNOWN: str = "unknown"


class NetworkType(EnumModel[_NetworkTypeEnum]):
    """An alias of `_NetworkTypeEnum`."""

    @property
    def is_mainnet(self) -> bool:
        """Checks if the network type is mainnet.

        Returns:
            True if the network type is mainnet, False otherwise.
        """
        return self.root == _NetworkTypeEnum.MAINNET

    @property
    def is_testnet(self) -> bool:
        """Checks if the network type is testnet.

        Returns:
            True if the network type is testnet, False otherwise.
        """
        return self.root == _NetworkTypeEnum.TESTNET

    @property
    def is_unknown(self) -> bool:
        """Checks if the network type is unknown.

        Returns:
            True if the network type is unknown, False otherwise.
        """
        return self.root == _NetworkTypeEnum.UNKNOWN

    @classmethod
    def ascending_list(cls) -> list[Self]:
        return [NetworkType(network_type) for network_type in _NetworkTypeEnum]
