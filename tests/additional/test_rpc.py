from asyncio import gather
from copy import deepcopy
from pathlib import Path
from re import search
from subprocess import run, PIPE

import pytest
from pydantic import HttpUrl
from web3 import Web3, HTTPProvider

from libraries.models.asset import Asset
from libraries.models.network import Network
from libraries.models.reference_list import ReferenceList
from libraries.models.terminals.id import Id
from libraries.utils.eth_erc20 import EthErc20Interface
from libraries.utils.file import PWD
from tests.utils.reader import read_models


@pytest.mark.rpc
class TestAdditionalRpc:
    """Tests the information with RPC connection.

    Attributes:
        asset_list: List of asset information.
        network_list: List of network information.
        rpc_map: Mapping of network ID to RPC URL.
    """

    asset_list = list[tuple[Asset, Path]]
    network_list = list[tuple[Network, Path]]
    network_map: dict[Id, Network]
    rpc_map: dict[Id, HttpUrl]

    def setup_class(self):
        """Set up the class before tests in this class."""
        self.asset_list = read_models(Asset)
        self.network_list = read_models(Network)
        self.network_map = {network.id: network for network, _ in self.network_list}
        self.rpc_map = {
            rpc.id: rpc.url
            for rpc in ReferenceList.get_ref_list(
                PWD.joinpath("libraries/constants/rpc.json")
            )
            if rpc.url
        }

    @pytest.mark.asyncio
    async def test_rpc_url_map(self):
        """All networks have a valid RPC URL."""
        await gather(
            *[self.__test_rpc_url(network) for network, _ in self.network_list]
        )

    async def __test_rpc_url(self, network: Network):
        """Test the RPC URL of the network.

        Args:
            network: The network information.
        """
        if node_url := self.rpc_map.get(network.id, None):
            if network.engine.is_evm:
                node = Web3(HTTPProvider(node_url))
                assert node.is_connected(), f"The node ${network.id} is not connected."
                assert node.eth.chain_id == int(
                    str(network.id).removeprefix("evm-")
                ), "The chain ID ${node.eth.chain_id} does not match the network ID ${network.id}."
            else:
                pass
        else:
            pass

    @pytest.mark.asyncio
    async def test_all_contracts_info_valid(self):
        """All contracts in asset information are valid."""
        for asset in self.__filter_modified_assets():
            await gather(*[self.__test_all_contract_info_valid(asset)])

    async def __test_all_contract_info_valid(self, asset: Asset):
        """Test the validity of the contract information.

        Args:
            asset: The asset information.
        """
        for contract in asset.contracts:
            network = self.network_map.get(contract.network, None)
            # Skip unknown asset
            if asset.id == network.unknown_asset_id:
                return
            # Skip native coin
            if contract.address == network.currency.address:
                return
            # Check contract validity
            if node_url := self.rpc_map.get(network.id, None):
                if network.engine.is_evm:
                    erc20 = EthErc20Interface(node_url, str(contract.address))
                    name, symbol, decimals = await gather(
                        *[erc20.get_name(), erc20.get_symbol(), erc20.get_decimals()]
                    )
                    expected = deepcopy(contract)
                    expected.name = name
                    expected.symbol = symbol
                    expected.decimals = decimals
                    assert contract == expected
                else:
                    pass

    def __filter_modified_assets(self) -> list[Asset]:
        """Filter the modified assets."""
        # Get recent tag
        recent_tag_result = run(
            ["git", "describe", "--tags", "--abbrev=0", "HEAD^"],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            check=True,
        )
        recent_tag = recent_tag_result.stdout.strip()
        # Get modified files
        diff_result = run(
            ["git", "diff", "--name-only", recent_tag],
            stdout=PIPE,
            stderr=PIPE,
            text=True,
            check=True,
        )
        changed_files = [
            file for file in diff_result.stdout.strip().split("\n") if file
        ]
        asset_matches = [
            search(r"assets/([^/]+)/info.json", file) for file in changed_files
        ]
        asset_ids = [match.group(1) for match in asset_matches if match]
        return [asset for asset, _ in self.asset_list if asset.id in asset_ids]
