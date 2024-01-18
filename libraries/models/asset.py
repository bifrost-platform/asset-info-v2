from libraries.models.contract import ContractList
from libraries.models.id import Id
from libraries.models.image_info import ImageInfo
from libraries.models.reference import ReferenceList
from libraries.models.tag import TagList
from libraries.utils.model import CamelCaseModel


class Asset(CamelCaseModel):
    """The base model of information about assets in blockchain networks.

    Attributes:
        contracts: contracts' information about the asset in blockchain networks.
                   (:class:`ContractList`: constrained :class:`list` of :class:`Contract`.)
        id: ID of the asset. (:class:`Id`: constrained :class:`str`.)
        images: information about the existence of each image type. (:class:`ImageInfo`)
        name: name of the asset. (:class:`str`: must be the same as one of the contract's names.)
        references: reference information for the asset.
                    (:class:`ReferenceList`: constrained :class:`list` of :class:`Reference`.)
        tags: tags of the asset. (:class:`TagList`: constrained :class:`list` of :class:`Tag`.)
    """

    contracts: ContractList
    id: Id
    images: ImageInfo
    name: str
    references: ReferenceList
    tags: TagList
