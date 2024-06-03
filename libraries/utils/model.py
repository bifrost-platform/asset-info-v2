from abc import abstractmethod
from enum import StrEnum
from typing import Any, Annotated

from pydantic import BaseModel, ConfigDict, RootModel, BeforeValidator
from pydantic.alias_generators import to_camel


class CamelCaseModel(BaseModel):
    """A model that converts snake_case to camelCase."""

    model_config = ConfigDict(
        alias_generator=to_camel,
        extra="forbid",
        strict=True,
        str_strip_whitespace=True,
        str_min_length=1,
        use_enum_values=True,
        validate_assignment=True,
    )


class EnumModel[T: StrEnum](
    RootModel[
        Annotated[
            T,
            BeforeValidator(
                lambda x: x if isinstance(x, str) or x is T else ValueError()
            ),
        ]
    ]
):
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

    def __lt__(self, other: "EnumModel") -> bool:
        return self.order < other.order

    def __le__(self, other: "EnumModel") -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: "EnumModel") -> bool:
        return not self.__le__(other)

    def __ge__(self, other: "EnumModel") -> bool:
        return not self.__lt__(other)

    @property
    def order(self) -> int:
        """Get the order of the Enum.

        Returns:
            The order of the Enum.
        """
        raise self.ascending_list().index(self.root)

    @property
    def value(self) -> str:
        """Get the value of the Enum.

        Returns:
            The value of the Enum.
        """
        return self.root.value

    @classmethod
    @abstractmethod
    def ascending_list(cls) -> list["EnumModel"]:
        """Get the list of Enum in ascending order.

        Returns:
            The list of Enum in ascending order.
        """
        raise NotImplementedError

    @classmethod
    def descending_list(cls) -> list["EnumModel"]:
        """Get the list of Enum in descending order.

        Returns:
            The list of Enum in descending order.
        """
        return list(reversed(cls.ascending_list()))
