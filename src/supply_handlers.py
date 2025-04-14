import logging
from datetime import datetime, UTC

from models import Token, AbstractRpc
from cfg import VESTING_SCHEDULES, TREASURIES, TOKENS


logger = logging.getLogger(__name__)


def get_locked_supply():
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
    max_supply: int, treasury_supply: int, locked_supply: int
) -> int:
    return max_supply - treasury_supply - locked_supply


def get_max_supply() -> int:
    return sum(
        token.value.rpc_type(token.value.token_contract).get_total_supply()
        for token in TOKENS
        if token.value.include_in_max_supply
    )


def get_treasury_supply() -> int:
    # Added deduplication of clients as duplicate clients caused frequent RPC errors
    # In future this should be rolled out on all RPC interactions
    rpc_client_per_token: dict[str, AbstractRpc] = dict()

    result: int = 0
    for treasury in TREASURIES:
        token_name = treasury.value.token.name
        token: Token = treasury.value.token.value
        rpc_client = (
            token.rpc_type(token.token_contract)
            if token_name not in rpc_client_per_token
            else rpc_client_per_token[token_name]
        )
        rpc_client_per_token[token_name] = rpc_client
        result += rpc_client.get_balance_of(treasury.value.treasury_addess)
    return result


def supply_handler() -> dict[str, str]:
    max_supply: int = get_max_supply()
    locked_supply: int = get_locked_supply()
    treasury_supply: int = get_treasury_supply()

    circulating_supply: int = get_circulating_supply(
        max_supply, treasury_supply, locked_supply
    )

    return {"total": str(max_supply), "circulating": str(circulating_supply)}
