from enum import Enum


class EnumTagTypeEnum(str, Enum):
    """Enumerated values for the different types of enumerated tag information.

    Attributes:
    """

    ASSET: str = "asset"
    ASSET_CONTRACTS: str = "asset.contracts"
    NETWORK: str = "network"
    PROTOCOL: str = "protocol"
