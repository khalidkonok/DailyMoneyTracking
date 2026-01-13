import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from core.analysis_engine import load_days, aggregate
from core.pdf_report import generate_period_pdf


class AnalysisPage:
    def __init__(self, root, mode):
        self.root = root
        self.mode = mode  # "weekly" or "monthly"

        self.window = tk.Toplevel(root)
        self.window.title(f"{mode.capitalize()} Analysis")
        self.window.geometry("900x650")
        self.window.configure(bg="#F4F7FB")

        # -------- Load Data --------
        days = 7 if mode == "weekly" else 30
        raw_data = load_days(days)

        if not raw_data:
            messagebox.showwarning(
                "No Data",
                f"No data found for {mode} analysis."
            )
            self.window.destroy()
            return

        expense, income, total_expense, total_income = aggregate(raw_data)

        # -------- Header --------
        title = tk.Label(
            self.window,
            text=f"{mode.capitalize()} Financial Analysis",
            font=("Segoe UI", 18, "bold"),
            fg="#1F4FD8",
            bg="#F4F7FB"
        )
        title.pack(pady=10)

        summary = tk.Label(
            self.window,
            text=(
                f"Total Income: {total_income:.2f} BDT\n"
                f"Total Expense: {total_expense:.2f} BDT\n"
                f"Net Balance: {(total_income - total_expense):.2f} BDT"
            ),
            font=("Segoe UI", 11),
            bg="#F4F7FB"
        )
        summary.pack(pady=10)

        # -------- Charts --------
        chart_frame = tk.Frame(self.window, bg="#F4F7FB")
        chart_frame.pack(fill="both", expand=True, padx=20)

        if expense:
            self.draw_chart(
                chart_frame,
                expense,
                "Expense Breakdown"
            )

        if income:
            self.draw_chart(
                chart_frame,
                income,
                "Income Breakdown"
            )

        # -------- PDF Button --------
        pdf_btn = ttk.Button(
            self.window,
            text=f"Generate {mode.capitalize()} PDF Report",
            command=lambda: self.generate_pdf(
                expense,
                income,
                total_expense,
                total_income
            )
        )
        pdf_btn.pack(pady=15)

    # ----------------- CHART -----------------
    def draw_chart(self, parent, data, title):
        fig, ax = plt.subplots(figsize=(4.5, 4.5))
        ax.pie(
            data.values(),
            labels=data.keys(),
            autopct="%1.1f%%",
            startangle=90
        )
        ax.set_title(title)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(side="left", expand=True, padx=10)

    # ----------------- PDF -----------------
    def generate_pdf(self, expense, income, total_exp, total_inc):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        pdf_dir = os.path.join(base_dir, "reports", "pdf")
        os.makedirs(pdf_dir, exist_ok=True)

        filename = (
            f"{self.mode}_report_"
            f"{datetime.now().strftime('%Y-%m-%d')}.pdf"
        )
        output_path = os.path.join(pdf_dir, filename)

        generate_period_pdf(
            self.mode,
            None,
            expense,
            income,
            total_exp,
            total_inc,
            output_path
        )

        messagebox.showinfo(
            "PDF Generated",
            f"{self.mode.capitalize()} report saved successfully.\n\n{output_path}"
        )
