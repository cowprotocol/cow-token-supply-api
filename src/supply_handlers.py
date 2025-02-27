import logging
from datetime import datetime, UTC

from cfg import VESTING_SCHEDULES, TREASURIES, TOKENS, Treasury


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
    return sum(
        treasury.value.token.rpc_type(
            treasury.value.token.token_contract
        ).get_balance_of(treasury.value.treasury_addess)
        for treasury in TREASURIES
    )


def supply_handler() -> dict[str, int]:
    max_supply: int = get_max_supply()
    locked_supply: int = get_locked_supply()
    treasury_supply: int = get_treasury_supply()

    circulating_supply: int = get_circulating_supply(
        max_supply, treasury_supply, locked_supply
    )

    return {"total": max_supply, "circulating": circulating_supply}
