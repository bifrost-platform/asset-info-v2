from typing import Annotated, Type, Union

from pydantic import StringConstraints

from libraries.utils.string import is_regex_in

EVM_ADDRESS_PATTERN: str = r"^0x[a-fA-F0-9]{40}$"
"""Regex pattern for an Ethereum Virtual Machine (EVM) address."""

EvmAddress: Type = Annotated[str, StringConstraints(pattern=EVM_ADDRESS_PATTERN)]
"""A constrained :class:`str` for the EVM address."""

Address: Type = Union[EvmAddress]
"""A union of constrained :class:`str` about each address of blockchain networks."""


def is_evm_address(address: str) -> bool:
    """Check if the address is an EVM address.

    Args:
        address: The address to check.

    Returns:
        Whether the address is an EVM address.
    """
    return is_regex_in(address, EVM_ADDRESS_PATTERN)
