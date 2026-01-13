import os
import json
from collections import defaultdict
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "daily")


def load_days(days=7):
    records = []
    today = datetime.now()

    for i in range(days):
        date = today - timedelta(days=i)
        file_path = os.path.join(DATA_DIR, date.strftime("%Y-%m-%d") + ".json")

        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                records.append(json.load(f))

    return records


def aggregate(records):
    expense = defaultdict(float)
    income = defaultdict(float)
    total_expense = 0.0
    total_income = 0.0

    for day in records:
        for acc in ("wallet", "bkash"):
            for row in day.get(acc, {}).get("money_out", []):
                expense[row["category"]] += row["amount"]
                total_expense += row["amount"]

            for row in day.get(acc, {}).get("money_in", []):
                income[row["category"]] += row["amount"]
                total_income += row["amount"]

    return expense, income, total_expense, total_income


def generate_insights(expense, income, total_expense, total_income):
    insights = {}

    if expense:
        max_exp = max(expense, key=expense.get)
        min_exp = min(expense, key=expense.get)

        insights["highest_expense_category"] = (max_exp, expense[max_exp])
        insights["lowest_expense_category"] = (min_exp, expense[min_exp])
    else:
        insights["highest_expense_category"] = None
        insights["lowest_expense_category"] = None

    if income:
        top_income = max(income, key=income.get)
        insights["top_income_source"] = (top_income, income[top_income])
    else:
        insights["top_income_source"] = None

    insights["total_expense"] = total_expense
    insights["total_income"] = total_income
    insights["net_balance"] = total_income - total_expense

    return insights


def weekly_analysis():
    records = load_days(7)
    expense, income, te, ti = aggregate(records)
    return generate_insights(expense, income, te, ti)


def monthly_analysis():
    records = load_days(30)
    expense, income, te, ti = aggregate(records)
    return generate_insights(expense, income, te, ti)
