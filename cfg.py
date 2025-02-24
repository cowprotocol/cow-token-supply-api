import os

from datetime import datetime, timedelta, UTC

from dotenv import load_dotenv
from eth_typing import Address, ABI

from vesting import VestingSchedule, linear_vesting

load_dotenv()


# Replace with your QuickNode RPC URL
QUICKNODE_RPC_URL = os.environ["QUICKNODE_RPC_URL"]

# Some constants
TOKEN_CONTRACT: Address = Address(bytes.fromhex("0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB"[2:]))
COW_DAO_TREASURY_ADDRESS: Address = Address(bytes.fromhex("0xcA771eda0c70aA7d053aB1B25004559B918FE662"[2:]))
MAX_TOTAL_SUPPLY: int = int(10**27)


# Minimal ERC20 ABI for balanceOf function
ERC20_ABI: ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function"
    }
]


# add all vesting schedules here
VESTING_SCHEDULES: list[VestingSchedule] = [
    VestingSchedule(
        name="GnosisDAO",
        vesting_start=datetime(year=2022, month=1, day=1, tzinfo=UTC),
        vesting_duration=timedelta(days=365*4),
        full_amount=8 * 10**24,
        vesting_model=linear_vesting
    )
]
