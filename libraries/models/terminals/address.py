from typing import Union, Self

from pydantic import RootModel

from libraries.models.terminals.address_evm import AddressEvm


class Address(RootModel[Union[AddressEvm]]):
    """A union of constrained `str` about each address of blockchain networks."""

    def __eq__(self, other: Self) -> bool:
        if self.is_evm_address and other.is_evm_address:
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
