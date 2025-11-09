from workers.sales_agent import propose_offer
from workers.verification_agent import verify_kyc
from workers.underwriting_agent import evaluate_eligibility, fetch_credit
from workers.sanction_generator import generate_sanction_letter
import requests

OFFER_BASE = "http://localhost:5002"

def get_offers(customer_id):
    resp = requests.get(f"{OFFER_BASE}/offers/{customer_id}", timeout=5)
    return resp.json().get("offers",[])

def master_handle_message(session, customer_id, message_text, context):
    # context is dict storing session state
    # steps: 1 identify customer 2 propose offer 3 verify 4 underwriting 5 sanction
    ret = {"responses": []}
    # simple finite state machine based on context['stage']
    stage = context.get("stage","start")
    if stage == "start":
        # load customer from CRM
        r = requests.get(f"http://localhost:5001/crm/customer/{customer_id}")
        if r.status_code!=200:
            context["stage"]="end"
            ret["responses"].append("Sorry I could not find your details. Please provide customer id.")
            return ret, context
        customer = r.json()["customer"]
        context["customer"]=customer
        # propose offer
        offers = get_offers(customer_id)
        prop = propose_offer(customer, offers)
        context["current_offer"] = prop["offer"]
        context["stage"]="offer_proposed"
        ret["responses"].append(prop["pitch"])
        return ret, context

    if stage == "offer_proposed":
        # interpret user reply (simple yes/no)
        if "yes" in message_text.lower() or "interested" in message_text.lower():
            context["stage"]="verify"
            ret["responses"].append("Great. I'll quickly verify your KYC (phone and address).")
            v = verify_kyc(customer_id, fields=["phone","city"])
            if v.get("result"):
                context["kyc"] = v["result"]
                ret["responses"].append("KYC verified.")
            else:
                ret["responses"].append("KYC could not be fully verified. Please confirm your phone and city.")
            # continue to underwriting
            context["stage"]="underwriting"
            ret["responses"].append("Running eligibility checks now.")
            return ret, context
        else:
            context["stage"]="end"
            ret["responses"].append("No worries. If you change your mind let me know.")
            return ret, context

    if stage == "underwriting":
        cust = context["customer"]
        offer = context["current_offer"]
        requested_amount = offer["amount"]
        uw = evaluate_eligibility(cust, requested_amount)
        if uw["decision"]=="approve":
            # generate sanction letter
            pdf = generate_sanction_letter(cust, offer)
            context["sanction_pdf"]=pdf
            context["stage"]="closed"
            ret["responses"].append("Congratulations your loan is approved. Download sanction letter at: "+pdf)
            return ret, context
        if uw["decision"]=="needs_salary_slip":
            context["stage"]="await_salary"
            ret["responses"].append("We need a salary slip to proceed. Please upload a salary slip (file upload).")
            return ret, context
        if uw["decision"]=="reject":
            context["stage"]="end"
            ret["responses"].append(f"Unfortunately we cannot approve this loan: {uw.get('reason')}")
            return ret, context

    if stage == "await_salary":
        # message_text assumed file uploaded path in context by upload endpoint
        if context.get("uploaded_salary_path"):
            # stubbed monthly salary extraction: assume API/ocr returns 60000
            monthly_salary = context.get("mock_salary_amount",60000)
            cust = context["customer"]
            offer = context["current_offer"]
            uw = evaluate_eligibility(cust, offer["amount"], monthly_salary=monthly_salary)
            if uw["decision"]=="approve":
                pdf = generate_sanction_letter(cust, offer)
                context["sanction_pdf"]=pdf
                context["stage"]="closed"
                ret["responses"].append("Salary verified. Loan approved. Sanction letter: "+pdf)
                return ret, context
            else:
                context["stage"]="end"
                ret["responses"].append("After reviewing salary slip we cannot approve the loan.")
                return ret, context
        else:
            ret["responses"].append("Waiting for salary slip upload.")
            return ret, context

    ret["responses"].append("Session ended.")
    context["stage"]="end"
    return ret, context
