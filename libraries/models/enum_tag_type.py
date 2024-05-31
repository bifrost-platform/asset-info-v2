from enum import StrEnum

from libraries.models.enum_info import EnumTypeModel
from libraries.utils.model import EnumModel


class _EnumTagTypeEnum(StrEnum):
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


class EnumTagType(EnumTypeModel[_EnumTagTypeEnum]):
    """An alias of `_EnumTagTypeEnum`."""

    @property
    def type(self) -> str:
        return "tags"

    @classmethod
    def ascending_list(cls) -> list["EnumModel"]:
        return [EnumTagType(enum_tag_type) for enum_tag_type in _EnumTagTypeEnum]

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
