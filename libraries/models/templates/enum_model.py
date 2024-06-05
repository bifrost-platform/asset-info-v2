from abc import abstractmethod
from enum import StrEnum
from typing import Any, Annotated, Self

from pydantic import RootModel, BeforeValidator


def _check_enum(enum: Any) -> str:
    """Check if the value is an Enum.

    Args:
        enum: The value to check.

    Returns:
        The valid Enum.
    """
    if not isinstance(enum, str):
        raise ValueError(f"The value must be a string.: {enum}")
    return enum


class EnumModel[T: StrEnum](RootModel[Annotated[T, BeforeValidator(_check_enum)]]):
    """A model that converts string to Enum.

    Notes:
        T should be a string Enum.
    """

    def __eq__(self, other: Any) -> bool:
        match other:
            case EnumModel():
                return self.root == other.root
            case str():
                return self.root == other

    def __lt__(self, other: Self) -> bool:
        return self.order < other.order

    def __le__(self, other: Self) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: Self) -> bool:
        return not self.__le__(other)

    def __ge__(self, other: Self) -> bool:
        return not self.__lt__(other)

    def __hash__(self) -> int:
        return self.root.__hash__()

    def __str__(self) -> str:
        return self.root.value

    @property
    def order(self) -> int:
        """Get the order of the Enum.

        Returns:
            The order of the Enum.
        """
        return self.ascending_list().index(self.root)

    @property
    def value(self) -> str:
        """Get the value of the Enum.

        Returns:
            The value of the Enum.
        """
        return self.__str__()

    @classmethod
    @abstractmethod
    def ascending_list(cls) -> list[Self]:
        """Get the list of Enum in ascending order.

        Returns:
            The list of Enum in ascending order.
        """
        raise NotImplementedError

    @classmethod
    def descending_list(cls) -> list[Self]:
        """Get the list of Enum in descending order.

        Returns:
            The list of Enum in descending order.
        """
        return list(reversed(cls.ascending_list()))
