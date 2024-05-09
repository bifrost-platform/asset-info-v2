from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
    prompt,
)
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError

from libraries.models.id import Id
from libraries.models.reference import Reference


class ExplorerValidator(Validator):
    """Validator for explorer ID.

    Attributes:
        explorer_ids: The list of valid explorer IDs.

    Args:
        explorer_ids: The list of explorer IDs to use for validation.
    """

    explorer_ids: list[Id]

    def __init__(self, explorer_ids: list[Id]) -> None:
        self.explorer_ids = explorer_ids

    def validate(self, document: Document) -> None:
        """Validate the explorer ID.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the explorer ID is not found in the list of explorer IDs.
        """
        text = document.text
        if text not in self.explorer_ids:
            raise ValidationError(message=f"Explorer {text} not found")


def get_explorer_id(explorers: list[Reference]) -> Id:
    """Get explorer ID from the given network.

    Args:
        explorers: The list of explorers in the network.

    Returns:
        The explorer ID if it exists, otherwise None.
    """
    explorer_ids = sorted([explorer.id for explorer in explorers])
    printf(HTML("<b>Enter the explorer ID: </b>" + ", ".join(explorer_ids)))
    explorer_completer = WordCompleter(explorer_ids)
    explorer_id = prompt(
        HTML("<b>> </b>"),
        completer=explorer_completer,
        placeholder=explorer_ids[0],
        validator=ExplorerValidator(explorer_ids),
    )
    return explorer_id
