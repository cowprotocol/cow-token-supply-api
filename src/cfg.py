import logging
from enum import Enum
from datetime import datetime, timedelta, UTC

from eth_typing import Address

from rpc import ERC20
from models import Treasury, VestingSchedule, Token
from vesting import linear_vesting

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)


# add all different chains for token here
class TOKENS(Enum):
    COW_MAINNET = Token(
        rpc_type=ERC20,
        token_contract=Address(
            bytes.fromhex("0xDEf1CA1fb7FBcDC777520aa7f396b4E015F497aB"[2:])
        ),
        include_in_max_supply=True,
    )


# add all treasuries here
class TREASURIES(Enum):
    COW_DAO_TREASURY_MAINNET = Treasury(
        token=TOKENS.COW_MAINNET.value,
        treasury_addess=Address(
            bytes.fromhex("0xcA771eda0c70aA7d053aB1B25004559B918FE662"[2:])
        ),
    )


# add all vesting schedules here
VESTING_SCHEDULES: list[VestingSchedule] = [
    VestingSchedule(
        name="CoW Protocol Virtual Token ETH",
        vesting_start=datetime.fromtimestamp(1644609915, tz=UTC),
        vesting_duration=timedelta(days=365 * 4 + 1),
        # Initial balance top up tx https://etherscan.io/tx/0x1100cd4a50a2c224ec39f861aef7574df394edb2b5ed850705cf0bb34f6a300d
        full_amount=439952166809283833193827347,
        vesting_model=linear_vesting,
    ),
    VestingSchedule(
        name="CoW Protocol Virtual Token GNOSIS",
        vesting_start=datetime.fromtimestamp(1644610920, tz=UTC),
        vesting_duration=timedelta(days=365 * 4 + 1),
        # TODO: find original transaction and adjust the amount
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
