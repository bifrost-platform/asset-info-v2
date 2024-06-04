from asyncio import gather
from copy import deepcopy
from pathlib import Path
from typing import Tuple

import pytest
from pydantic import HttpUrl

from libraries.models.asset import Asset
from libraries.models.enum_info import EnumInfo
from libraries.models.enum_info_list import EnumInfoList
from libraries.models.network import Network
from libraries.models.reference_list import ReferenceList
from libraries.models.terminals.enum_type_id import EnumTypeId
from libraries.models.terminals.enum_type_tag import EnumTypeTag
from libraries.models.terminals.id import Id
from libraries.utils.eth_erc20 import EthErc20Interface
from libraries.utils.file import PWD
from tests.utils.checker import (
    check_info_json_existence,
    check_images_validity,
)
from tests.utils.reader import read_models


class TestValidityAsset:
    """Tests the validity of asset information.

    Attributes:
        asset_list: List of asset information.
        asset_id_list: List of asset ID enum information.
        asset_reference_id_list: List of asset reference ID enum information.
        network_id_list: List of network ID enum information.
        asset_contract_tag_list: List of asset contract tag enum information.
        asset_tag_list: List of asset tag enum information.
        network_map: Mapping of network ID to network information.
        rpc_map: Mapping of network ID to RPC URL.
    """

    asset_list: list[Tuple[Asset, Path]]
    asset_id_list: list[EnumInfo]
    asset_reference_id_list: list[EnumInfo]
    network_id_list: list[EnumInfo]
    asset_contract_tag_list: list[EnumInfo]
    asset_tag_list: list[EnumInfo]
    network_map: dict[Id, Network]
    rpc_map: dict[Id, HttpUrl]

    def setup_class(self):
        """Set up the class before tests in this class."""
        self.asset_list = read_models(Asset)
        self.asset_id_list = EnumInfoList.get_info_list(EnumTypeId.asset())
        self.asset_reference_id_list = EnumInfoList.get_info_list(
            EnumTypeId.asset_reference()
        )
        self.network_id_list = EnumInfoList.get_info_list(EnumTypeId.network())
        self.asset_contract_tag_list = EnumInfoList.get_info_list(
            EnumTypeTag.asset_contracts()
        )
        self.asset_tag_list = EnumInfoList.get_info_list(EnumTypeTag.asset())
        self.network_map = {network.id: network for network, _ in read_models(Network)}
        self.rpc_map = {
            rpc.id: rpc.url
            for rpc in ReferenceList.get_ref_list(
                PWD.joinpath("libraries/constants/rpc.json")
            )
            if rpc.url
        }

    def test_all_dir_has_info_json(self):
        """All directories for asset information have a `info.json` file."""
        check_info_json_existence(Asset)

    def test_all_contracts_network_exists_in_enum_info(self):
        """All contracts in asset information have a network which is described
        in the enum information `enum/ids/network.json`."""
        network_value_list = [item.value for item in self.network_id_list]
        for asset, _ in self.asset_list:
            for contract in asset.contracts:
                assert contract.network in network_value_list
                network = self.network_map.get(contract.network, None)
                assert network is not None
                assert str(network.network) in contract.tags

    def test_all_contracts_tag_exists_in_enum_info(self):
        """All contracts in asset information have a tag which is described
        in the enum information `enum/tags/asset.contracts.json`."""
        tag_value_list = [item.value for item in self.asset_contract_tag_list]
        for asset, _ in self.asset_list:
            for contract in asset.contracts:
                for tag in contract.tags:
                    assert tag in tag_value_list

    @pytest.mark.asyncio
    async def test_all_contracts_info_valid(self):
        """All contracts in asset information are valid."""
        for asset, _ in self.asset_list:
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

    def test_all_id_exists_in_enum_info(self):
        """All asset information has an ID which is described in the enum
        information `enum/ids/asset.json`."""
        id_map = {item.value: item.description for item in self.asset_id_list}
        assert len(self.asset_list) == len(id_map)
        for asset, _ in self.asset_list:
            assert asset.id in id_map
            # its description is the same as its name
            assert id_map.get(asset.id) == asset.name

    def test_all_image_valid(self):
        """All assets' images are valid."""
        for asset, file in self.asset_list:
            check_images_validity(asset.images, file)

    def test_all_name_in_its_contracts(self):
        """All assets' name exists in `contracts` of `Asset`."""
        for asset, _ in self.asset_list:
            contract_name_list = [contract.name for contract in asset.contracts]
            if len(contract_name_list) != 0:
                assert asset.name in contract_name_list

    def test_all_reference_id_exists_in_enum_info(self):
        """All asset information has a reference ID which is described in the
        enum information `enum/ids/asset.reference.json`."""
        reference_id_value_list = [item.value for item in self.asset_reference_id_list]
        for asset, _ in self.asset_list:
            for reference in asset.references:
                assert reference.id in reference_id_value_list
                assert reference.url is not None

    def test_all_tags_exists_in_enum_info(self):
        """All assets' tags exist in `tags` of `Asset`."""
        tag_value_list = [item.value for item in self.asset_tag_list]
        for asset, _ in self.asset_list:
            for tag in asset.tags:
                assert tag in tag_value_list
