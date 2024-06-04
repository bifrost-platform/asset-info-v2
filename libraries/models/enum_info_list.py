from typing import Self

from libraries.models.enum_info import EnumInfo
from libraries.models.templates.list_model import ListModel


class EnumInfoList(ListModel[EnumInfo]):
    """A constrained `list` of `EnumInfo`."""

    def validate_items(self) -> Self:
        for idx in range(len(self.root) - 1):
            fst, snd = idx, idx + 1
            if self.root[fst].value >= self.root[snd].value:
                raise ValueError(
                    "Enum info list must be sorted by value in ascending order and unique, but got "
                    + f"""'{self.root[fst].value}', before '{self.root[snd].value}'"""
                )
        return self
