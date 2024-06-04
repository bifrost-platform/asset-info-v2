from abc import ABCMeta, abstractmethod
from typing import Annotated, Self, Iterator, Callable, Any

from pydantic import RootModel, BeforeValidator, model_validator


def _check_list(lst: Any) -> list:
    """Check if the value is a list of T.

    Args:
        lst: The value to check.

    Returns:
        The valid list of T.
    """
    if not isinstance(lst, list):
        raise ValueError(f"The value must be a list.: {lst}")
    return lst


class ListModel[T](
    RootModel[Annotated[list[T], BeforeValidator(_check_list)]], metaclass=ABCMeta
):
    """A constrained `list` of T."""

    def __getitem__(self, key: int) -> T:
        return self.root[key]

    def __iter__(self) -> Iterator[T]:
        return iter(self.root)

    def __len__(self) -> int:
        return len(self.root)

    @abstractmethod
    def validate_items(self) -> list[T]:
        """Validate the items in the list.

        Returns:
            The validated list.
        """
        raise NotImplementedError

    @model_validator(mode="wrap")
    def validator(self: list[T], handler: Callable[[list[T]], Self]) -> Self:
        return handler(self).validate_items()
