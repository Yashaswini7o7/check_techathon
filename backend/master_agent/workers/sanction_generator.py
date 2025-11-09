from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

def generate_sanction_letter(customer, offer, out_dir="generated"):
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)
    fname = f"{out_dir}/sanction_{customer['id']}_{offer['offer_id']}.pdf"
    c = canvas.Canvas(fname, pagesize=A4)
    c.setFont("Helvetica",12)
    c.drawString(72,800,"Tata Capital - Sanction Letter")
    c.drawString(72,780,f"Customer: {customer['name']} ({customer['id']})")
    c.drawString(72,760,f"Offer ID: {offer['offer_id']} Amount: INR {offer['amount']}")
    c.drawString(72,740,f"Tenure: {offer['tenure_months']} months Rate: {offer['rate_annual_percent']}% p.a.")
    c.drawString(72,700,"This is an automated sanction letter based on pre-approved offer subject to final checks.")
    c.showPage()
    c.save()
    return fname
