from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
    prompt,
)
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError
from pydantic import ValidationError as PydanticValidationError, HttpUrl


class HttpUrlValidator(Validator):
    """Validator for HTTP URL input."""

    def validate(self, document: Document) -> None:
        """Validate the HTTP URL input.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the input HTTP URL is not valid.
        """
        text = document.text
        try:
            HttpUrl(text)
        except PydanticValidationError:
            raise ValidationError(message="Invalid URL")


def get_http_url(msg: str) -> str:
    """Get the HTTP URL.

    Args:
        msg: The message to display.

    Returns:
        The HTTP URL.
    """
    printf(HTML(f"<b>{msg}</b>"))
    input_url = prompt(HTML("<b>> </b>"), validator=HttpUrlValidator())
    return input_url
