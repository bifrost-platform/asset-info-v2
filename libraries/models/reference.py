from pydantic import HttpUrl, WrapValidator
from typing_extensions import Callable, Annotated, Type

from libraries.models.id import Id
from libraries.utils.model import CamelCaseModel


class Reference(CamelCaseModel):
    """The base model of information about each reference.

    Attributes:
        id: ID of the reference. (:class:`Id`: constrained :class:`str`.)
        url: URL of the reference. (:class:`HttpUrl`: constrained :class:`str`.)
    """

    id: Id
    url: HttpUrl


def __validate_reference_list(
    value: dict, handler: Callable[dict, list[Reference]]
) -> list[Reference]:
    """Validate the list of references.

    Args:
        value: The dictionary value to validate.
        handler: The handler of the Pydantic validator.

    Returns:
        The validated list of :class:`Reference`.

    Notes:
        The list of references must be sorted by ID in ascending order and unique.
    """
    for idx in range(len(value) - 1):
        fst, snd = idx, idx + 1
        if value[fst]["id"] >= value[snd]["id"]:
            raise ValueError(
                "Reference list must be sorted by ID in ascending order and unique, but got "
                + f"""{value[fst]["id"]}, before {value[snd]["id"]}"""
            )
    return handler(value)


ReferenceList: Type = Annotated[
    list[Reference], WrapValidator(__validate_reference_list)
]
"""Constrained :class:`list` of :class:`Reference`."""
