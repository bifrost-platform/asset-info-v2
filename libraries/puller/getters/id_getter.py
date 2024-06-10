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
        is_none_accepted: Whether the None value is accepted.

    Args:
        forbidden_id: The set of forbidden IDs to use for validation.
        permitted_id: The set of permitted IDs to use for validation.
        is_none_accepted: Whether the None value is accepted.
    """

    forbidden_id: set[Id]
    permitted_id: set[Id]
    is_none_accepted: bool

    def __init__(
        self,
        forbidden_id: set[Id] | None,
        permitted_id: set[Id] | None,
        is_none_accepted: bool,
    ) -> None:
        self.forbidden_id = forbidden_id or set()
        self.permitted_id = permitted_id or set()
        self.is_none_accepted = is_none_accepted

    def validate(self, document: Document) -> None:
        """Validate the ID input.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the input ID is not valid.
        """
        text = document.text
        try:
            if text == "" and self.is_none_accepted:
                return
            if (input_id := Id(text)) not in self.forbidden_id:
                if self.permitted_id and input_id not in self.permitted_id:
                    raise ValidationError(
                        message=f"Input ID is not permitted: {','.join(str(value) for value in self.permitted_id)}"
                    )
            else:
                raise ValidationError(message="Input ID is forbidden")
        except PydanticValidationError:
            raise ValidationError(message="Invalid ID")


def get_id(
    msg: str,
    forbidden_id: set[Id] | None = None,
    permitted_id: set[Id] | None = None,
    is_none_accepted: bool = False,
) -> Id | None:
    """Get the ID.

    Args:
        msg: The message to display.
        forbidden_id: The list of forbidden IDs.
        permitted_id: The list of permitted IDs.
        is_none_accepted: Whether the None value is accepted.

    Returns:
        The ID.

    Notes:
        The forbidden rule is prioritized over the permitted rule.
    """
    printf(
        HTML(
            f"<b>{msg}</b>"
            + (
                ": " + ", ".join(str(value) for value in permitted_id)
                if permitted_id
                else ""
            )
        )
    )
    completer = (
        WordCompleter([str(value) for value in permitted_id]) if permitted_id else None
    )
    input_id = prompt(
        HTML("<b>> </b>"),
        completer=completer,
        placeholder=str(permitted_id.copy().pop()) if permitted_id else None,
        validator=IdValidator(forbidden_id, permitted_id, is_none_accepted),
    )
    return None if input_id == "" and is_none_accepted else Id(input_id)
