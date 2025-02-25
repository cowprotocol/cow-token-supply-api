from web3 import Web3
from eth_typing import Address, ABI

from cfg import QUICKNODE_RPC_URL, ERC20_ABI


def fetch_token_metadata(
    token_contract: Address,
    wallet_address: Address,
    rpc_url: str = QUICKNODE_RPC_URL,
    abi: ABI = ERC20_ABI,
) -> tuple[int, int]:
    """
    Fetch token metadata including balance and total supply
    Returns a tuple of (balance, total_supply)
    """
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(rpc_url))

    # Verify connection
    if not w3.is_connected():
        raise Exception("Failed to connect to QuickNode RPC")

    # Create contract instance
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(token_contract), abi=abi
    )

    # Get balance
    balance = contract.functions.balanceOf(
        Web3.to_checksum_address(wallet_address)
    ).call()

    # Get total supply (doesn't need wallet address)
    total_supply = contract.functions.totalSupply().call()

    return balance, total_supply
