from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
    prompt,
)
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError
from pydantic import ValidationError as PydanticValidationError

from libraries.models.terminals.id import Id


class IdValidator(Validator):
    """Validator for ID input.

    Attributes:
        forbidden_id: The set of forbidden IDs.
        permitted_id: The set of permitted IDs.

    Args:
        forbidden_id: The set of forbidden IDs to use for validation.
        permitted_id: The set of permitted IDs to use for validation.
    """

    forbidden_id: set[Id]
    permitted_id: set[Id]

    def __init__(
        self, forbidden_id: set[Id] | None, permitted_id: set[Id] | None
    ) -> None:
        self.forbidden_id = forbidden_id or set()
        self.permitted_id = permitted_id or set()

    def validate(self, document: Document) -> None:
        """Validate the ID input.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the input ID is not valid.
        """
        text = document.text
        try:
            if (input_id := Id(text)) not in self.forbidden_id:
                if self.permitted_id and input_id not in self.permitted_id:
                    raise ValidationError(
                        message=f"Input ID is not permitted: {','.join(value.root for value in self.permitted_id)}"
                    )
            else:
                raise ValidationError(message="Input ID is forbidden")
        except PydanticValidationError:
            raise ValidationError(message="Invalid ID")


def get_id(
    msg: str, forbidden_id: set[Id] | None = None, permitted_id: set[Id] | None = None
) -> Id:
    """Get the ID.

    Args:
        msg: The message to display.
        forbidden_id: The list of forbidden IDs.
        permitted_id: The list of permitted IDs.

    Returns:
        The ID.

    Notes:
        The forbidden rule is prioritized over the permitted rule.
    """
    printf(
        HTML(
            f"<b>{msg}</b>"
            + (
                ": " + ", ".join(value.root for value in permitted_id)
                if permitted_id
                else ""
            )
        )
    )
    completer = (
        WordCompleter([value.root for value in permitted_id]) if permitted_id else None
    )
    input_id = prompt(
        HTML("<b>> </b>"),
        completer=completer,
        placeholder=permitted_id.copy().pop() if permitted_id else None,
        validator=IdValidator(forbidden_id, permitted_id),
    )
    return Id(input_id)
