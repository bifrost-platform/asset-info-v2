from pathlib import Path

import pytest

from libraries.models.asset import Asset
from libraries.models.network import Network
from libraries.models.protocol import Protocol
from tests.utils.checker import check_images_validity, check_info_json_existence
from tests.utils.reader import read_models


class TestAdditionalFile:
    """Tests the files

    Attributes:
        asset_list: List of asset information.
        network_list: List of network information.
    """

    asset_list = list[tuple[Asset, Path]]
    network_list = list[tuple[Network, Path]]
    protocol_list: list[tuple[Protocol, Path]]

    def setup_class(self):
        """Set up the class before tests in this class."""
        self.asset_list = read_models(Asset)
        self.network_list = read_models(Network)
        self.protocol_list = read_models(Protocol)

    def test_all_dir_has_info_json(self):
        """All directories for information have a `info.json` file."""
        check_info_json_existence(Asset)
        check_info_json_existence(Network)
        check_info_json_existence(Protocol)

    @pytest.mark.image
    def test_all_asset_image_valid(self):
        """All assets' images are valid."""
        for asset, file in self.asset_list:
            check_images_validity(asset.images, file)

    @pytest.mark.image
    def test_all_network_image_exists(self):
        """All networks' images are valid."""
        for network, file in self.network_list:
            check_images_validity(network.images, file)

    @pytest.mark.image
    def test_all_protocol_image_exists(self):
        """All protocols' images are valid."""
        for protocol, file in self.protocol_list:
            check_images_validity(protocol.images, file)
