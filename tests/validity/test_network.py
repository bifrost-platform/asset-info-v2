from pathlib import Path
from typing import Tuple

from libraries.models.asset import Asset
from libraries.models.enum_id_type import EnumIdType
from libraries.models.enum_info import EnumInfo
from libraries.models.enum_tag_type import EnumTagType
from libraries.models.network import Network
from libraries.models.network_type import NetworkTypeEnum
from tests.utils.checker import (
    check_info_json_existence,
    check_images_validity,
)
from tests.utils.reader import read_models


class TestValidityNetwork:
    """Tests the validity of network information.

    Attributes:
        asset_list: List of asset information.
        network_list: List of network information.
        network_id_list: List of network ID enum information.
        network_explorer_id_list: List of network explorer ID enum information.
        network_tag_list: List of network tag enum information.
    """

    asset_list = list[Tuple[Asset, Path]]
    network_list = list[Tuple[Network, Path]]
    network_id_list = list[EnumInfo]
    network_explorer_id_list = list[EnumInfo]
    network_tag_list = list[EnumInfo]

    def setup_class(self):
        """Set up the class before tests in this class."""
        self.asset_list = read_models(Asset)
        self.network_list = read_models(Network)
        self.network_id_list = EnumIdType.network().get_enum_info()
        self.network_explorer_id_list = EnumIdType.network_explorer().get_enum_info()
        self.network_tag_list = EnumTagType.network().get_enum_info()

    def test_all_dir_has_info_json(self):
        """All directories for network information have a `info.json` file."""
        check_info_json_existence(Network)

    def test_currency_exists_in_asset_contract(self):
        """The Currency exists in asset contract and its information is match with it.

        Notes:
            Contract also has `native-coin` and network type tags.
            If the type of network is `UNKNOWN`, tags are not checked.
        """
        asset_map = {asset.id: asset for asset, _ in self.asset_list}
        for network, _ in self.network_list:
            asset = asset_map.get(network.currency.id, None)
            assert asset is not None
            contract = next(
                (c for c in asset.contracts if c.network == network.id), None
            )
            assert contract is not None
            assert network.currency.address == contract.address
            assert network.currency.decimals == contract.decimals
            assert network.currency.symbol == contract.symbol
            assert network.currency.name == contract.name
            if network.network != NetworkTypeEnum.UNKNOWN:
                assert "native-coin" in contract.tags
                assert network.network in contract.tags

    def test_all_explorer_id_exists_in_enum_info(self):
        """All explorer ID in network information has an ID which is described
        in the enum information `enum/ids/explorer.json`."""
        explorer_id_value_list = [item.value for item in self.network_explorer_id_list]
        for network, _ in self.network_list:
            for explorer in network.explorers:
                assert explorer.id in explorer_id_value_list

    def test_all_id_exists_in_enum_info(self):
        """All ID in network information has an ID which is described
        in the enum information `enum/ids/network.json`."""
        id_map = {item.value: item.description for item in self.network_id_list}
        for network, _ in self.network_list:
            assert network.id in id_map
            # its description is the same as its name
            assert id_map.get(network.id) == network.name

    def test_all_image_exists(self):
        """All networks' images are valid."""
        for network, file in self.network_list:
            check_images_validity(network.images, file)

    def test_all_tags_exists_in_enum_info(self):
        """All tags in network information have a tag which is described
        in the enum information `enum/tags/network.json`."""
        tag_value_list = [item.value for item in self.network_tag_list]
        for network, _ in self.network_list:
            for tag in network.tags:
                assert tag in tag_value_list

    def test_all_unknown_asset_id_in_asset_list(self):
        """All unknown asset ID in network information has an asset which is
        described in the asset information `asset.json`."""
        asset_id_list = [item.id for item, _ in self.asset_list]
        for network, _ in self.network_list:
            assert network.unknown_asset_id in asset_id_list
            if network.unknown_asset_id.root.startswith("unknown-"):
                assert (
                    network.unknown_asset_id.root.removeprefix("unknown-")
                    in network.tags
                )
