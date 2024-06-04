from pydantic import HttpUrl

from libraries.models.abstractions.info_model import InfoModel
from libraries.models.terminals.id_list import IdList
from libraries.models.terminals.info_category import InfoCategory


class Protocol(InfoModel):
    """The base model of information about each protocol.

    Attributes:
        id: ID of the protocol (`IdList`: constrained `list` of `Id`.)
        images: information about the existence of each image type (`ImageInfo`)
        name: name of the protocol (`str`)
        networks: network IDs of the protocol that supports (`Id`: constrained `str`.)
        tags: tags of the protocol (`TagList`: constrained `list` of `Tag`.)
        url: main URL of the protocol (`HttpUrl`: constrained `str`.)
    """

    networks: IdList
    url: HttpUrl

    @staticmethod
    def get_info_category() -> InfoCategory:
        return InfoCategory.protocol()
