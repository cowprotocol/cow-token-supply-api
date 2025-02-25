from datetime import datetime, UTC
from helpers import fetch_token_metadata
from cfg import (
    TOKEN_CONTRACT,
    COW_DAO_TREASURY_ADDRESS,
    VESTING_SCHEDULES,
    MAX_TOTAL_SUPPLY,
)


def calulate_circulating_tokens_amount() -> int:
    # Go through every vesting schedule and calculate number of tokens vested
    total_locked: int = 0
    for vesting_schedule in VESTING_SCHEDULES:
        vested = vesting_schedule.vesting_model(
            vesting_schedule.full_amount,
            vesting_schedule.vesting_start,
            vesting_schedule.vesting_duration,
            datetime.now(UTC),
            None,
        )
        print(
            f"[{vesting_schedule.name}] full_amount: {vesting_schedule.full_amount} vested: {vested}"
        )
        total_locked += vesting_schedule.full_amount - vested

    # Fetch amount of tokens in the Treasury
    balance, max_supply = fetch_token_metadata(TOKEN_CONTRACT, COW_DAO_TREASURY_ADDRESS)

    return max_supply - balance - total_locked


if __name__ == "__main__":
    amount = calulate_circulating_tokens_amount()
    print(f"Total: {MAX_TOTAL_SUPPLY}, Circulating: {amount}")
