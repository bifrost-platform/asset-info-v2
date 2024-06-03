from typing import Self

from web3 import Web3

from libraries.models.templates.str_model import StrModel


class AddressEvm(StrModel):
    """A constrained `str` for the EVM address."""

    def __eq__(self, other: Self | str) -> bool:
        match other:
            case AddressEvm():
                return int(self.root, 16) == int(other.root, 16)
            case str():
                return int(self.root, 16) == int(other, 16)
            case _:
                raise ValueError(f"Cannot compare {self} with {other}")

    def __lt__(self, other: Self) -> bool:
        match other:
            case AddressEvm():
                return int(self.root, 16) < int(other.root, 16)
            case str():
                return int(self.root, 16) < int(other, 16)
            case _:
                raise ValueError(f"Cannot compare {self} with {other}")

    def validate_str(self) -> Self:
        if not Web3.is_address(self.root):
            raise ValueError(f"Invalid EVM address: {self.root}")
        if not Web3.is_checksum_address(self.root):
            raise ValueError(f"Invalid checksum address: {self.root}")
        return self
