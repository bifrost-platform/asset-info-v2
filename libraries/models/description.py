from typing import Type, Annotated

from pydantic import StringConstraints

DESCRIPTION_PATTERN: str = r".+[^.]$"
"""Regex pattern for a description."""

Description: Type = Annotated[str, StringConstraints(pattern=DESCRIPTION_PATTERN)]
"""A constrained :class:`str` for the description of :class:`EnumInfo`.
(The description must not end with a period.)"""
