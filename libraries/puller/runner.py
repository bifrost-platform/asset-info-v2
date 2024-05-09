from typing import Type

from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
)
from prompt_toolkit.shortcuts import clear

from libraries.puller.getters.explorer_getter import get_explorer_id
from libraries.puller.getters.network_getter import get_network
from libraries.puller.token_pullers.token_puller_abstracted import TokenPullerAbstracted

TOKEN_PULLER_CLASS_MAP: dict[str, Type[TokenPullerAbstracted]] = {}


def run_token_puller() -> None:
    """Run interactive token puller."""
    clear()
    printf(HTML("<b>✶ Start the token puller prompt ✶</b>"))
    network = get_network()
    if len(network.explorers) == 0:
        printf(HTML("<b><red>Error: </red>No explorer found</b>"))
        return
    explorer_id = get_explorer_id(
        [
            explorer
            for explorer in network.explorers
            if explorer.id in TOKEN_PULLER_CLASS_MAP
        ]
    )
    clear()
    if token_puller_class := TOKEN_PULLER_CLASS_MAP.get(explorer_id, None):
        token_puller = token_puller_class(network)
        token_puller.run()
    else:
        printf(HTML("<b><red>Error: </red>Token puller not implemented</b>"))
        return