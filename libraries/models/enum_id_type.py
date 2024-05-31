from enum import StrEnum

from libraries.models.info_category import InfoCategoryEnum
from libraries.utils.model import EnumModel


class _EnumIdTypeEnum(StrEnum):
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


class EnumIdType(EnumModel[_EnumIdTypeEnum]):
    """An alias of `_EnumIdTypeEnum`."""

    @classmethod
    def ascending_list(cls) -> list["EnumModel"]:
        return [EnumIdType(enum_id_type) for enum_id_type in _EnumIdTypeEnum]

    @staticmethod
    def asset() -> "EnumIdType":
        """Gets the enum type for asset.

        Returns:
            The enum type for asset.
        """
        return EnumIdType(_EnumIdTypeEnum.ASSET)

    @staticmethod
    def asset_reference() -> "EnumIdType":
        """Gets the enum type for reference in asset.

        Returns:
            The enum type for reference in asset.
        """
        return EnumIdType(_EnumIdTypeEnum.ASSET_REFERENCE)

    @staticmethod
    def network() -> "EnumIdType":
        """Gets the enum type for network.

        Returns:
            The enum type for network.
        """
        return EnumIdType(_EnumIdTypeEnum.NETWORK)

    @staticmethod
    def network_explorer() -> "EnumIdType":
        """Gets the enum type for explorer in network.

        Returns:
            The enum type for explorer in network.
        """
        return EnumIdType(_EnumIdTypeEnum.NETWORK_EXPLORER)

    @staticmethod
    def protocol() -> "EnumIdType":
        """Gets the enum type for protocol.

        Returns:
            The enum type for protocol.
        """
        return EnumIdType(_EnumIdTypeEnum.PROTOCOL)

    @staticmethod
    def get_enum_type(info_category: InfoCategoryEnum) -> "EnumIdType":
        """Gets the enum type from the info category.

        Args:
            info_category: The info category.

        Returns:
            The enum type.

        Raises:
            ValueError: If the info category is unknown.
        """
        match info_category:
            case InfoCategoryEnum.ASSET:
                return EnumIdType.asset()
            case InfoCategoryEnum.NETWORK:
                return EnumIdType.network()
            case InfoCategoryEnum.PROTOCOL:
                return EnumIdType.protocol()
            case _:
                raise ValueError(f"Unknown info category: {info_category}")
