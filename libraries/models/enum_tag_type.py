from enum import Enum
from typing import Type, Annotated

from pydantic import BeforeValidator, RootModel


class _EnumTagTypeEnum(str, Enum):
    """Enumerated values for the different types of enumerated tag information.

    Attributes:
        ASSET: enumerated value for asset.
        ASSET_CONTRACTS: enumerated value for contracts in asset.
        NETWORK: enumerated value for network.
        PROTOCOL: enumerated value for protocol.
    """

    ASSET: str = "asset"
    ASSET_CONTRACTS: str = "asset.contracts"
    NETWORK: str = "network"
    PROTOCOL: str = "protocol"


__EnumTagTypeType: Type = Annotated[
    _EnumTagTypeEnum,
    BeforeValidator(lambda x: _EnumTagTypeEnum(x) if isinstance(x, str) else x),
]
"""An annotated type for the type of enumerated tag information."""


class EnumTagType(RootModel[__EnumTagTypeType]):
    """An alias of `_EnumTagTypeEnum`."""

    @property
    def value(self) -> str:
        """Gets the value of the enum type.

        Returns:
            The value of the enum type.
        """
        return self.root.value

    @staticmethod
    def asset() -> "EnumTagType":
        """Gets the enum type for asset.

        Returns:
            The enum type for asset.
        """
        return EnumTagType(_EnumTagTypeEnum.ASSET)

    @staticmethod
    def asset_contracts() -> "EnumTagType":
        """Gets the enum type for contracts in asset.

        Returns:
            The enum type for contracts in asset.
        """
        return EnumTagType(_EnumTagTypeEnum.ASSET_CONTRACTS)

    @staticmethod
    def network() -> "EnumTagType":
        """Gets the enum type for network.

        Returns:
            The enum type for network.
        """
        return EnumTagType(_EnumTagTypeEnum.NETWORK)

    @staticmethod
    def protocol() -> "EnumTagType":
        """Gets the enum type for protocol.

        Returns:
            The enum type for protocol.
        """
        return EnumTagType(_EnumTagTypeEnum.PROTOCOL)
