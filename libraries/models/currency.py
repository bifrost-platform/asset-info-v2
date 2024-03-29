from pydantic import NonNegativeInt

from libraries.models.address import Address
from libraries.models.id import Id
from libraries.utils.model import CamelCaseModel


class Currency(CamelCaseModel):
    """The base model of information on assets as currencies in blockchain networks.

    Attributes:
        address: address regarded as a currency contract in asset information.
                 (:class:`Address`: constrained :class:`str`.)
        decimals: decimals of the currency. (:class:`NonNegativeInt`: constrained :class:`int`.)
        id: ID of the currency in asset information. (:class:`Id`: constrained :class:`str`.)
        name: name of the currency. (:class:`str`)
        symbol: the symbol string of the currency. (:class:`str`)
    """

    address: Address
    decimals: NonNegativeInt
    id: Id
    name: str
    symbol: str
