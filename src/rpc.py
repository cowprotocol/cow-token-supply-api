import os
import logging
from abc import ABC, abstractmethod

from web3 import Web3
from dotenv import load_dotenv

from eth_typing import Address, ABI


load_dotenv()

logger = logging.getLogger(__name__)


class AbstractRpc(ABC):
    class RpcConnectionError(Exception):
        pass

    @abstractmethod
    def __init__(self, token_contract: Address, rpc_url_env_var: str) -> None:
        pass

    @abstractmethod
    def get_balance_of(self, wallet_address: Address) -> int:
        pass

    @abstractmethod
    def get_total_supply(self) -> int:
        pass


class EvmERC20(AbstractRpc):
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

    def __init__(self, token_contract: Address, rpc_url_env_var: str) -> None:
        rpc_url = os.environ.get(rpc_url_env_var)
        if not rpc_url:
            raise self.RpcConnectionError(
                f"Environment variable {rpc_url_env_var} is not set"
            )

        self._w3 = Web3(Web3.HTTPProvider(rpc_url))

        if not self._w3.is_connected():
            logger.error("Failed to connect to RPC from %s", rpc_url_env_var)
            raise self.RpcConnectionError(
                f"Failed to connect to RPC from {rpc_url_env_var}"
            )

        self.contract = self._w3.eth.contract(
            address=Web3.to_checksum_address(token_contract), abi=self.ERC20_ABI
        )
        self._rpc_url_env_var = rpc_url_env_var
        super().__init__(token_contract, rpc_url_env_var)

    def get_balance_of(self, wallet_address: Address):
        return self.contract.functions.balanceOf(
            Web3.to_checksum_address(wallet_address)
        ).call()

    def get_total_supply(self):
        return self.contract.functions.totalSupply().call()
