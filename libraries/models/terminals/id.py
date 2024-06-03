from re import search
from typing import Self

from libraries.models.templates.str_model import StrModel


class Id(StrModel):
    """A constrained `str` for the ID.
    (IDs must be lowercase alphanumeric strings, optionally with numbering.)"""

    def validate_str(self) -> Self:
        if not search(r"^[a-z0-9]+(\-[a-z0-9]+)*(\-[0-9]+)?$", self.root):
            raise ValueError(f"Invalid description: {self.root}")
        return self
