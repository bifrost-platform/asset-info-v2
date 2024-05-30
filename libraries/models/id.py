from typing import Annotated, Iterator, Any

from pydantic import StringConstraints, WrapValidator, RootModel

__ID_PATTERN: str = r"^[a-z0-9]+(\-[a-z0-9]+)*(\-[0-9]+)?$"
"""Regex pattern for an ID."""


class Id(RootModel[Annotated[str, StringConstraints(pattern=__ID_PATTERN)]]):
    """A constrained `str` for the ID.
    (IDs must be lowercase alphanumeric strings, optionally with numbering.)"""

    def __eq__(self, other: Any) -> bool:
        match other:
            case Id():
                return self.root == other.root
            case str():
                return self.root == other
            case _:
                return False

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Any) -> bool:
        match other:
            case Id():
                return self.root < other.root
            case str():
                return self.root < other
            case _:
                raise ValueError(f"Cannot compare {self} with {other}")

    def __le__(self, other: Any) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: Any) -> bool:
        return not self.__le__(other)

    def __ge__(self, other: Any) -> bool:
        return not self.__lt__(other)

    def __hash__(self) -> int:
        return hash(self.root)


def __validate_id_list(value: dict, handler) -> list[Id]:
    """Validate the list of IDs.

    Args:
        value: The dictionary value to validate.
        handler: The handler of the Pydantic validator.

    Returns:
        The validated list of `Id`.

    Notes:
        The list of IDs must be sorted in ascending order and unique.
    """
    for idx in range(len(value) - 1):
        fst, snd = idx, idx + 1
        if value[fst] >= value[snd]:
            raise ValueError(
                "ID list must be sorted in ascending order and unique, but got "
                + f"""{value[fst]}, before {value[snd]}"""
            )
    return handler(value)


class IdList(RootModel[Annotated[list[Id], WrapValidator(__validate_id_list)]]):
    """Constrained `list` of `Id`."""

    def __iter__(self) -> Iterator[Id]:
        return iter(self.root)

    def __getitem__(self, item) -> Id:
        return self.root[item]
