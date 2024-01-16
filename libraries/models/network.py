from libraries.models.currency import Currency
from libraries.models.engine import Engine
from libraries.models.id import Id
from libraries.models.image_info import ImageInfo
from libraries.models.network_type import NetworkType
from libraries.models.reference import ReferenceList
from libraries.models.tag import TagList
from libraries.utils.model import CamelCaseModel


class Network(CamelCaseModel):
    """The base model of information about each blockchain network.

    Attributes:
        currency: currency information of the network. (:class:`Currency`)
        engine: engine type of the network. (:class:`Engine`)
        explorers: explorers' information of the network.
                   (:class:`ReferenceList`: constrained :class:`list` of :class:`Reference`.)
        id: ID of the network. (:class:`Id`: constrained :class:`str`.)
        images: information about the existence of each image type. (:class:`ImageInfo`)
        name: name of the network. (:class:`str`)
        network: type of the network. (:class:`NetworkType`)
        tags: tags of the network.
              (:class:`TagList`: constrained :class:`list` of :class:`Tag`.)
    """

    currency: Currency
    engine: Engine
    explorers: ReferenceList
    id: Id
    images: ImageInfo
    name: str
    network: NetworkType
    tags: TagList
