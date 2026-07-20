import logging
from enum import Enum
from datetime import datetime, UTC

from models import Token
from rpc import EvmERC20
from cfg import VESTING_SCHEDULES, TREASURIES, BONDS, STAKING_CONTRACTS, TOKENS


logger = logging.getLogger(__name__)


def get_locked_supply() -> int:
    # Go through every vesting schedule and calculate total number of tokens that are not vested yet.
    total_locked: int = 0
    for vesting_schedule in VESTING_SCHEDULES:
        vested = vesting_schedule.vesting_model(
            vesting_schedule.full_amount,
            vesting_schedule.vesting_start,
            vesting_schedule.vesting_duration,
            datetime.now(UTC),
            None,
        )
        logger.debug(
            "[%s] full_amount: %s vested: %s",
            vesting_schedule.name,
            vesting_schedule.full_amount,
            vested,
        )
        total_locked += vesting_schedule.full_amount - vested

    return total_locked


def get_circulating_supply(
    max_supply: int,
    treasury_supply: int,
    locked_supply: int,
    bond_supply: int,
    staked_supply: int,
) -> int:
    return (
        max_supply
        - treasury_supply
        - locked_supply
        - bond_supply
        - staked_supply
    )


def get_max_supply() -> int:
    return sum(
        EvmERC20(
            token.value.token_contract, token.value.rpc_url_env_var
        ).get_total_supply()
        for token in TOKENS
        if token.value.include_in_max_supply
    )


def _sum_balances(holders: type[Enum], address_attr: str) -> int:
    """Sum ERC20 balances across an enum of holders.

    One RPC client per (chain, token) pair is reused to limit connection
    overhead — historically duplicate clients caused frequent RPC errors.
    """
    rpc_client_cache: dict[str, EvmERC20] = dict()
    result: int = 0
    for holder in holders:
        token_name = holder.value.token.name
        token: Token = holder.value.token.value
        rpc_client = rpc_client_cache.get(token_name) or EvmERC20(
            token.token_contract, token.rpc_url_env_var
        )
        rpc_client_cache[token_name] = rpc_client
        holder_address = getattr(holder.value, address_attr)
        result += rpc_client.get_balance_of(holder_address)
    return result


def get_treasury_supply() -> int:
    return _sum_balances(TREASURIES, "treasury_addess")


def get_bond_supply() -> int:
    return _sum_balances(BONDS, "bond_address")


def get_staked_supply() -> int:
    return _sum_balances(STAKING_CONTRACTS, "contract_address")


def format_token_amount(amount: int) -> str:
    """Convert from wei (10^18) to native token amounts and format as string."""
    decimals = 10**18
    return f"{amount / decimals:.18f}".rstrip('0').rstrip('.')


def supply_handler() -> dict[str, str]:
    max_supply: int = get_max_supply()
    locked_supply: int = get_locked_supply()
    treasury_supply: int = get_treasury_supply()
    bond_supply: int = get_bond_supply()
    staked_supply: int = get_staked_supply()

    circulating_supply: int = get_circulating_supply(
        max_supply,
        treasury_supply,
        locked_supply,
        bond_supply,
        staked_supply,
    )

    return {
        "total": format_token_amount(max_supply),
        "circulating": format_token_amount(circulating_supply),
        "treasury": format_token_amount(treasury_supply),
        "locked": format_token_amount(locked_supply),
        "bonds": format_token_amount(bond_supply),
        "staked": format_token_amount(staked_supply),
    }
