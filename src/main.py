import logging

from flask import Flask, jsonify, request

from rpc import AbstractRpc
from supply_handlers import supply_handler

app = Flask(__name__)

logger = logging.getLogger(__name__)


_SCALAR_QUERY_KEYS = {"total", "circulating", "treasury", "locked", "bonds", "staked"}


@app.route("/supply")
def supply():
    try:
        response = supply_handler()
    except AbstractRpc.RpcConnectionError:
        return (
            jsonify({"error": "Rpc connection failed, please retry the request"}),
            503,
        )

    query_param = request.args.get('q')

    if query_param in _SCALAR_QUERY_KEYS:
        value = response[query_param]
        logger.info(f"{query_param} supply: {value}")
        return value, 200
    else:
        logger.info(str(response))
        return jsonify(response), 200


if __name__ == "__main__":
    from waitress import (
        serve,
    )  # Do we need this together with nginx? Cant we do just app.run()?

    serve(app, host="0.0.0.0", port=8080)
