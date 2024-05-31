from typing import Annotated, Any

from pydantic import StringConstraints, RootModel

DESCRIPTION_PATTERN: str = r".+[^.]$"
"""Regex pattern for a description."""


class Description(
    RootModel[Annotated[str, StringConstraints(pattern=DESCRIPTION_PATTERN)]]
):
    """A constrained `str` for the description of `EnumInfo` (The description must not end with a period.)"""

    def __eq__(self, other: Any) -> bool:
        match other:
            case Description():
                return self.root == other.root
            case str():
                return self.root == other
            case _:
                return False
