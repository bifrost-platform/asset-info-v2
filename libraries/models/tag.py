from pydantic import StringConstraints, WrapValidator
from typing_extensions import Annotated, Type

TAG_PATTERN: str = r"^[a-z0-9\-]+$"
"""Regex pattern for a tag."""

Tag: Type = Annotated[str, StringConstraints(pattern=TAG_PATTERN)]
"""A constrained :class:`str` for the tag.
(Tags must be lowercase alphanumeric strings, optionally with hyphens.)"""


def __validate_tag_list(value: dict, handler):
    """Validate the list of tags.

    Args:
        value: The dictionary value to validate.
        handler: The handler of the Pydantic validator.

    Returns:
        The validated list of :class:`Tag`.

    Notes:
        The list of tags must be sorted in ascending order and unique.
    """
    for idx in range(len(value) - 1):
        fst, snd = idx, idx + 1
        if value[fst] >= value[snd]:
            raise ValueError(
                "Tag list must be sorted in ascending order and unique, but got "
                + f"""{value[fst]}, before {value[snd]}"""
            )
    return handler(value)


TagList: Type = Annotated[list[Tag], WrapValidator(__validate_tag_list)]
"""Constrained :class:`list` of :class:`Tag`."""
