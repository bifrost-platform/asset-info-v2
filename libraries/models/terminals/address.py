from typing import Union, Self, get_args

from pydantic import RootModel, model_validator

from libraries.models.terminals.address_bitcoin import AddressBitcoin
from libraries.models.terminals.address_evm import AddressEvm

ADDRESS_TYPES = Union[AddressEvm, AddressBitcoin]


class Address(RootModel[ADDRESS_TYPES]):
    """A union of constrained `str` about each address of blockchain networks."""

    def __eq__(self, other: Self) -> bool:
        if self.is_evm_address and other.is_evm_address:
            return self.root.__eq__(other.root)
        elif self.is_bitcoin_address and other.is_bitcoin_address:
            return self.root.__eq__(other.root)
        else:
            raise ValueError(
                f"Cannot compare difference addresses {type(self.root)} and {type(other.root)}."
            )

    def __ne__(self, other: Self) -> bool:
        return not self.__eq__(other)

    def __lt__(self, other: Self) -> bool:
        if self.is_evm_address and other.is_evm_address:
            return self.root.__lt__(other.root)
        elif self.is_bitcoin_address and other.is_bitcoin_address:
            return self.root.__lt__(other.root)
        else:
            raise ValueError(
                f"Cannot compare difference addresses {type(self.root)} and {type(other.root)}."
            )

    def __le__(self, other: Self) -> bool:
        return self.__lt__(other) or self.__eq__(other)

    def __gt__(self, other: Self) -> bool:
        return not self.__le__(other)

    def __ge__(self, other: Self) -> bool:
        return not self.__lt__(other)

    def __hash__(self) -> int:
        return self.root.__hash__()

    def __str__(self) -> str:
        return self.root.__str__()

    @property
    def is_evm_address(self) -> bool:
        """Check if the address is an EVM address.

        Returns:
            Whether the address is an EVM address.
        """
        return isinstance(self.root, AddressEvm)

    @property
    def is_bitcoin_address(self) -> bool:
        """Check if the address is a Bitcoin address.

        Returns:
            Whether the address is a Bitcoin address.
        """
        return isinstance(self.root, AddressBitcoin)

    @model_validator(mode="after")
    def validator(self) -> Self:
        root_types = get_args(ADDRESS_TYPES)
        if type(self.root) in root_types:
            return self
        elif isinstance(self.root, str):
            for root_type in root_types:
                try:
                    self.root = root_type(self.root)
                    return self
                except ValueError:
                    continue
        raise ValueError(f"Invalid address: {self.root}")
