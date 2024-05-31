from re import search
from typing import Annotated, Iterator, Any

from pydantic import WrapValidator, RootModel

from libraries.models.templates.str_model import StrModel


class Id(StrModel):
    """A constrained `str` for the ID.
    (IDs must be lowercase alphanumeric strings, optionally with numbering.)"""

    def validate_str(self) -> Any:
        if not search(r"^[a-z0-9]+(\-[a-z0-9]+)*(\-[0-9]+)?$", self.root):
            raise ValueError(f"Invalid description: {self.root}")
        return self


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
