from datetime import datetime, UTC
from flask import Flask, jsonify
import logging
from rpc import RpcClient
from cfg import TOKEN_CONTRACT, COW_DAO_TREASURY_ADDRESS, VESTING_SCHEDULES

app = Flask(__name__)

logger = logging.getLogger(__name__)


def get_circulating_supply(rpc_client: RpcClient, max_supply: int) -> int:
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
    balance = rpc_client.balanceOf(TOKEN_CONTRACT, COW_DAO_TREASURY_ADDRESS)

    return max_supply - balance - total_locked


def supply_handler() -> dict[str, int]:
    rpc = RpcClient()
    max_supply = rpc.totalSupply(TOKEN_CONTRACT)
    circulating_supply = get_circulating_supply(rpc, max_supply)

    return {"total": max_supply, "circulating": circulating_supply}


@app.route("/supply")
def supply():
    try:
        response = supply_handler()
    except RpcClient.RpcConnectionError as e:
        return (
            jsonify({"error": "Rpc connection failed, please retry the request"}),
            503,
        )

    logger.info(str(response))

    return (
        jsonify(response),
        200,
    )


if __name__ == "__main__":
    from waitress import (
        serve,
    )  # Do we need this together with nginx? Cant we do just app.run()?

    serve(app, host="0.0.0.0", port=8080)
