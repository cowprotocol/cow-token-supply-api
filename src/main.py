import logging

from flask import Flask, jsonify, request

from rpc import AbstractRpc
from supply_handlers import supply_handler

app = Flask(__name__)

logger = logging.getLogger(__name__)


@app.route("/supply")
def supply():
    try:
        response = supply_handler()
    except AbstractRpc.RpcConnectionError as e:
        return (
            jsonify({"error": "Rpc connection failed, please retry the request"}),
            503,
        )

    # Check for query parameter
    query_param = request.args.get('q')

    if query_param == 'total':
        logger.info(f"Total supply: {response['total']}")
        return response['total'], 200
    elif query_param == 'circulating':
        logger.info(f"Circulating supply: {response['circulating']}")
        return response['circulating'], 200
    else:
        # Default behavior - return JSON with both values
        logger.info(str(response))
        return jsonify(response), 200


if __name__ == "__main__":
    from waitress import (
        serve,
    )  # Do we need this together with nginx? Cant we do just app.run()?

    serve(app, host="0.0.0.0", port=8080)
