from enum import Enum

from libraries.models.info_category import InfoCategoryEnum


class EnumIdTypeEnum(str, Enum):
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

    @staticmethod
    def get_enum_type(info_category: InfoCategoryEnum) -> "EnumIdTypeEnum":
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
                return EnumIdTypeEnum.ASSET
            case InfoCategoryEnum.NETWORK:
                return EnumIdTypeEnum.NETWORK
            case InfoCategoryEnum.PROTOCOL:
                return EnumIdTypeEnum.PROTOCOL
            case _:
                raise ValueError(f"Unknown info category: {info_category}")
