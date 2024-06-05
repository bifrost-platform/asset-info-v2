from re import search
from typing import Self

from libraries.models.templates.str_model import StrModel


class Description(StrModel):
    """A constrained `str` for the description of `EnumInfo` (The description must not end with a period.)"""

    def validate_str(self) -> Self:
        if not search(r".+[^.]$", self.root):
            raise ValueError(f"Invalid description: {self.root}")
        return self
