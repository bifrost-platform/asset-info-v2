from re import search

from libraries.models.templates.str_model import StrModel


class Tag(StrModel):
    """A constrained `str` for the tag.
    (Tags must be lowercase alphanumeric strings, optionally with hyphens.)"""

    def validate_str(self) -> str:
        if not search(r"^[a-z0-9\-]+$", self.root):
            raise ValueError(f"Invalid description: {self.root}")
        return self
