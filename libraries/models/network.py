from libraries.models.currency import Currency
from libraries.models.engine import Engine
from libraries.models.id import Id
from libraries.models.image_info import ImageInfo
from libraries.models.network_type import NetworkType
from libraries.models.reference_list import ReferenceList
from libraries.models.tag_list import TagList
from libraries.models.templates.camelcase_model import CamelCaseModel


class Network(CamelCaseModel):
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
    id: Id
    images: ImageInfo
    name: str
    network: NetworkType
    tags: TagList
    unknown_asset_id: Id
