from web3 import Web3
from eth_typing import Address, ABI
import logging
from cfg import RPC_URL

logger = logging.getLogger(__name__)


class ERC20:
    class RpcConnectionError(Exception):
        pass

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

    def __init__(self, token_contract: Address, rpc_url: str = RPC_URL) -> None:
        self._w3 = Web3(Web3.HTTPProvider(rpc_url))

        # Verify connection
        if not self._w3.is_connected():
            logger.error("Failed to connect to RPC, please retry")
            raise self.RpcConnectionError("Failed to connect to RPC, please retry")

        self.contract = self._w3.eth.contract(
            address=Web3.to_checksum_address(token_contract), abi=self.ERC20_ABI
        )

    def balanceOf(self, wallet_address: Address):
        return self.contract.functions.balanceOf(
            Web3.to_checksum_address(wallet_address)
        ).call()

    def totalSupply(self):
        return self.contract.functions.totalSupply().call()
