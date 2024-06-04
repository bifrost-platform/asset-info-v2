from libraries.models.terminals.description import Description
from libraries.models.terminals.id import Id
from libraries.models.templates.camelcase_model import CamelCaseModel


class EnumInfo(CamelCaseModel):
    """The base model of information about each enumerated value.

    Attributes:
        value: ID of the enumerated value (`Id`: constrained `str`.)
        description: description of the enumerated value (`Description`: constrained `str`.)
    """

    value: Id
    description: Description
