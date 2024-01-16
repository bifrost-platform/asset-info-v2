from pydantic import HttpUrl

from libraries.models.id import Id, IdList
from libraries.models.image_info import ImageInfo
from libraries.models.tag import TagList
from libraries.utils.model import CamelCaseModel


class Protocol(CamelCaseModel):
    """The base model of information about each protocol.

    Attributes:
        id: ID of the protocol. (:class:`IdList`: constrained :class:`list` of :class:`Id`.)
        images: information about the existence of each image type. (:class:`ImageInfo`)
        name: name of the protocol. (:class:`str`)
        networks: network IDs of the protocol that supports. (:class:`Id`: constrained :class:`str`.)
        tags: tags of the protocol. (:class:`TagList`: constrained :class:`list` of :class:`Tag`.)
        url: main URL of the protocol. (:class:`HttpUrl`: constrained :class:`str`.)
    """

    id: Id
    images: ImageInfo
    name: str
    networks: IdList
    tags: TagList
    url: HttpUrl
