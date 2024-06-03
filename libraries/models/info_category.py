from enum import StrEnum
from pathlib import Path
from typing import Type

from libraries.models.asset import Asset as AssetModel
from libraries.models.enum_id_type import EnumIdType
from libraries.models.network import Network as NetworkModel
from libraries.models.protocol import Protocol as ProtocolModel
from libraries.utils.file import PWD, get_model_info, search
from libraries.utils.model import CamelCaseModel, EnumModel


class _InfoCategoryEnum(StrEnum):
    """Enumerated values for the different categories of information.

    Attributes:
        ASSET: enumerated value for asset information.
        NETWORK: enumerated value for network information.
        PROTOCOL: enumerated value for protocol information.
    """

    ASSET = "assets"
    NETWORK = "networks"
    PROTOCOL = "protocols"


class InfoCategory(EnumModel[_InfoCategoryEnum]):
    """An alias of `_InfoCategoryEnum`."""

    @property
    def is_asset(self) -> bool:
        """Checks if the information category is asset.

        Returns:
            True if the information category is asset, False otherwise.
        """
        return self.root == _InfoCategoryEnum.ASSET

    @property
    def is_network(self) -> bool:
        """Checks if the information category is network.

        Returns:
            True if the information category is network, False otherwise.
        """
        return self.root == _InfoCategoryEnum.NETWORK

    @property
    def is_protocol(self) -> bool:
        """Checks if the information category is protocol.

        Returns:
            True if the information category is protocol, False otherwise.
        """
        return self.root == _InfoCategoryEnum.PROTOCOL

    @property
    def model_type(self) -> Type:
        """Gets the model type from the information category.

        Returns:
            The model type.
        """
        match self.root:
            case _InfoCategoryEnum.ASSET:
                return AssetModel
            case _InfoCategoryEnum.NETWORK:
                return NetworkModel
            case _InfoCategoryEnum.PROTOCOL:
                return ProtocolModel
            case _:
                raise ValueError(f"Unknown information category: {self}")

    @classmethod
    def ascending_list(cls) -> list["EnumModel"]:
        return [InfoCategory(info_category) for info_category in _InfoCategoryEnum]

    @staticmethod
    def asset() -> "InfoCategory":
        """Gets the information category for asset.

        Returns:
            The information category for asset.
        """
        return InfoCategory(_InfoCategoryEnum.ASSET)

    @staticmethod
    def network() -> "InfoCategory":
        """Gets the information category for network.

        Returns:
            The information category for network.
        """
        return InfoCategory(_InfoCategoryEnum.NETWORK)

    @staticmethod
    def protocol() -> "InfoCategory":
        """Gets the information category for protocol.

        Returns:
            The information category for protocol.
        """
        return InfoCategory(_InfoCategoryEnum.PROTOCOL)

    @staticmethod
    def get_info_category(model_type: Type[CamelCaseModel]) -> "InfoCategory":
        if model_type == AssetModel:
            return InfoCategory.asset()
        elif model_type == NetworkModel:
            return InfoCategory.network()
        elif model_type == ProtocolModel:
            return InfoCategory.protocol()
        else:
            raise ValueError(f"Unknown model type: {model_type}")

    def get_enum_type(self) -> EnumIdType:
        """Gets the enum type from the information category.

        Returns:
            The enum type.

        Raises:
            ValueError: If the information category is unknown.
        """
        match self.root:
            case _InfoCategoryEnum.ASSET:
                return EnumIdType.asset()
            case _InfoCategoryEnum.NETWORK:
                return EnumIdType.network()
            case _InfoCategoryEnum.PROTOCOL:
                return EnumIdType.protocol()
            case _:
                raise ValueError(f"Unknown information category: {self}")

    def get_model_dir_path(self) -> Path:
        """Gets the model directory from the information category.

        Returns:
            The model directory.
        """
        return PWD.joinpath(self.root)

    def get_model_info_list[T](self) -> list[tuple[T, Path]]:
        """Reads the enum information from the given enum tag type.

        Returns:
            The enum information.
        """
        return [
            get_model_info(self.model_type, file)
            for file in search(self.get_model_dir_path(), r"^info\.json$")
        ]
