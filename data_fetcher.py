import os
import requests
import pandas as pd

API_KEY = os.getenv("TWELVE_DATA_API_KEY")

BASE_URL = "https://api.twelvedata.com/time_series"


def convert_pair(pair):

    pair = pair.upper().replace("/", "")

    mapping = {
        "EURUSD": "EUR/USD",
        "AUDUSD": "AUD/USD"
    }

    return mapping.get(pair, "EUR/USD")


def get_candles(pair="EUR/USD", timeframe="1min"):

    symbol = convert_pair(pair)

    params = {
        "symbol": symbol,
        "interval": timeframe,
        "outputsize": 100,
        "apikey": API_KEY,
        "format": "JSON"
    }

    response = requests.get(
        BASE_URL,
        params=params,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    if "values" not in data:
        raise Exception(
            f"Invalid API response: {data}"
        )

    df = pd.DataFrame(data["values"])

    df = df.rename(columns={
        "datetime": "time"
    })

    numeric_cols = [
        "open",
        "high",
        "low",
        "close"
    ]

    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col])

    df = df.sort_values("time")

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df
