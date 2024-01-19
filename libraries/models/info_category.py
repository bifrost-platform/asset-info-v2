from enum import Enum
from typing import Type

from libraries.models.asset import Asset as AssetModel
from libraries.models.network import Network as NetworkModel
from libraries.models.protocol import Protocol as ProtocolModel
from libraries.utils.model import CamelCaseModel


class InfoCategoryEnum(str, Enum):
    """Enumerated values for the different categories of information.

    Attributes:
        ASSET: enumerated value for asset information.
        NETWORK: enumerated value for network information.
        PROTOCOL: enumerated value for protocol information.
    """

    ASSET = "assets"
    NETWORK = "networks"
    PROTOCOL = "protocols"

    @staticmethod
    def get_info_category(model_type: Type[CamelCaseModel]) -> "InfoCategoryEnum":
        if model_type == AssetModel:
            return InfoCategoryEnum.ASSET
        elif model_type == NetworkModel:
            return InfoCategoryEnum.NETWORK
        elif model_type == ProtocolModel:
            return InfoCategoryEnum.PROTOCOL
        else:
            raise ValueError(f"Unknown model type: {model_type}")
