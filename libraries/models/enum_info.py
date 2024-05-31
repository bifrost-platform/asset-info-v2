from typing import Callable, Annotated, Iterator

from pydantic import WrapValidator, RootModel

from libraries.models.description import Description
from libraries.models.id import Id
from libraries.utils.model import CamelCaseModel


class EnumInfo(CamelCaseModel):
    """The base model of information about each enumerated value.

    Attributes:
        value: ID of the enumerated value (`Id`: constrained `str`.)
        description: description of the enumerated value (`Description`: constrained `str`.)
    """

    value: Id
    description: Description


def _validate_enum_info_list(
    value: list[dict], handler: Callable[[list[dict]], list[EnumInfo]]
) -> list[EnumInfo]:
    """Validate the list of enum information.

    Args:
        value: The dictionary value to validate.
        handler: The handler of the Pydantic validator.

    Returns:
        The validated list of `EnumInfo`.

    Notes:
        The list of enum information must be sorted by value in ascending order and unique.
    """
    for idx in range(len(value) - 1):
        fst, snd = idx, idx + 1
        if value[fst]["value"] >= value[snd]["value"]:
            raise ValueError(
                "Enum info list must be sorted by value in ascending order and unique, but got "
                + f"""'{value[fst]["value"]}', before '{value[snd]["value"]}'"""
            )
    return handler(value)


class EnumInfoList(
    RootModel[Annotated[list[EnumInfo], WrapValidator(_validate_enum_info_list)]]
):
    """A constrained `list` of `EnumInfo`."""

    def __iter__(self) -> Iterator[EnumInfo]:
        return iter(self.root)

    def __getitem__(self, item) -> EnumInfo:
        return self.root[item]
