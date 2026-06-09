import json
import os
from datetime import datetime

DATA_DIR = "data"
REQUESTS_FILE = os.path.join(DATA_DIR, "requests.json")

DAILY_LIMIT = 800


def ensure_file():

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    if not os.path.exists(REQUESTS_FILE):
        save_data({
            "date": current_date(),
            "used": 0
        })


def current_date():
    return datetime.utcnow().strftime("%Y-%m-%d")


def load_data():

    ensure_file()

    with open(REQUESTS_FILE, "r") as f:
        return json.load(f)


def save_data(data):

    with open(REQUESTS_FILE, "w") as f:
        json.dump(data, f, indent=2)


def reset_if_new_day():

    data = load_data()

    if data["date"] != current_date():

        data = {
            "date": current_date(),
            "used": 0
        }

        save_data(data)

    return data


def get_used_requests():

    data = reset_if_new_day()
    return data["used"]


def get_remaining_requests():

    used = get_used_requests()
    remaining = DAILY_LIMIT - used

    if remaining < 0:
        remaining = 0

    return remaining


def can_make_request():

    return get_remaining_requests() > 0


def record_request():

    data = reset_if_new_day()

    data["used"] += 1

    if data["used"] > DAILY_LIMIT:
        data["used"] = DAILY_LIMIT

    save_data(data)
