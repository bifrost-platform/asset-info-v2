from libraries.models.abstractions.info_model import InfoModel
from libraries.models.currency import Currency
from libraries.models.reference_list import ReferenceList
from libraries.models.terminals.engine import Engine
from libraries.models.terminals.id import Id
from libraries.models.terminals.info_category import InfoCategory
from libraries.models.terminals.network_type import NetworkType


class Network(InfoModel):
    """The base model of information about each blockchain network.

    Attributes:
        currency: currency information of the network (`Currency`)
        engine: engine type of the network (`Engine`)
        explorers: explorers' information of the network (`ReferenceList`: constrained `list` of `Reference`.)
        id: ID of the network (`Id`: constrained `str`.)
        images: information about the existence of each image type (`ImageInfo`)
        name: name of the network (`str`)
        network: type of the network (`NetworkType`)
        tags: tags of the network (`TagList`: constrained `list` of `Tag`.)
        unknown_asset_id: ID of the unknown asset of the network (`Id`: constrained `str`.)
    """

    currency: Currency
    engine: Engine
    explorers: ReferenceList
    network: NetworkType
    unknown_asset_id: Id

    @staticmethod
    def get_info_category() -> InfoCategory:
        return InfoCategory.network()
