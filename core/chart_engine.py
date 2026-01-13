import matplotlib.pyplot as plt

def expense_pie(expense_data, title):
    categories = list(expense_data.keys())
    amounts = list(expense_data.values())

    if not categories:
        return None

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.pie(amounts, labels=categories, autopct="%1.1f%%", startangle=90)
    ax.set_title(title)
    return fig


def income_bar(income_data, title):
    categories = list(income_data.keys())
    amounts = list(income_data.values())

    if not categories:
        return None

    fig, ax = plt.subplots(figsize=(5, 4))
    ax.bar(categories, amounts)
    ax.set_title(title)
    ax.set_ylabel("Amount (BDT)")
    ax.tick_params(axis="x", rotation=45)
    return fig
