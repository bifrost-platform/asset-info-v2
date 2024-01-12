from pydantic import StringConstraints, WrapValidator
from typing_extensions import Annotated, Type

ID_PATTERN: str = r"^[a-z0-9\-]+(\-[0-9]+)?$"
"""Regex pattern for an ID."""

Id: Type = Annotated[str, StringConstraints(pattern=ID_PATTERN)]
"""A constrained :class:`str` for the ID.
(IDs must be lowercase alphanumeric strings, optionally with numbering.)"""


def __validate_id_list(value: dict, handler) -> list[Id]:
    """Validate the list of IDs.

    Args:
        value: The dictionary value to validate.
        handler: The handler of the Pydantic validator.

    Returns:
        The validated list of :class:`Id`.

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


IdList: Type = Annotated[list[Id], WrapValidator(__validate_id_list)]
"""Constrained :class:`list` of :class:`Id`."""
