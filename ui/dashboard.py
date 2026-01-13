import tkinter as tk

CARD = "#FFFFFF"
PRIMARY = "#1F4FD8"

class EditableTable:
    def __init__(self, parent, title, on_change):
        self.on_change = on_change
        self.rows = []

        frame = tk.Frame(parent, bg=CARD, padx=10, pady=10)
        frame.pack(fill="x", pady=6)

        tk.Label(frame, text=title, bg=CARD, fg=PRIMARY,
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")

        header = tk.Frame(frame, bg=CARD)
        header.pack()
        tk.Label(header, text="Category", width=28, bg=CARD).grid(row=0, column=0)
        tk.Label(header, text="Amount (BDT)", width=14, bg=CARD).grid(row=0, column=1)

        self.body = tk.Frame(frame, bg=CARD)
        self.body.pack()

        # Total row
        self.total_var = tk.StringVar(value="0.00")
        total_row = tk.Frame(frame, bg=CARD)
        total_row.pack(anchor="e", pady=(4,0))
        tk.Label(total_row, text="Total:", bg=CARD, fg=PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Label(total_row, textvariable=self.total_var, bg=CARD, fg=PRIMARY,
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(4,0))

        self.add_row()

    def add_row(self):
        r = len(self.rows)
        cat = tk.Entry(self.body, width=30)
        amt = tk.Entry(self.body, width=16)
        cat.grid(row=r, column=0, pady=3, padx=(0,5))
        amt.grid(row=r, column=1, pady=3)
        cat.bind("<Return>", lambda e: amt.focus())
        amt.bind("<Return>", lambda e: self.finish())
        self.rows.append((cat, amt))

    def finish(self):
        self.calculate()
        self.add_row()
        self.rows[-1][0].focus()

    def calculate(self):
        total = 0.0
        for _, amt in self.rows:
            try:
                total += float(amt.get())
            except:
                pass
        self.total_var.set(f"{total:.2f}")
        self.on_change()

    def total(self):
        try:
            return float(self.total_var.get())
        except:
            return 0.0

    def export(self):
        data = []
        for c, a in self.rows:
            if c.get() and a.get():
                try:
                    data.append({"category": c.get(), "amount": float(a.get())})
                except:
                    pass
        return data

class Account:
    def __init__(self, parent, title, save_cb):
        self.save_cb = save_cb
        self.ob_manual = False

        box = tk.Frame(parent, bg=CARD, padx=12, pady=12)
        box.pack(fill="both", expand=True, padx=5)

        tk.Label(box, text=title, bg=CARD, fg=PRIMARY,
                 font=("Segoe UI", 13, "bold")).pack(anchor="w")

        # Opening Balance
        ob_row = tk.Frame(box, bg=CARD)
        ob_row.pack(anchor="w", pady=5)
        tk.Label(ob_row, text="Opening Balance:", bg=CARD).pack(side="left")
        self.ob = tk.StringVar(value="0.00")
        e = tk.Entry(ob_row, textvariable=self.ob, width=14)
        e.pack(side="left", padx=5)
        e.bind("<KeyRelease>", self.manual)

        # Tables
        self.out = EditableTable(box, "Money Out", self.update)
        self.inp = EditableTable(box, "Money In", self.update)

        # Remaining Balance
        self.rb = tk.StringVar(value="0.00")
        rb_row = tk.Frame(box, bg=CARD)
        rb_row.pack(anchor="e", pady=(6,0))
        tk.Label(rb_row, text="Remaining Balance:", bg=CARD, fg=PRIMARY,
                 font=("Segoe UI", 11, "bold")).pack(side="left")
        tk.Label(rb_row, textvariable=self.rb, bg=CARD, fg=PRIMARY,
                 font=("Segoe UI", 11, "bold")).pack(side="left", padx=(6,0))

    def manual(self, _=None):
        self.ob_manual = True
        self.update()

    def update(self):
        try:
            ob = float(self.ob.get())
        except:
            ob = 0.0
        rb = ob + self.inp.total() - self.out.total()
        self.rb.set(f"{rb:.2f}")
        self.save_cb()

    def load_ob(self, amount):
        if not self.ob_manual:
            self.ob.set(f"{amount:.2f}")
            self.update()

    def export(self):
        return {
            "opening_balance": float(self.ob.get() or 0),
            "money_in": self.inp.export(),
            "money_out": self.out.export(),
            "remaining_balance": float(self.rb.get() or 0)
        }
