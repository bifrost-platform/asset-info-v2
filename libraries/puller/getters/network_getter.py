from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
    prompt,
)
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.document import Document
from prompt_toolkit.validation import Validator, ValidationError

from libraries.models.terminals.id import Id
from libraries.models.network import Network


class NetworkValidator(Validator):
    """Validator for network ID.

    Attributes:
        network_ids: The list of valid network IDs.

    Args:
        network_ids: The list of network IDs to use for validation.
    """

    network_ids: list[Id]

    def __init__(self, network_ids: list[Id]) -> None:
        self.network_ids = network_ids

    def validate(self, document: Document) -> None:
        """Validate the network ID.

        Args:
            document: The document to validate.

        Raises:
            ValidationError: If the network ID is not found in the list of valid network IDs.
        """
        text = document.text
        if text not in self.network_ids:
            raise ValidationError(message=f"Network {text} not found")


def get_network() -> Network:
    """Get network information from the given network ID.

    Returns:
        The network information if it exists, otherwise None.
    """
    networks = sorted(
        [network for network, _ in Network.get_info_list()],
        key=lambda x: x.id,
    )
    network_ids = [network.id for network in networks if len(network.explorers) > 0]
    printf(
        HTML(
            "<b>Enter the network ID: </b>"
            + ", ".join(value.root for value in network_ids)
        )
    )
    network_completer = WordCompleter([value.root for value in network_ids])
    network_id = prompt(
        HTML("<b>> </b>"),
        completer=network_completer,
        placeholder=network_ids[0].root if len(network_ids) != 0 else None,
        validator=NetworkValidator(network_ids),
    )
    return next(filter(lambda x: x.id == Id(network_id), networks))
