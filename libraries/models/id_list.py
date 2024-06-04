from typing import Self

from libraries.models.id import Id
from libraries.models.templates.list_model import ListModel


class IdList(ListModel[Id]):
    """Constrained `list` of `Id`."""

    def validate_items(self) -> Self:
        for idx in range(len(self.root) - 1):
            fst, snd = idx, idx + 1
            if self.root[fst] >= self.root[snd]:
                raise ValueError(
                    "ID list must be sorted in ascending order, but got "
                    + f"{self.root[fst]}, before {self.root[snd]}"
                )
        return self
