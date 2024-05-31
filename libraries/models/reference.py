from pydantic import HttpUrl

from libraries.models.id import Id
from libraries.models.templates.camelcase_model import CamelCaseModel


class Reference(CamelCaseModel):
    """The base model of information about each reference.

    Attributes:
        id: ID of the reference.
        url: URL of the reference.
    """

    id: Id
    url: HttpUrl
