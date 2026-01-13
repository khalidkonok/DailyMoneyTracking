import tkinter as tk
from datetime import datetime
import os
import sys

from core.storage import save_today, get_previous_balances, load_day
from core.pdf_report import generate_pdf
from ui.dashboard import Account
from ui.history import HistoryPage
from ui.analysis import AnalysisPage

BG = "#F4F7FB"
PRIMARY = "#1F4FD8"

if getattr(sys, "frozen", False):
    BASE_DIR = os.path.join(os.getenv("LOCALAPPDATA"), "DailyMoneyTracking")
else:
    BASE_DIR = os.path.dirname(__file__)
PDF_DIR = os.path.join(BASE_DIR, "reports", "pdf")
os.makedirs(PDF_DIR, exist_ok=True)

class App:
    def __init__(self, root):
        self.root = root

        # Window
        root.title("Daily Money Tracking")
        root.geometry("1200x720")
        root.configure(bg=BG)

        # Top bar
        top = tk.Frame(root, bg=BG)
        top.pack(fill="x", padx=20, pady=10)
        tk.Label(top, text="Daily Money Tracking", bg=BG, fg=PRIMARY,
                 font=("Segoe UI", 20, "bold")).pack(side="top")
        tk.Button(top, text="History", command=self.open_history).pack(side="right", padx=5)
        tk.Button(top, text="Monthly Analysis", command=lambda: self.open_analysis("monthly")).pack(side="right", padx=5)
        tk.Button(top, text="Weekly Analysis", command=lambda: self.open_analysis("weekly")).pack(side="right", padx=5)

        # Date
        tk.Label(root, text=datetime.now().strftime("%A, %d %B %Y"),
                 bg=BG, fg="#666", font=("Segoe UI", 10)).pack(pady=(0,10))

        # Body
        body = tk.Frame(root, bg=BG)
        body.pack(fill="both", expand=True, padx=20)
        left = tk.Frame(body, bg=BG)
        right = tk.Frame(body, bg=BG)
        left.pack(side="left", fill="both", expand=True)
        right.pack(side="right", fill="both", expand=True)

        # Accounts
        self.wallet = Account(left, "Wallet – Fiat : Cash", self.save)
        self.bkash = Account(right, "bKash – Fiat : Digital", self.save)

        # Load today data or initialize
        today_str = datetime.now().strftime("%Y-%m-%d")
        self.today_data = load_day(today_str)
        if not self.today_data:
            wallet_ob, bkash_ob = get_previous_balances()
            self.today_data = {
                "date": today_str,
                "wallet": {
                    "opening_balance": wallet_ob,
                    "money_in": [],
                    "money_out": [],
                    "remaining_balance": wallet_ob
                },
                "bkash": {
                    "opening_balance": bkash_ob,
                    "money_in": [],
                    "money_out": [],
                    "remaining_balance": bkash_ob
                }
            }
            save_today(self.today_data)

        # Load previous balances
        self.wallet.load_ob(self.today_data["wallet"]["opening_balance"])
        self.bkash.load_ob(self.today_data["bkash"]["opening_balance"])

        # Populate tables if any
        self.populate_table(self.wallet.inp, self.today_data["wallet"]["money_in"])
        self.populate_table(self.wallet.out, self.today_data["wallet"]["money_out"])
        self.populate_table(self.bkash.inp, self.today_data["bkash"]["money_in"])
        self.populate_table(self.bkash.out, self.today_data["bkash"]["money_out"])

        root.protocol("WM_DELETE_WINDOW", self.on_close)

    def populate_table(self, table, data_list):
        for entry in data_list:
            row = table.rows[-1]
            row[0].insert(0, entry["category"])
            row[1].insert(0, str(entry["amount"]))
            table.add_row()
        table.calculate()

    def save(self):
        self.today_data = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "wallet": self.wallet.export(),
            "bkash": self.bkash.export()
        }
        save_today(self.today_data)

    def on_close(self):
        self.save()
        if self.today_data:
            pdf_path = os.path.join(PDF_DIR, f"{self.today_data['date']}.pdf")
            generate_pdf(self.today_data, pdf_path)
        self.root.destroy()

    def open_history(self):
        HistoryPage(self.root)

    def open_analysis(self, mode):
        AnalysisPage(self.root, mode)

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
