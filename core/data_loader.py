import json
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "daily")


def load_day(date_str):
    """Load a single day's data"""
    file_path = os.path.join(DATA_DIR, f"{date_str}.json")
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_range(start_date, end_date):
    """Load data between two dates (inclusive)"""
    results = []
    current = start_date

    while current <= end_date:
        date_str = current.strftime("%Y-%m-%d")
        data = load_day(date_str)
        if data:
            results.append(data)
        current = current.replace(day=current.day + 1)

    return results


def list_all_days():
    """Return all available dates"""
    if not os.path.exists(DATA_DIR):
        return []

    files = os.listdir(DATA_DIR)
    dates = []

    for f in files:
        if f.endswith(".json"):
            try:
                dates.append(datetime.strptime(f[:-5], "%Y-%m-%d"))
            except:
                pass

    return sorted(dates)
