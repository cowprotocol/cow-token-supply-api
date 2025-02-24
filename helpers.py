from web3 import Web3
from eth_typing import Address, ABI

from cfg import QUICKNODE_RPC_URL, ERC20_ABI


def check_token_balance(
        token_contract: Address,
        wallet_address: Address,
        rpc_url: str=QUICKNODE_RPC_URL,
        abi: ABI=ERC20_ABI
    ) -> int:
    """
    Check the token balance for the specified wallet address
    Returns the balance as a float
    """
    # Initialize Web3
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    # Verify connection
    if not w3.is_connected():
        raise Exception("Failed to connect to QuickNode RPC")

    # Create contract instance
    contract = w3.eth.contract(
        address=Web3.to_checksum_address(token_contract),
        abi=abi
    )
    
    # Get balance
    raw_balance = contract.functions.balanceOf(
        Web3.to_checksum_address(wallet_address)
    ).call()
    
    return raw_balance
