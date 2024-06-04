from abc import ABCMeta, abstractmethod
from typing import Annotated, Any, Self, Callable

from pydantic import RootModel, BeforeValidator, model_validator


def _check_str(s: Any) -> str:
    """Check if the value is a string.

    Args:
        s: The value to check.

    Returns:
        The valid string.
    """
    if not isinstance(s, str):
        raise ValueError(f"The value must be a string.: {s}")
    return s


class StrModel(
    RootModel[Annotated[str, BeforeValidator(_check_str)]], metaclass=ABCMeta
):
    """A constrained `str`."""

    def __eq__(self, other: Self | str) -> bool:
        match other:
            case StrModel():
                return self.root == other.root
            case str():
                return self.root == other
            case _:
                raise ValueError(f"Cannot compare {self} with {other}")

    def __ne__(self, other: Self | str) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Self | str) -> bool:
        match other:
            case StrModel():
                return self.root < other.root
            case str():
                return self.root < other
            case _:
                raise ValueError(f"Cannot compare {self} with {other}")

    def __le__(self, other: Self | str) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: Self | str) -> bool:
        return not self.__le__(other)

    def __ge__(self, other: Self | str) -> bool:
        return not self.__lt__(other)

    def __hash__(self) -> int:
        return hash(self.root)

    def __str__(self) -> str:
        return self.root

    @abstractmethod
    def validate_str(self) -> str:
        """Validate the string.

        Returns:
            The validated string.
        """
        raise NotImplementedError

    @model_validator(mode="wrap")
    def validator(self: str, handler: Callable[[str], Self]) -> Self:
        return handler(self).validate_str()
