from typing import Self

from libraries.models.terminals.tag import Tag
from libraries.models.templates.list_model import ListModel


class TagList(ListModel[Tag]):
    """A constrained `list` of `Tag`."""

    def validate_items(self) -> Self:
        for idx in range(len(self.root) - 1):
            fst, snd = idx, idx + 1
            if self.root[fst] >= self.root[snd]:
                raise ValueError(
                    "Tag list must be sorted in ascending order and unique, but got "
                    + f"""{self.root[fst]}, before {self.root[snd]}"""
                )
        return self
