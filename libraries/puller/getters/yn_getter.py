from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
    prompt,
)
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError


class YNValidator(Validator):
    """Validator for yes/no input."""

    def validate(self, document: Document) -> None:
        """Validate the yes/no input.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the lowercase of input is not 'y' or 'n'.
        """
        text = document.text
        if text.lower() not in ["y", "n"]:
            raise ValidationError(message="Please enter 'y', 'Y', 'n', or 'N'")


def get_flag(msg: str) -> bool:
    """Get the flag.

    Args:
        msg: The message to display.

    Returns:
        The flag.
    """
    printf(HTML(f"<b>{msg} (y/n)</b>"))
    flag = prompt(
        HTML("<b>> </b>"),
        completer=WordCompleter(["y", "n"]),
        placeholder="n",
        validator=YNValidator(),
    )
    return flag.lower() == "y"
