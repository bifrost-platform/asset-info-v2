from typing import Annotated, Callable, Type

from pydantic import NonNegativeInt, WrapValidator

from libraries.models.address import Address
from libraries.models.id import Id
from libraries.models.tag import TagList
from libraries.utils.model import CamelCaseModel


class Contract(CamelCaseModel):
    """The base model of information about each asset contract in blockchain networks.

    Attributes:
        address: address of the asset contract. (:class:`Address`: constrained :class:`str`.)
        decimals: decimals of the asset contract. (:class:`NonNegativeInt`: constrained :class:`int`.)
        name: name of the asset contract. (:class:`str`)
        network: network ID of the asset contract in network information. (:class:`Id`: constrained :class:`str`.)
        symbol: the symbol string of the asset contract. (:class:`str`)
        tags: tags of the asset contract. (:class:`TagList`: constrained :class:`list` of :class:`Tag`.)
    """

    address: Address
    decimals: NonNegativeInt
    name: str
    network: Id
    symbol: str
    tags: TagList


def __validate_contract_list(
    value: dict, handler: Callable[[dict], list[Contract]]
) -> list[Contract]:
    """Validate the list of contracts.

    Args:
        value: The dictionary value to validate.
        handler: The handler of the Pydantic validator.

    Returns:
        The validated list of :class:`Class`.

    Notes:
        The list of contracts must be sorted by network ID and address in ascending order,
        and the list of contracts must be unique by address in same network.
    """
    for idx in range(len(value) - 1):
        fst, snd = idx, idx + 1
        if value[fst]["network"] > value[snd]["network"]:
            raise ValueError(
                "Contract list must be sorted by network ID in ascending order, but got "
                + f"""{value[fst]["network"]}, before {value[snd]["network"]}"""
            )
        elif (
            value[fst]["network"] == value[snd]["network"]
            and value[fst]["address"] >= value[snd]["address"]
        ):
            raise ValueError(
                "Contract list must be sorted by address in ascending order and unique in same network, but got "
                + f"""{value[fst]["address"]}, before {value[snd]["address"]} at {value[fst]["network"]}"""
            )
    return handler(value)


ContractList: Type = Annotated[list[Contract], WrapValidator(__validate_contract_list)]
"""Constrained :class:`list` of :class:`Contract`."""
