from pydantic import StringConstraints
from typing_extensions import Annotated, Type, Union

EVM_ADDRESS_PATTERN: str = r"^0x[a-fA-F0-9]{40}$"
"""Regex pattern for an Ethereum Virtual Machine (EVM) address."""

EvmAddress: Type = Annotated[str, StringConstraints(pattern=EVM_ADDRESS_PATTERN)]
"""A constrained :class:`str` for the EVM address."""

Address: Type = Union[EvmAddress]
"""A union of constrained :class:`str` about each address of blockchain networks."""
