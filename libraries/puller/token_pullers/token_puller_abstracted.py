from abc import ABCMeta, abstractmethod
from copy import deepcopy
from json import dump
from os import mkdir
from os.path import exists
from pathlib import Path
from shutil import copy, rmtree
from tempfile import NamedTemporaryFile, mkdtemp

from prompt_toolkit import (
    print_formatted_text as printf,
    HTML,
)
from prompt_toolkit.shortcuts import confirm, clear
from pydantic import HttpUrl, ValidationError
from requests import get
from web3 import Web3, HTTPProvider
from yarl import URL

from libraries.models.address import Address
from libraries.models.asset import Asset
from libraries.models.contract import Contract
from libraries.models.id import Id
from libraries.models.image_info import ImageInfo
from libraries.models.image_type import ImageType
from libraries.models.info_category import InfoCategory
from libraries.models.network import Network
from libraries.models.reference import Reference
from libraries.preprocess.image import downscale_png, png_to_square
from libraries.preprocess.runner import run_enum_preprocess
from libraries.puller.getters.http_url_getter import get_http_url
from libraries.puller.getters.id_getter import get_id
from libraries.puller.getters.token_count_getter import get_token_count
from libraries.utils.eth_erc20 import EthErc20Interface
from libraries.utils.file import PWD

ETH_REFERENCE_BASE: dict[Id, URL] = {
    Id("coingecko"): URL("https://www.coingecko.com/en/coins/"),
    Id("coinmarketcap"): URL("https://coinmarketcap.com/currencies/"),
}


class NotSavedError(Exception):
    """Exception for not saved asset information."""


class TokenPullerAbstracted(metaclass=ABCMeta):
    """Abstracted class for token puller.

    Attributes:
        all_assets: The map of assets managed by asset-info-v2.
        network_assets: The map of assets in the given `self.network`.
        node_url: The node URL of the network.
        flag_image_pull: The flag for image pull.
        network: The network information.
        tmp_dir: The temporary directory for images.
        token_count: The token count for pulling.
    """

    all_assets: dict[Id, Asset]
    network_assets: dict[Address, Asset]
    node_url: HttpUrl
    flag_image_pull: bool
    network: Network
    tmp_dir: Path
    token_count: int

    def __init__(self, network: Network):
        """Initialize the token puller abstracted class.

        Args:
            network: The network information.
        """
        clear()
        printf(HTML("<b>✶ Set puller ✶</b>"))
        self.network = network
        self.tmp_dir = Path(mkdtemp(prefix="tmp_", dir=PWD))
        self.token_count = get_token_count()
        self.node_url = get_http_url(f"Enter the node URL of {self.network.name}")
        self.__check_node_url(network, URL(self.node_url))
        self.flag_image_pull = confirm("Do you want to pull images?")
        self.all_assets, self.network_assets = self.__get_assets(self.network)

    def __del__(self):
        """Remove the temporary directory and run the enum preprocessing."""
        rmtree(self.tmp_dir)
        run_enum_preprocess(Asset)
        printf(HTML("<b>✶ End puller ✶</b>"))

    def run(self) -> None:
        """Run the interactive token puller."""
        target_token_list = self.__get_target_token_list()
        length = len(target_token_list)
        for idx, address in enumerate(target_token_list, 1):
            retry = True
            while retry:
                retry = False
                try:
                    clear()
                    printf(HTML(f"<b>✶ [{idx}/{length}] Pull {address} ✶</b>"))
                    self.__run_body(address)
                except ValidationError as e:
                    printf(HTML(f"<red>Validation Error</red>\n<grey>{e}</grey>"))
                    retry = confirm("Would you like to retry?")
                except NotSavedError:
                    printf(HTML("<grey>Not saved</grey>"))
                    retry = confirm("Would you like to retry?")
            if idx < length and not confirm("Next?"):
                break

    def __run_body(self, address: Address) -> None:
        """Run the interactive token puller.

        Args:
            address: The address of the token.
        """
        address, name, symbol, decimals = self.__get_contract_info(address)
        printf(HTML(f"<b>  Name: {name}</b>"))
        printf(HTML(f"<b>  Symbol: {symbol}</b>"))
        printf(
            HTML(f"<b>  Source: <skyblue>{self._get_token_url(address)}</skyblue></b>")
        )
        info = self.network_assets.get(address.lower(), None)
        if info is not None and not confirm("Would you like to renew the information?"):
            return None
        gen_info = (
            info
            if info
            else self.__make_asset_information(address, name, symbol, decimals)
        )
        if gen_info is None:
            printf(HTML("<red>Failed to get asset information</red>"))
            return None
        img_info = self.__save_image(address, gen_info)
        if info == gen_info and img_info is None:
            printf(HTML("<grey>Nothing to update</grey>"))
            return None
        self.__save_asset_information(gen_info, img_info)

    @abstractmethod
    def _get_top_token_list(self) -> set[tuple[int, Address]]:
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
        if network.engine.is_evm:
            web3 = Web3(HTTPProvider(str(url)))
            if (
                not web3.is_connected()
                or str(web3.eth.chain_id) != network.id.split("-")[-1]
            ):
                printf(HTML(f"<red>Invalid node URL: {url}</red>"))
                raise ValueError("Invalid node URL")

    @staticmethod
    def __get_assets(network: Network) -> tuple[dict[Id, Asset], dict[Address, Asset]]:
        """Get the asset information in the given network.

        Args:
            network: The network information.

        Returns:
            The tuple of asset map.
            The first element is the map of all asset information.
            The second element is the map of asset addresses and asset information.
        """
        all_assets = {
            asset.id: asset for asset, _ in InfoCategory.asset().get_model_info_list()
        }
        network_assets = {}
        for asset in all_assets.values():
            for contract in filter(lambda x: x.network == network.id, asset.contracts):
                if contract.address.lower() in network_assets:
                    raise ValueError(f"Duplicate address found: {contract.address}")
                else:
                    network_assets[contract.address.lower()] = asset
        return all_assets, network_assets

    def __get_target_token_list(self) -> list[Address]:
        """Get the target token list from the top token list.

        Returns:
            The map of target token addresses and asset information.
        """
        top_token_list = sorted(self._get_top_token_list(), key=lambda x: x[0])
        target_token_list = list()
        for _, token in top_token_list:
            if asset := self.network_assets.get(token.lower(), None):
                if self.flag_image_pull and not asset.images.svg:
                    target_token_list.append(token)
            else:
                target_token_list.append(token)
        return target_token_list

    def __get_contract_info(self, address: Address) -> tuple[Address, str, str, int]:
        """Get the contract information.

        Args:
            address: The address of the token.

        Returns:
            The tuple of contract information.
        """
        if (asset := self.network_assets.get(address, None)) is not None:
            contract = next(
                filter(lambda x: x.network == self.network.id, asset.contracts)
            )
            return contract.address, contract.name, contract.symbol, contract.decimals
        assert self.network.engine.is_evm
        it = EthErc20Interface(self.node_url, address)
        return (
            Address(it.contract.address),
            it.get_name(),
            it.get_symbol(),
            it.get_decimals(),
        )

    def __make_asset_information(
        self, address: Address, name: str, symbol: str, decimals: int
    ) -> Asset | None:
        """Make new or updated asset information.

        Args:
            address: The address of the token.
            name: The name of the token.
            symbol: The symbol of the token.
            decimals: The decimals of the token.

        Returns:
            The asset information if it is new or updated, otherwise None.
        """
        asset_id = get_id(f"Enter the ID of asset")
        if asset_id not in self.all_assets:
            contract = self.__pull_contract_information(address, name, symbol, decimals)
            return self.__pull_asset_information(contract, asset_id)
        else:
            if confirm(
                f"The id '{asset_id}' is already exists. Would you like to overwrite?"
            ):
                info = deepcopy(self.all_assets.get(asset_id))
                contract = self.__pull_contract_information(
                    address, name, symbol, decimals
                )
                info.contracts.append(contract)
                info.contracts.sort(key=lambda x: x.network)
                return info
            elif confirm("Would you like to enter a new ID?"):
                return self.__make_asset_information(address, name, symbol, decimals)
            else:
                return None

    def __pull_contract_information(
        self, address: Address, name: str, symbol: str, decimals: int
    ) -> Contract:
        """Pull the contract information.

        Args:
            address: The address of the token.
            name: The name of the token.
            symbol: The symbol of the token.
            decimals: The decimals of the token.

        Returns:
            The pulled contract information.
        """
        return Contract(
            address=address,
            decimals=decimals,
            name=name,
            network=self.network.id,
            symbol=symbol,
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
            url = ref_base_url / asset_id.root
            response = get(str(url))
            if response.status_code == 200:
                return Reference(id=ref_id, url=HttpUrl(str(url)))
        return None

    def __save_image(
        self, address: Address, info: Asset
    ) -> tuple[Path, list[ImageType]] | None:
        """Download the image of the asset.

        Args:
            address: The address of the token.
            info: The asset information.

        Returns:
            The tuple of image path and image type if the image is downloaded, otherwise None.
        """
        # Get the image URL
        if (token_image_url := self._get_token_image_url(address)) is None:
            return None
        printf(HTML(f"Image URL found: <skyblue>{token_image_url}</skyblue>"))
        if not confirm("Would you like to download the image?"):
            return None
        # Download the image
        if (image := self._download_token_image(token_image_url)) is None:
            return None
        # Save the image
        image_path = Path(mkdtemp(prefix=info.id.root, dir=self.tmp_dir))
        with NamedTemporaryFile(
            mode="w+b", dir=image_path, suffix="_origin.png"
        ) as fp_origin:
            fp_origin.write(image)
            fp_origin.flush()
            with NamedTemporaryFile(
                mode="w+b", dir=image_path, suffix="_squared.png"
            ) as fp_square:
                # Convert the downloaded PNG image to a squared image
                png_to_square(Path(fp_origin.name), Path(fp_square.name))
                # Downscale the image
                downloaded_type = downscale_png(
                    Path(image_path),
                    Path(fp_square.name),
                )
        if len(downloaded_type) == 0 or info.images.get(
            max(downloaded_type, key=lambda x: x.size)
        ):
            return None
        return image_path, (
            downloaded_type if not info.images.get(max(downloaded_type)) else []
        )

    def __save_asset_information(
        self,
        info: Asset,
        image_info: tuple[Path, list[ImageType]] | None,
    ) -> None:
        """Save the updated asset information.

        Args:
            info: The asset information.
            image_info: The tuple of image path and image type.
        """
        new_info = deepcopy(info)
        for image_type in image_info[1] if image_info else []:
            new_info.images.set(image_type)
        printf(HTML(f"<grey>{new_info.model_dump(mode='json')}</grey>"))
        if confirm("Would you like to save this asset information?"):
            # Update all_assets and network_assets
            self.all_assets.update({new_info.id: new_info})
            for contract in new_info.contracts:
                if contract.address.lower() in self.network_assets:
                    self.network_assets.update({contract.address.lower(): new_info})
            # Get the path of the asset information
            path = (
                InfoCategory.get_info_category(Asset)
                .get_model_dir_path()
                .joinpath(new_info.id.root)
            )
            if not exists(path):
                mkdir(path)
            # Save the asset information
            with open(path.joinpath("info.json"), "w") as fp:
                dump(new_info.model_dump(mode="json"), fp, indent=2)
                fp.write("\n")
            # Save the images
            for image_type in image_info[1] if image_info else []:
                image_path = image_type.get_path(image_info[0])
                if exists(image_path):
                    copy(image_path, path)
        else:
            raise NotSavedError()
