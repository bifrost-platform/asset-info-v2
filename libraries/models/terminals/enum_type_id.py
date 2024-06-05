from enum import StrEnum
from typing import Self

from libraries.models.abstractions.enum_type_model import EnumTypeModel


class _EnumTypeIdEnum(StrEnum):
    """Enumerated values for the different types of enumerated ID information.

    Attributes:
        ASSET: enumerated value for asset.
        ASSET_REFERENCE: enumerated value for reference in asset.
        NETWORK: enumerated value for network.
        NETWORK_EXPLORER: enumerated value for explorer in network.
        PROTOCOL: enumerated value for protocol.
    """

    ASSET: str = "asset"
    ASSET_REFERENCE: str = "asset.reference"
    NETWORK: str = "network"
    NETWORK_EXPLORER: str = "network.explorer"
    PROTOCOL: str = "protocol"


class EnumTypeId(EnumTypeModel[_EnumTypeIdEnum]):
    """An alias of `_EnumIdTypeEnum`."""

    @property
    def type(self) -> str:
        return "ids"

    @classmethod
    def ascending_list(cls) -> list[Self]:
        return [EnumTypeId(enum_id_type) for enum_id_type in _EnumTypeIdEnum]

    @staticmethod
    def asset() -> Self:
        """Gets the enum type for asset.

        Returns:
            The enum type for asset.
        """
        return EnumTypeId(_EnumTypeIdEnum.ASSET)

    @staticmethod
    def asset_reference() -> Self:
        """Gets the enum type for reference in asset.

        Returns:
            The enum type for reference in asset.
        """
        return EnumTypeId(_EnumTypeIdEnum.ASSET_REFERENCE)

    @staticmethod
    def network() -> Self:
        """Gets the enum type for network.

        Returns:
            The enum type for network.
        """
        return EnumTypeId(_EnumTypeIdEnum.NETWORK)

    @staticmethod
    def network_explorer() -> Self:
        """Gets the enum type for explorer in network.

        Returns:
            The enum type for explorer in network.
        """
        return EnumTypeId(_EnumTypeIdEnum.NETWORK_EXPLORER)

    @staticmethod
    def protocol() -> Self:
        """Gets the enum type for protocol.

        Returns:
            The enum type for protocol.
        """
        return EnumTypeId(_EnumTypeIdEnum.PROTOCOL)
