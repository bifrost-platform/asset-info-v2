from pydantic import NonNegativeInt

from libraries.models.address import Address
from libraries.models.id import Id
from libraries.utils.model import CamelCaseModel


class Currency(CamelCaseModel):
    """The base model of information on assets as currencies in blockchain networks.

    Attributes:
        address: address regarded as a currency contract in asset information (`Address`: constrained `str`.)
        decimals: decimals of the currency (`NonNegativeInt`: constrained `int`.)
        id: ID of the currency in asset information (`Id`: constrained `str`.)
        name: name of the currency (`str`)
        symbol: the symbol string of the currency (`str`)
    """

    address: Address
    decimals: NonNegativeInt
    id: Id
    name: str
    symbol: str
