from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
    prompt,
)
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError
from pydantic import ValidationError as PydanticValidationError

from libraries.models.id import Id


class IdValidator(Validator):
    """Validator for ID input.

    Attributes:
        forbidden_id: The set of forbidden IDs.

    Args:
        forbidden_id: The set of forbidden IDs to use for validation.
    """

    forbidden_id: set[Id]

    def __init__(self, forbidden_id: set[Id] | None) -> None:
        self.forbidden_id = forbidden_id or set()

    def validate(self, document: Document) -> None:
        """Validate the ID input.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the input ID is not valid.
        """
        text = document.text
        try:
            if input_id := Id(text) not in self.forbidden_id:
                return input_id
            else:
                raise ValidationError(message="Input ID is forbidden")
        except PydanticValidationError:
            raise ValidationError(message="Invalid ID")


def get_id(msg: str, forbidden_id: set[Id] | None = None) -> Id:
    """Get the ID.

    Args:
        msg: The message to display.
        forbidden_id: The list of forbidden IDs.

    Returns:
        The ID.
    """
    printf(HTML(f"<b>{msg}</b>"))
    input_id = prompt(HTML("<b>> </b>"), validator=IdValidator(forbidden_id))
    return Id(input_id)
