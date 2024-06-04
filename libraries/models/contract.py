from pydantic import NonNegativeInt

from libraries.models.address import Address
from libraries.models.id import Id
from libraries.models.tag_list import TagList
from libraries.models.templates.camelcase_model import CamelCaseModel


class Contract(CamelCaseModel):
    """The base model of information about each asset contract in blockchain networks.

    Attributes:
        address: address of the asset contract (`Address`: constrained `str`.)
        decimals: decimals of the asset contract (`NonNegativeInt`: constrained `int`.)
        name: name of the asset contract (`str`)
        network: network ID of the asset contract in network information (`Id`: constrained `str`.)
        symbol: the symbol string of the asset contract (`str`)
        tags: tags of the asset contract (`TagList`: constrained `list` of `Tag`.)
    """

    address: Address
    decimals: NonNegativeInt
    name: str
    network: Id
    symbol: str
    tags: TagList
