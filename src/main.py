from datetime import datetime, UTC
from flask import Flask, jsonify
import logging
from helpers import fetch_token_metadata
from cfg import TOKEN_CONTRACT, COW_DAO_TREASURY_ADDRESS, VESTING_SCHEDULES

app = Flask(__name__)

logger = logging.getLogger(__name__)


def calulate_circulating_and_max_tokens_amount() -> tuple[int, int]:
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

    # Fetch amount of tokens in the Treasury
    balance, max_supply = fetch_token_metadata(TOKEN_CONTRACT, COW_DAO_TREASURY_ADDRESS)

    return max_supply - balance - total_locked, max_supply


@app.route("/supply")
def supply():
    circulating, max_supply = calulate_circulating_and_max_tokens_amount()
    logger.info(str({"total": max_supply, "circulating": circulating}))
    return jsonify({"total": max_supply, "circulating": circulating})


if __name__ == "__main__":
    from waitress import (
        serve,
    )  # Do we need this together with nginx? Cant we do just app.run()?

    serve(app, host="0.0.0.0", port=8080)
