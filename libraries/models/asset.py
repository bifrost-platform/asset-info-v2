from libraries.models.abstractions.info_model import InfoModel
from libraries.models.contract_list import ContractList
from libraries.models.reference_list import ReferenceList
from libraries.models.terminals.info_category import InfoCategory


class Asset(InfoModel):
    """The base model of information about assets in blockchain networks.

    Attributes:
        contracts: contracts' information about the asset in blockchain networks (`ContractList`: constrained `list` of
            `Contract`.)
        id: ID of the asset (`Id`: constrained `str`.)
        images: information about the existence of each image type (`ImageInfo`)
        name: name of the asset (`str`: must be the same as one of the contract's names.)
        references: reference information for the asset (`ReferenceList`: constrained `list` of `Reference`.)
        tags: tags of the asset (`TagList`: constrained `list` of `Tag`.)
    """

    contracts: ContractList
    references: ReferenceList

    @staticmethod
    def get_info_category() -> InfoCategory:
        return InfoCategory.asset()
