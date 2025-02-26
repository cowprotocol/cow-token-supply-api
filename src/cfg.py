import os
import logging
from datetime import datetime, timedelta, UTC

from dotenv import load_dotenv
from eth_typing import Address, ABI

from vesting import VestingSchedule, linear_vesting

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

# Replace with your QuickNode RPC URL
RPC_URL = os.environ["RPC_URL"]

# Some constants
TOKEN_CONTRACT: Address = Address(
    bytes.fromhex("0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB"[2:])
)
COW_DAO_TREASURY_ADDRESS: Address = Address(
    bytes.fromhex("0xcA771eda0c70aA7d053aB1B25004559B918FE662"[2:])
)


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


# add all vesting schedules here
VESTING_SCHEDULES: list[VestingSchedule] = [
    VestingSchedule(
        name="CoW Protocol Virtual Token ETH",
        vesting_start=datetime.fromtimestamp(1644609915, tz=UTC),
        vesting_duration=timedelta(days=365 * 4 + 1),
        full_amount=191370151938368622968421015,
        vesting_model=linear_vesting,
    ),
    VestingSchedule(
        name="CoW Protocol Virtual Token GNOSIS",
        vesting_start=datetime.fromtimestamp(1644610920, tz=UTC),
        vesting_duration=timedelta(days=365 * 4 + 1),
        full_amount=8818826428106585592815710,
        vesting_model=linear_vesting,
    ),
    VestingSchedule(
        name="GNOSIS DAO allocation ETH",
        vesting_start=datetime.fromtimestamp(1644584715, tz=UTC),
        vesting_duration=timedelta(days=365 * 4),
        full_amount=41894957000000000000000000,
        vesting_model=linear_vesting,
    ),
]
