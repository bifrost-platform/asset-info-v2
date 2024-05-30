from typing import Tuple

from libraries.models.enum_id_type import EnumIdType
from libraries.models.enum_info import EnumInfo
from libraries.models.enum_tag_type import EnumTagTypeEnum
from libraries.models.protocol import Protocol
from libraries.utils.file import File
from tests.utils.checker import check_info_json_existence, check_images_validity
from tests.utils.reader import read_models, read_enum_info


class TestValidityProtocol:
    """Tests the validity of protocol information."""

    protocol_list: list[Tuple[Protocol, File]]
    network_id_list = list[EnumInfo]
    protocol_id_list = list[EnumInfo]
    protocol_tag_list = list[EnumInfo]

    def setup_class(self):
        """Set up the class before tests in this class."""
        self.protocol_list = read_models(Protocol)
        self.network_id_list = read_enum_info(EnumIdType.network())
        self.protocol_id_list = read_enum_info(EnumIdType.protocol())
        self.protocol_tag_list = read_enum_info(EnumTagTypeEnum.PROTOCOL)

    def test_all_dir_has_info_json(self):
        """All directories for protocol information have a `info.json` file."""
        check_info_json_existence(Protocol)

    def test_all_id_exists_in_enum_info(self):
        """All ID in protocol information has an ID which is described
        in the enum information `enum/ids/protocol.json`."""
        id_map = {item.value: item.description for item in self.protocol_id_list}
        for protocol, _ in self.protocol_list:
            assert protocol.id in id_map
            # its description is the same as its name
            assert id_map.get(protocol.id) == protocol.name

    def test_all_image_exists(self):
        """All protocols' images are valid."""
        for protocol, file in self.protocol_list:
            check_images_validity(protocol.images, file)

    def test_all_networks_exists_in_enum_info(self):
        """All networks in protocol information have a network which is described
        in the enum information `enum/ids/network.json`."""
        network_value_list = [item.value for item in self.network_id_list]
        for protocol, _ in self.protocol_list:
            for network in protocol.networks:
                assert network in network_value_list

    def test_all_tags_exists_in_enum_info(self):
        """All tags in protocol information have a tag which is described
        in the enum information `enum/tags/protocol.json`."""
        tag_value_list = [item.value for item in self.protocol_tag_list]
        for protocol, _ in self.protocol_list:
            for tag in protocol.tags:
                assert tag in tag_value_list
