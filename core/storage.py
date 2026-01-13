import json
import os
from datetime import datetime, timedelta
import sys

# -----------------------------
# Use AppData folder if frozen exe, else project folder
# -----------------------------
if getattr(sys, "frozen", False):
    BASE_DIR = os.path.join(os.getenv("LOCALAPPDATA"), "DailyMoneyTracking")
else:
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DATA_DIR = os.path.join(BASE_DIR, "data", "daily")
os.makedirs(DATA_DIR, exist_ok=True)  # Ensure folder exists

# -----------------------------
# Date helpers
# -----------------------------
def today():
    return datetime.now().strftime("%Y-%m-%d")

def yesterday():
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

def daily_path(date_str):
    return os.path.join(DATA_DIR, f"{date_str}.json")

# -----------------------------
# Load a specific day's JSON
# -----------------------------
def load_day(date_str):
    path = daily_path(date_str)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return None

# -----------------------------
# Save today's data
# -----------------------------
def save_today(data):
    os.makedirs(DATA_DIR, exist_ok=True)
    path = daily_path(today())
    with open(path, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------
# Get remaining balances from yesterday
# -----------------------------
def get_previous_balances():
    y_data = load_day(yesterday())
    if not y_data:
        return 0.0, 0.0
    wallet_rb = y_data.get("wallet", {}).get("remaining_balance", 0.0)
    bkash_rb = y_data.get("bkash", {}).get("remaining_balance", 0.0)
    return wallet_rb, bkash_rb
