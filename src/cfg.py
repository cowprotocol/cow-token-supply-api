import logging
from enum import Enum
from datetime import datetime, timedelta, UTC

from eth_typing import Address

from rpc import MainnetERC20
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
        rpc_type=MainnetERC20,
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
        # https://etherscan.io/tx/0x1100cd4a50a2c224ec39f861aef7574df394edb2b5ed850705cf0bb34f6a300d
        full_amount=439952166809283833193827347,
        vesting_model=linear_vesting,
    ),
    VestingSchedule(
        name="CoW Protocol Virtual Token GNOSIS",
        vesting_start=datetime.fromtimestamp(1644610920, tz=UTC),
        vesting_duration=timedelta(days=365 * 4 + 1),
        # https://gnosisscan.io/tx/0x3cb8cf2affc63d897e9efa9882a194a1ce809e88be82a8cbc4bc63eed897550e
        full_amount=34850471096742687083022409,
        vesting_model=linear_vesting,
    ),
    VestingSchedule(
        name="GNOSIS DAO allocation ETH",
        vesting_start=datetime.fromtimestamp(1644584715, tz=UTC),
        vesting_duration=timedelta(days=365 * 4),
        # https://etherscan.io/tx/0x0e105389f5bc8ded16723ac44e231a8e484eab28da4113a8fd3892624a364882
        full_amount=41894957000000000000000000,
        vesting_model=linear_vesting,
    ),
]
