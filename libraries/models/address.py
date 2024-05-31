from typing import Annotated, Type, Union

from pydantic import StringConstraints, RootModel, AfterValidator
from web3 import Web3

EVM_ADDRESS_PATTERN: str = r"^0x[a-fA-F0-9]{40}$"
"""Regex pattern for an Ethereum Virtual Machine (EVM) address."""

EvmAddress: Type = RootModel[
    Annotated[
        str,
        StringConstraints(pattern=EVM_ADDRESS_PATTERN),
        AfterValidator(lambda x: Web3.to_checksum_address(x)),
    ]
]
"""A constrained `str` for the EVM address."""

Address: Type = RootModel[Union[EvmAddress]]
"""A union of constrained `str` about each address of blockchain networks."""


def is_evm_address(address: Address) -> bool:
    """Check if the address is an EVM address.

    Args:
        address: The address to check.

    Returns:
        Whether the address is an EVM address.
    """
    return isinstance(address.root, EvmAddress)
