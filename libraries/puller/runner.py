from typing import Type

from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
)
from prompt_toolkit.shortcuts import clear

from libraries.models.terminals.id import Id
from libraries.puller.getters.explorer_getter import get_explorer_id
from libraries.puller.getters.network_getter import get_network
from libraries.puller.token_pullers.token_puller_abstracted import TokenPullerAbstracted
from libraries.puller.token_pullers.token_puller_blockscout import TokenPullerBlockscout
from libraries.puller.token_pullers.token_puller_dexguru import TokenPullerDexguru
from libraries.puller.token_pullers.token_puller_etherscan import TokenPullerEtherscan

TOKEN_PULLER_CLASS_MAP: dict[Id, Type[TokenPullerAbstracted]] = {
    Id("blockscout"): TokenPullerBlockscout,
    Id("dexguru"): TokenPullerDexguru,
    Id("etherscan"): TokenPullerEtherscan,
}


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
        try:
            token_puller.run()
        finally:
            del token_puller
    else:
        printf(HTML("<b><red>Error: </red>Token puller not implemented</b>"))
        return
