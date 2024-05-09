from typing import Callable, Annotated, Type

from pydantic import HttpUrl, WrapValidator

from libraries.models.id import Id
from libraries.utils.model import CamelCaseModel


class Reference(CamelCaseModel):
    """The base model of information about each reference.

    Attributes:
        id: ID of the reference.
        url: URL of the reference.
    """

    id: Id
    url: HttpUrl


def __validate_reference_list(
    value: list[dict | Reference],
    handler: Callable[[list[dict | Reference]], list[Reference]],
) -> list[Reference]:
    """Validate the list of references.

    Args:
        value: The dictionary value to validate.
        handler: The handler of the Pydantic validator.

    Returns:
        The validated list of `Reference`.

    Notes:
        The list of references must be sorted by ID in ascending order and unique.
    """
    for idx in range(len(value) - 1):
        fst = (
            Reference.model_validate(value[idx])
            if isinstance(value[idx], dict)
            else value[idx]
        )
        snd = (
            Reference.model_validate(value[idx + 1])
            if isinstance(value[idx + 1], dict)
            else value[idx + 1]
        )
        if fst.id >= snd.id:
            raise ValueError(
                "Reference list must be sorted by ID in ascending order and unique, but got "
                + f"""{fst.id}, before {snd.id}"""
            )
    return handler(value)


ReferenceList: Type = Annotated[
    list[Reference], WrapValidator(__validate_reference_list)
]
"""Constrained list of `Reference`."""
