import tkinter as tk
import os
import json
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data", "daily")
PDF_DIR = os.path.join(BASE_DIR, "reports", "pdf")

class HistoryPage(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.title("History")
        self.geometry("400x500")

        tk.Label(self, text="History",
                 font=("Segoe UI", 16, "bold")).pack(pady=10)

        self.listbox = tk.Listbox(self)
        self.listbox.pack(fill="both", expand=True, padx=10, pady=10)

        self.load_dates()
        self.listbox.bind("<Double-Button-1>", self.open_pdf)

    def load_dates(self):
        if not os.path.exists(DATA_DIR):
            return
        for f in sorted(os.listdir(DATA_DIR), reverse=True):
            if f.endswith(".json"):
                self.listbox.insert("end", f.replace(".json", ""))

    def open_pdf(self, _):
        date = self.listbox.get(self.listbox.curselection())
        pdf_path = os.path.join(PDF_DIR, f"{date}.pdf")

        if os.path.exists(pdf_path):
            subprocess.Popen(pdf_path, shell=True)
