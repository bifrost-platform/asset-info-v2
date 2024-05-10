from abc import ABCMeta, abstractmethod
from copy import deepcopy
from json import dump
from os import mkdir
from os.path import exists
from pathlib import Path
from tempfile import NamedTemporaryFile

from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
)
from prompt_toolkit.shortcuts import confirm, clear
from pydantic import HttpUrl
from requests import get
from web3 import Web3, HTTPProvider
from yarl import URL

from libraries.models.address import Address
from libraries.models.asset import Asset
from libraries.models.contract import Contract
from libraries.models.engine import EngineEnum
from libraries.models.id import Id
from libraries.models.image_info import ImageInfo
from libraries.models.network import Network
from libraries.models.reference import Reference
from libraries.preprocess.image import downscale_png
from libraries.puller.getters.http_url_getter import get_http_url
from libraries.puller.getters.id_getter import get_id
from libraries.puller.getters.token_count_getter import get_token_count
from libraries.puller.getters.yn_getter import get_flag
from libraries.utils.eth_erc20 import EthErc20Interface
from libraries.utils.file import get_model_dir_path, PWD, get_model_info_list

ETH_REFERENCE_BASE: dict[Id, URL] = {
    "coingecko": URL("https://www.coingecko.com/en/coins/"),
    "coinmarketcap": URL("https://coinmarketcap.com/currencies/"),
}


class TokenPullerAbstracted(metaclass=ABCMeta):
    """Abstracted class for token puller.

    Attributes:
        all_assets: The map of assets managed by asset-info-v2.
        network_assets: The map of assets in the given `self.network`.
        node_url: The node URL of the network.
        flag_image_pull: The flag for image pull.
        network: The network information.
        token_count: The token count for pulling.
    """

    all_assets: dict[Id, Asset]
    forbidden_asset_id: set[Id]
    network_assets: dict[Address, Asset]
    node_url: HttpUrl
    flag_image_pull: bool
    network: Network
    token_count: int

    def __init__(
        self,
        network: Network,
    ) -> None:
        """Initialize the token puller abstracted class.

        Args:
            network: The network information.
        """
        clear()
        printf(HTML("<b>✶ Set puller ✶</b>"))
        self.network = network
        self.token_count = get_token_count()
        self.node_url = get_http_url(f"Enter the node URL of {self.network.name}")
        self.__check_node_url(network, URL(self.node_url))
        self.flag_image_pull = get_flag("Do you want to pull images?")
        self.all_assets, self.network_assets = self.__get_assets()
        self.forbidden_asset_id = set(
            asset.id for asset in self.network_assets.values()
        )

    def run(self) -> None:
        """Run the interactive token puller."""
        target_token_list = self.__get_target_token_list()
        length = len(target_token_list)
        for idx, (address, info) in enumerate(target_token_list.items(), 1):
            clear()
            printf(HTML(f"<b>✶ [{idx}/{length}] Pull {address} ✶</b>"))
            printf(
                HTML(f"<b>  from <skyblue>{self._get_token_url(address)}</skyblue></b>")
            )
            gen_info = info if info else self.__make_asset_information(address)
            if gen_info is None:
                continue
            new_info = self.__save_image(address, gen_info)
            self.__save_asset_information(new_info, info)
            if not confirm("Next?"):
                break

    @abstractmethod
    def _get_top_token_list(self) -> set[Address]:
        """Get the top token list from the given network's explorer.

        Returns:
            The list of top token addresses.
        """
        raise ModuleNotFoundError(
            "Abstract method `get_top_token_list` is not implemented"
        )

    @abstractmethod
    def _get_token_url(self, address: Address) -> URL:
        """Get the URL of the token.

        Args:
            address: The address of the token.

        Returns:
            The URL of the token.
        """
        raise ModuleNotFoundError("Abstract method `get_token_url` is not implemented")

    @abstractmethod
    def _get_token_image_url(self, address: Address) -> URL | None:
        """Get the URL of the token image.

        Args:
            address: The address of the token.

        Returns:
            The URL of the token image.
        """
        raise ModuleNotFoundError(
            "Abstract method `get_token_image_url` is not implemented"
        )

    @abstractmethod
    def _download_token_image(self, token_image_url: URL) -> bytes | None:
        """Download the image of the token.

        Args:
            token_image_url: The URL of the token image.

        Returns:
            The image of the token if it is downloaded, otherwise None.
        """
        raise ModuleNotFoundError(
            "Abstract method `download_token_image` is not implemented"
        )

    @staticmethod
    def __check_node_url(network: Network, url: URL) -> None:
        """Check the node URL.

        Args:
            network: The network information.
            url: The node URL.

        Raises:
            ValueError: If the node URL is invalid.
        """
        if network.engine == EngineEnum.EVM:
            web3 = Web3(HTTPProvider(str(url)))
            if (
                not web3.is_connected()
                or str(web3.eth.chain_id) != network.id.split("-")[-1]
            ):
                printf(HTML(f"<red>Invalid node URL: {url}</red>"))
                raise ValueError("Invalid node URL")

    def __get_assets(self) -> tuple[dict[Id, Asset], dict[Address, Asset]]:
        """Get the asset information in the given network.

        Returns:
            The tuple of asset map.
            The first element is the map of all asset information.
            The second element is the map of asset addresses and asset information.
        """
        all_assets = {asset.id: asset for asset, _ in get_model_info_list(Asset)}
        network_assets = {}
        for asset in all_assets.values():
            if contract := next(
                filter(lambda x: x.network == self.network.id, asset.contracts),
                None,
            ):
                if contract.address.lower() in network_assets:
                    raise ValueError(f"Duplicate address found: {contract.address}")
                else:
                    network_assets[contract.address.lower()] = asset
        return all_assets, network_assets

    def __get_target_token_list(self) -> dict[Address, Asset | None]:
        """Get the target token list from the top token list.

        Returns:
            The map of target token addresses and asset information.
        """
        top_token_list = self._get_top_token_list()
        target_token_list = {}
        for token in top_token_list:
            if asset := self.network_assets.get(token.lower(), None):
                if self.flag_image_pull and not asset.images.svg:
                    target_token_list[token] = asset
            else:
                target_token_list[token] = None
        return target_token_list

    def __make_asset_information(self, address: Address) -> Asset | None:
        """Make new or updated asset information.

        Args:
            address: The address of the token.

        Returns:
            The asset information if it is new or updated, otherwise None.
        """
        it = EthErc20Interface(self.node_url, address)
        asset_id = get_id(
            f"Enter the ID of asset '{it.get_name()}'({it.get_symbol()})",
            forbidden_id=self.forbidden_asset_id,
        )
        if asset_id not in self.all_assets:
            contract = self.__pull_contract_information(it)
            return self.__pull_asset_information(contract, asset_id)
        else:
            if confirm(
                f"The id '{asset_id}' is already exists. Would you like to overwrite?"
            ):
                info = self.all_assets.get(asset_id)
                contract = self.__pull_contract_information(it)
                info.contracts.append(contract)
                info.contracts.sort(key=lambda x: x.network)
                return info
            else:
                return None

    def __pull_contract_information(self, it: EthErc20Interface) -> Contract:
        """Pull the contract information.

        Args:
            it: The ERC20 interface.

        Returns:
            The pulled contract information.
        """
        return Contract(
            address=Address(it.contract.address),
            decimals=it.get_decimals(),
            name=it.get_name(),
            network=self.network.id,
            symbol=it.get_symbol(),
            tags=[self.network.network],
        )

    def __pull_asset_information(self, contract: Contract, asset_id: Id) -> Asset:
        """Pull the asset information.

        Args:
            contract: The contract information.
            asset_id: The asset ID.

        Returns:
            The pulled asset information.
        """
        raw_references = filter(
            None,
            [
                self.__get_reference(ref_id, ref_base_url)
                for ref_id, ref_base_url in ETH_REFERENCE_BASE.items()
            ],
        )
        return Asset(
            contracts=[contract],
            id=asset_id,
            images=ImageInfo.create_empty(),
            name=contract.name,
            references=sorted(list(raw_references), key=lambda x: x.id),
            tags=[],
        )

    @staticmethod
    def __get_reference(ref_id: Id, ref_base_url: URL) -> Reference | None:
        """Get the reference information.

        Args:
            ref_id: The reference ID.
            ref_base_url: The base URL of the reference.

        Returns:
            The reference information if it exists, otherwise None.
        """
        asset_id = get_id(
            f"Enter the asset ID on https://{ref_base_url.host} if exists"
        )
        if asset_id != "":
            url = ref_base_url / asset_id
            response = get(str(url))
            if response.status_code == 200:
                return Reference(id=ref_id, url=HttpUrl(str(url)))
        return None

    def __save_image(self, address: Address, info: Asset) -> Asset:
        """Download the image of the asset.

        Args:
            info: The asset information.

        Returns:
            The updated asset information.
        """
        if (token_image_url := self._get_token_image_url(address)) is None:
            return info
        printf(HTML(f"Image URL found: <skyblue>{token_image_url}</skyblue>"))
        if not confirm("Would you like to download the image?"):
            return info
        if (image := self._download_token_image(token_image_url)) is None:
            return info
        new_info = deepcopy(info)
        tmp_dir = PWD.joinpath("tmp")
        if not exists(tmp_dir):
            mkdir(tmp_dir)
        with NamedTemporaryFile(mode="w+b", dir=tmp_dir, suffix=".png") as fp:
            fp.write(image)
            fp.flush()
            asset_path = get_model_dir_path(Asset).joinpath(new_info.id)
            if not exists(asset_path):
                mkdir(asset_path)
            downloaded_type = downscale_png(
                asset_path,
                Path(fp.name),
                overwrite=False,
            )
            for image_type in downloaded_type:
                new_info.images.set(image_type)
        return new_info

    def __save_asset_information(self, new_info: Asset, old_info: Asset) -> None:
        """Save the updated asset information.

        Args:
            new_info: The updated asset information.
            old_info: The old asset information.
        """
        if new_info == old_info:
            return None
        printf(HTML(f"<grey>{new_info.model_dump(mode='json')}</grey>"))
        if confirm("Would you like to save this asset information?"):
            self.forbidden_asset_id.add(new_info.id)
            path = get_model_dir_path(Asset).joinpath(new_info.id)
            if not exists(path):
                mkdir(path)
            with open(path.joinpath("info.json"), "w") as fp:
                dump(new_info.model_dump(mode="json"), fp, indent=2)
                fp.write("\n")
