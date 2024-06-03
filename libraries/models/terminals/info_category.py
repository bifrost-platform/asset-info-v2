from enum import StrEnum
from pathlib import Path
from typing import Self

from libraries.models.terminals.enum_type_id import EnumTypeId
from libraries.models.templates.enum_model import EnumModel
from libraries.utils.file import PWD


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

    @classmethod
    def ascending_list(cls) -> list[Self]:
        return [InfoCategory(info_category) for info_category in _InfoCategoryEnum]

    @staticmethod
    def asset() -> Self:
        """Gets the information category for asset.

        Returns:
            The information category for asset.
        """
        return InfoCategory(_InfoCategoryEnum.ASSET)

    @staticmethod
    def network() -> Self:
        """Gets the information category for network.

        Returns:
            The information category for network.
        """
        return InfoCategory(_InfoCategoryEnum.NETWORK)

    @staticmethod
    def protocol() -> Self:
        """Gets the information category for protocol.

        Returns:
            The information category for protocol.
        """
        return InfoCategory(_InfoCategoryEnum.PROTOCOL)

    def get_enum_type(self) -> EnumTypeId:
        """Gets the enum type from the information category.

        Returns:
            The enum type.

        Raises:
            ValueError: If the information category is unknown.
        """
        match self.root:
            case _InfoCategoryEnum.ASSET:
                return EnumTypeId.asset()
            case _InfoCategoryEnum.NETWORK:
                return EnumTypeId.network()
            case _InfoCategoryEnum.PROTOCOL:
                return EnumTypeId.protocol()
            case _:
                raise ValueError(f"Unknown information category: {self}")

    def get_model_dir_path(self) -> Path:
        """Gets the model directory from the information category.

        Returns:
            The model directory.
        """
        return PWD.joinpath(self.root)
