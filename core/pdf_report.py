from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
import os


def generate_pdf(data, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>Daily Money Report</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f"Date: {data['date']}", styles["Normal"]))
    story.append(Spacer(1, 12))

    for acc in ["wallet", "bkash"]:
        acc_data = data[acc]

        story.append(Paragraph(acc.upper(), styles["Heading2"]))
        story.append(
            Paragraph(
                f"Opening Balance: {acc_data['opening_balance']} BDT",
                styles["Normal"]
            )
        )
        story.append(Spacer(1, 8))

        # Money Out
        story.append(Paragraph("Money Out", styles["Heading3"]))
        table_data = [["Category", "Amount (BDT)"]]
        for row in acc_data["money_out"]:
            table_data.append([row["category"], f"{row['amount']:.2f}"])
        story.append(Table(table_data))
        story.append(Spacer(1, 8))

        # Money In
        story.append(Paragraph("Money In", styles["Heading3"]))
        table_data = [["Category", "Amount (BDT)"]]
        for row in acc_data["money_in"]:
            table_data.append([row["category"], f"{row['amount']:.2f}"])
        story.append(Table(table_data))
        story.append(Spacer(1, 8))

        story.append(
            Paragraph(
                f"Remaining Balance: {acc_data['remaining_balance']} BDT",
                styles["Normal"]
            )
        )
        story.append(Spacer(1, 20))

    doc.build(story)
def generate_period_pdf(
    mode,
    data,
    expense,
    income,
    total_expense,
    total_income,
    output_path
):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(
        Paragraph(
            f"<b>{mode.capitalize()} Financial Report</b>",
            styles["Title"]
        )
    )
    story.append(Spacer(1, 12))

    # Summary
    story.append(Paragraph(
        f"Total Income: {total_income:.2f} BDT",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"Total Expense: {total_expense:.2f} BDT",
        styles["Normal"]
    ))
    story.append(Paragraph(
        f"Net Balance: {(total_income - total_expense):.2f} BDT",
        styles["Normal"]
    ))
    story.append(Spacer(1, 20))

    # Expense Table
    if expense:
        story.append(Paragraph("Expense Breakdown", styles["Heading2"]))
        table_data = [["Category", "Amount (BDT)"]]
        for k, v in expense.items():
            table_data.append([k, f"{v:.2f}"])
        story.append(Table(table_data))
        story.append(Spacer(1, 15))

    # Income Table
    if income:
        story.append(Paragraph("Income Breakdown", styles["Heading2"]))
        table_data = [["Category", "Amount (BDT)"]]
        for k, v in income.items():
            table_data.append([k, f"{v:.2f}"])
        story.append(Table(table_data))

    doc.build(story)
