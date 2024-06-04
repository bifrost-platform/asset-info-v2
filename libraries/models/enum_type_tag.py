from enum import StrEnum
from typing import Self

from libraries.models.templates.enum_type_model import EnumTypeModel


class _EnumTypeTagEnum(StrEnum):
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


class EnumTypeTag(EnumTypeModel[_EnumTypeTagEnum]):
    """An alias of `_EnumTagTypeEnum`."""

    @property
    def type(self) -> str:
        return "tags"

    @classmethod
    def ascending_list(cls) -> list[Self]:
        return [EnumTypeTag(enum_tag_type) for enum_tag_type in _EnumTypeTagEnum]

    @staticmethod
    def asset() -> Self:
        """Gets the enum type for asset.

        Returns:
            The enum type for asset.
        """
        return EnumTypeTag(_EnumTypeTagEnum.ASSET)

    @staticmethod
    def asset_contracts() -> Self:
        """Gets the enum type for contracts in asset.

        Returns:
            The enum type for contracts in asset.
        """
        return EnumTypeTag(_EnumTypeTagEnum.ASSET_CONTRACTS)

    @staticmethod
    def network() -> Self:
        """Gets the enum type for network.

        Returns:
            The enum type for network.
        """
        return EnumTypeTag(_EnumTypeTagEnum.NETWORK)

    @staticmethod
    def protocol() -> Self:
        """Gets the enum type for protocol.

        Returns:
            The enum type for protocol.
        """
        return EnumTypeTag(_EnumTypeTagEnum.PROTOCOL)
