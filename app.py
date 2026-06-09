from flask import Flask, render_template, jsonify, request
from data_fetcher import get_candles
from signal_engine import generate_signal
from request_tracker import (
    can_make_request,
    record_request,
    get_remaining_requests
)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/requests")
def requests_status():
    return jsonify({
        "remaining": get_remaining_requests()
    })


@app.route("/api/signal")
def signal():

    pair = request.args.get("pair", "EUR/USD")
    timeframe = request.args.get("timeframe", "1min")

    if not can_make_request():
        return jsonify({
            "signal": "DAILY LIMIT CROSSED",
            "confidence": 0,
            "trend": "STOPPED",
            "remaining": 0
        })

    candles = get_candles(pair, timeframe)

    result = generate_signal(candles)

    record_request()

    result["remaining"] = get_remaining_requests()

    return jsonify(result)


@app.route("/health")
def health():
    return jsonify({
        "status": "healthy"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
