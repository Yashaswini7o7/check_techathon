# simple rule-based sales agent
def propose_offer(customer, offers):
    # choose top offer by amount
    if not offers: return None
    best = max(offers, key=lambda o: o["amount"])
    pitch = f"Hi {customer['name']}. You have a pre-approved offer of INR {best['amount']}. Tenure {best['tenure_months']} months at {best['rate_annual_percent']}% p.a. Interested?"
    return {"pitch": pitch, "offer": best}
