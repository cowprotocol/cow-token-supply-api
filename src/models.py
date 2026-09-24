from typing import Optional, Any
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections.abc import Callable

from eth_typing import Address

@dataclass
class Token:
    token_contract: Address
    rpc_url_env_var: str
    include_in_max_supply: bool


@dataclass
class Treasury:
    token: Any  # To accept ENUM we keep it Any, but TOKENS ENUM literal is expected
    treasury_addess: Address


@dataclass
class SolverBond:
    """Wallet that holds bonded COW as solver collateral.

    Funds here are not slashable on-chain by the protocol but are committed
    against solver misbehaviour and therefore not part of the freely
    circulating supply.
    """

    token: Any
    bond_address: Address


@dataclass
class StakingContract:
    """Contract custodying COW staked under a future staking program.

    Balances held here are excluded from circulating supply because the
    underlying COW is locked until the staker exits.
    """

    token: Any
    contract_address: Address


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
