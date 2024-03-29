from typing import Tuple

from web3 import Web3

from libraries.models.address import is_evm_address
from libraries.models.asset import Asset
from libraries.models.enum_id_type import EnumIdTypeEnum
from libraries.models.enum_info import EnumInfo
from libraries.models.enum_tag_type import EnumTagTypeEnum
from libraries.models.network import Network
from libraries.utils.file import File
from tests.utils.checker import (
    check_info_json_existence,
    check_images_validity,
)
from tests.utils.reader import read_models, read_enum_info


class TestValidityAsset:
    """Tests the validity of asset information.

    Attributes:
        asset_list: List of asset information.
        network_list: List of network information.
        asset_id_list: List of asset ID enum information.
        asset_reference_id_list: List of asset reference ID enum information.
        network_id_list: List of network ID enum information.
        asset_contract_tag_list: List of asset contract tag enum information.
        asset_tag_list: List of asset tag enum information.
    """

    asset_list: list[Tuple[Asset, File]]
    network_list: list[Tuple[Network, File]]
    asset_id_list: list[EnumInfo]
    asset_reference_id_list: list[EnumInfo]
    network_id_list: list[EnumInfo]
    asset_contract_tag_list: list[EnumInfo]
    asset_tag_list: list[EnumInfo]

    def setup_class(self):
        """Set up the class before tests in this class."""
        self.asset_list = read_models(Asset)
        self.network_list = read_models(Network)
        self.asset_id_list = read_enum_info(EnumIdTypeEnum.ASSET)
        self.asset_reference_id_list = read_enum_info(EnumIdTypeEnum.ASSET_REFERENCE)
        self.network_id_list = read_enum_info(EnumIdTypeEnum.NETWORK)
        self.asset_contract_tag_list = read_enum_info(EnumTagTypeEnum.ASSET_CONTRACTS)
        self.asset_tag_list = read_enum_info(EnumTagTypeEnum.ASSET)

    def test_all_dir_has_info_json(self):
        """All directory for asset information has a `info.json` file."""
        check_info_json_existence(Asset)

    def test_all_contracts_address_checksum_valid(self):
        """All contracts in asset information has a valid address checksum."""
        for asset, _ in self.asset_list:
            for contract in asset.contracts:
                if is_evm_address(contract.address):
                    assert Web3.is_checksum_address(contract.address)

    def test_all_contracts_network_exists_in_enum_info(self):
        """All contracts in asset information has a network which is described
        in the enum information `enum/ids/network.json`."""
        network_value_list = [item.value for item in self.network_id_list]
        for asset, _ in self.asset_list:
            for contract in asset.contracts:
                assert contract.network in network_value_list
                network = next(item for item, _ in self.network_list if item.id == contract.network)
                assert network.network in contract.tags

    def test_all_contracts_tag_exists_in_enum_info(self):
        """All contracts in asset information has a tag which is described
        in the enum information `enum/tags/asset.contracts.json`."""
        tag_value_list = [item.value for item in self.asset_contract_tag_list]
        for asset, _ in self.asset_list:
            for contract in asset.contracts:
                for tag in contract.tags:
                    assert tag in tag_value_list

    def test_all_id_exists_in_enum_info(self):
        """All asset information has an ID which is described in the enum
        information `enum/ids/asset.json`."""
        id_map = {item.value: item.description for item in self.asset_id_list}
        assert len(self.asset_list) == len(id_map)
        for asset, _ in self.asset_list:
            assert asset.id in id_map
            # its description is same as its name
            assert id_map.get(asset.id) == asset.name

    def test_all_image_valid(self):
        """All assets' images are valid."""
        for asset, file in self.asset_list:
            check_images_validity(asset.images, file)

    def test_all_name_in_its_contracts(self):
        """All assets' name exists in `contracts` of :class:`Asset`."""
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

    def test_all_tags_exists_in_enum_info(self):
        """All assets' tags exist in `tags` of :class:`Asset`."""
        tag_value_list = [item.value for item in self.asset_tag_list]
        for asset, _ in self.asset_list:
            for tag in asset.tags:
                assert tag in tag_value_list
