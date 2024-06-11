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

    def append(self, item: T) -> None:
        """Append an object to the end of the list.

        Args:
            item: The object to append.
        """
        self.root.append(item)

    def sort(self, key: Callable[[T], Any] = None, reverse: bool = False) -> None:
        """Sort the list in ascending order and return None.
        The sort is in-place (i.e., the list itself is modified) and stable
        (i.e., the order of two equal elements is maintained).
        If a key function is given, apply it once to each list item and sort them,
        ascending or descending, according to their function values.
        The reverse flag can be set to sort in descending order.

        Args:
            key: A callable that returns a value to compare and sort the list.
            reverse: A flag to sort in descending order.
        """
        self.root.sort(key=key, reverse=reverse)

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
