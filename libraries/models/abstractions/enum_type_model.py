from abc import ABCMeta, abstractmethod
from enum import StrEnum
from json import loads
from pathlib import Path

from libraries.models.enum_info_list import EnumInfoList
from libraries.models.templates.enum_model import EnumModel
from libraries.utils.file import PWD


class EnumTypeModel[T: StrEnum](EnumModel[T], metaclass=ABCMeta):
    """The base model of enumerated type information."""

    @property
    @abstractmethod
    def type(self) -> str:
        """Gets the type of the enum."""
        raise NotImplementedError

    def get_enum_path(self) -> Path:
        """Gets the enum path from the enum tag type.

        Returns:
            The enum path.
        """
        return PWD.joinpath("enums").joinpath(self.type).joinpath(f"{self.value}.json")

    def get_enum_info(self) -> EnumInfoList:
        """Reads the enum information from the given enum tag type.

        Returns:
            The enum information.
        """
        with open(self.get_enum_path(), "r") as fp:
            return EnumInfoList.model_validate(loads(fp.read()))
