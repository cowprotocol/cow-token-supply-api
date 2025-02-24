from datetime import datetime, UTC
from helpers import check_token_balance
from cfg import TOKEN_CONTRACT, COW_DAO_TREASURY_ADDRESS, VESTING_SCHEDULES, MAX_TOTAL_SUPPLY


def calulate_circulating_tokens_amount() -> int:
    # Go through every vesting schedule and calculate number of tokens vested
    total_vested: int = 0
    for vesting_schedule in VESTING_SCHEDULES:
        vested = vesting_schedule.vesting_model(
            vesting_schedule.full_amount,
            vesting_schedule.vesting_start,
            vesting_schedule.vesting_duration,
            datetime.now(UTC),
            None
        )
        print(f"[{vesting_schedule.name}] full_amount: {vesting_schedule.full_amount} vested: {vested}")
        total_vested += vested

    # Fetch amount of tokens in the Treasury
    balance = check_token_balance(
        TOKEN_CONTRACT,
        COW_DAO_TREASURY_ADDRESS
    )

    return MAX_TOTAL_SUPPLY - balance - total_vested




if __name__ == "__main__":
    amount = calulate_circulating_tokens_amount()
    print(f"Total: {MAX_TOTAL_SUPPLY}, Circulating: {amount}")
