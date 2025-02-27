import os
import logging
from abc import ABC, abstractmethod

from web3 import Web3
from dotenv import load_dotenv

from eth_typing import Address, ABI


load_dotenv()
ETH_RPC_URL = os.environ["ETH_RPC_URL"]


logger = logging.getLogger(__name__)


class AbstractRpc(ABC):
    class RpcConnectionError(Exception):
        pass

    @abstractmethod
    def __init__(self, token_contract: Address) -> None:
        pass

    @abstractmethod
    def get_balance_of(self, wallet_address: Address) -> int:
        pass

    @abstractmethod
    def get_total_supply(self) -> int:
        pass


class ERC20(AbstractRpc):
    # Minimal ERC20 ABI for balanceOf and totalSupply functions
    ERC20_ABI: ABI = [
        {
            "constant": True,
            "inputs": [{"name": "_owner", "type": "address"}],
            "name": "balanceOf",
            "outputs": [{"name": "balance", "type": "uint256"}],
            "type": "function",
        },
        {
            "constant": True,
            "inputs": [],
            "name": "totalSupply",
            "outputs": [{"name": "", "type": "uint256"}],
            "type": "function",
        },
    ]

    def __init__(self, token_contract: Address) -> None:
        self._w3 = Web3(Web3.HTTPProvider(ETH_RPC_URL))

        # Verify connection
        if not self._w3.is_connected():
            logger.error("Failed to connect to RPC, please retry")
            raise self.RpcConnectionError("Failed to connect to RPC, please retry")

        self.contract = self._w3.eth.contract(
            address=Web3.to_checksum_address(token_contract), abi=self.ERC20_ABI
        )
        super().__init__(token_contract)

    def get_balance_of(self, wallet_address: Address):
        return self.contract.functions.balanceOf(
            Web3.to_checksum_address(wallet_address)
        ).call()

    def get_total_supply(self):
        return self.contract.functions.totalSupply().call()
