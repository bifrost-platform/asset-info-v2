from abc import ABCMeta, abstractmethod
from enum import StrEnum
from pathlib import Path

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
