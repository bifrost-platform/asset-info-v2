from pydantic import HttpUrl

from libraries.models.templates.camelcase_model import CamelCaseModel
from libraries.models.terminals.id import Id


class Reference(CamelCaseModel):
    """The base model of information about each reference.

    Attributes:
        id: ID of the reference.
        url: URL of the reference (Nullable.)
    """

    id: Id
    url: HttpUrl | None
