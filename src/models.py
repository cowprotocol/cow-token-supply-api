from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections.abc import Callable

from eth_typing import Address

from rpc import AbstractRpc


@dataclass
class Token:
    token_contract: Address
    rpc_type: type[AbstractRpc]
    include_in_max_supply: bool


@dataclass
class Treasury:
    token: Any  # To accept ENUM we keep it Any, but TOKENS ENUM literal is expected
    treasury_addess: Address


_VESTING_MODEL_SIGNATURE = Callable[
    [int, datetime, timedelta, datetime, Optional[timedelta]], int
]


@dataclass
class VestingSchedule:
    name: str
    vesting_start: datetime
    vesting_duration: timedelta
    full_amount: int
    vesting_model: _VESTING_MODEL_SIGNATURE
