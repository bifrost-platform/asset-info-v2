from pydantic import HttpUrl

from libraries.models.id import Id
from libraries.models.id_list import IdList
from libraries.models.image_info import ImageInfo
from libraries.models.tag import TagList
from libraries.utils.model import CamelCaseModel


class Protocol(CamelCaseModel):
    """The base model of information about each protocol.

    Attributes:
        id: ID of the protocol (`IdList`: constrained `list` of `Id`.)
        images: information about the existence of each image type (`ImageInfo`)
        name: name of the protocol (`str`)
        networks: network IDs of the protocol that supports (`Id`: constrained `str`.)
        tags: tags of the protocol (`TagList`: constrained `list` of `Tag`.)
        url: main URL of the protocol (`HttpUrl`: constrained `str`.)
    """

    id: Id
    images: ImageInfo
    name: str
    networks: IdList
    tags: TagList
    url: HttpUrl
