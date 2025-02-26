from web3 import Web3
from eth_typing import Address, ABI
import logging
from cfg import RPC_URL, ERC20_ABI

logger = logging.getLogger(__name__)


class RpcClient:
    class RpcConnectionError(Exception):
        pass

    def __init__(self, rpc_url: str = RPC_URL) -> None:
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))

        # Verify connection
        if not self.w3.is_connected():
            logger.error("Failed to connect to RPC, please retry")
            raise self.RpcConnectionError("Failed to connect to RPC, please retry")

    def balanceOf(
        self, token_contract: Address, wallet_address: Address, abi: ABI = ERC20_ABI
    ):
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_contract), abi=abi
        )
        return contract.functions.balanceOf(
            Web3.to_checksum_address(wallet_address)
        ).call()

    def totalSupply(self, token_contract: Address, abi: ABI = ERC20_ABI):
        contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(token_contract), abi=abi
        )
        return contract.functions.totalSupply().call()
