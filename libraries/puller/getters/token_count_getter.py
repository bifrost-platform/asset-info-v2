from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
    prompt,
)
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError

TOKEN_COUNT_PER_PAGE: int = 50


class TokenCountValidator(Validator):
    """Validator for the token count input."""

    def validate(self, document: Document) -> None:
        """Validate the token count input.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the input is not a number, is not positive, or is not a multiple of PAGE_TOKEN_COUNT.
        """
        text = document.text
        if not text.isdigit():
            raise ValidationError(message="Please enter a number")
        if int(text) <= 0:
            raise ValidationError(message="Please enter a positive number")
        if int(text) % TOKEN_COUNT_PER_PAGE != 0:
            raise ValidationError(
                message=f"Please enter a multiple of {TOKEN_COUNT_PER_PAGE}"
            )


def get_token_count() -> int:
    """Get the number of tokens to pull.

    Returns:
        The number of tokens to pull.
    """
    printf(
        HTML(
            f"<b>Enter the number of tokens (a positive multiple of {TOKEN_COUNT_PER_PAGE})</b>"
        )
    )
    token_count = prompt(
        HTML("<b>> </b>"),
        completer=WordCompleter([str(i * TOKEN_COUNT_PER_PAGE) for i in range(1, 5)]),
        placeholder=str(TOKEN_COUNT_PER_PAGE),
        validator=TokenCountValidator(),
    )
    return int(token_count)
