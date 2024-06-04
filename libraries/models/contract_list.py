from typing import Self

from libraries.models.contract import Contract
from libraries.models.templates.list_model import ListModel


class ContractList(ListModel[Contract]):
    """Constrained `list` of `Contract`."""

    def validate_items(self) -> Self:
        for idx in range(len(self.root) - 1):
            fst, snd = idx, idx + 1
            if self.root[fst].network > self.root[snd].network:
                raise ValueError(
                    "Contract list must be sorted by network ID in ascending order, but got "
                    + f"""{self.root[fst].network}, before {self.root[snd].network}"""
                )
            elif (
                self.root[fst].network == self.root[snd].network
                and self.root[fst].address >= self.root[snd].address
            ):
                raise ValueError(
                    "Contract list must be sorted by address in ascending order and unique in same network, but got "
                    + f"""{self.root[fst].address}, before {self.root[snd].address} at {self.root[fst].network}"""
                )
        return self
