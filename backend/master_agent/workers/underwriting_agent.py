import requests
CREDIT_BASE = "http://localhost:5003"
def fetch_credit(customer_id):
    r = requests.get(f"{CREDIT_BASE}/credit/{customer_id}", timeout=5)
    return r.json().get("score",0)

def evaluate_eligibility(customer, requested_amount, monthly_salary=None):
    score = fetch_credit(customer["id"])
    pre_lim = customer["preapproved_limit"]
    # rules from problem statement
    if score < 700:
        return {"decision":"reject", "reason":"low_credit_score", "score":score}
    if requested_amount <= pre_lim:
        return {"decision":"approve", "score":score, "requires_salary_slip": False}
    if requested_amount <= 2*pre_lim:
        if monthly_salary is None:
            return {"decision":"needs_salary_slip", "score":score}
        # compute EMI simple approximate: monthly EMI for loan = (r/12 * P) / (1 - (1+r/12)^-n)
        r = 0.125/12
        n = 12*2 # example: 2 yrs
        P = requested_amount
        emi = (r * P) / (1 - (1+r)**(-n))
        if emi <= 0.5 * monthly_salary:
            return {"decision":"approve", "score":score, "emi":emi}
        else:
            return {"decision":"reject", "reason":"emi_gt_50pct_salary","emi":emi, "score":score}
    return {"decision":"reject","reason":"above_2x_limit","score":score}
