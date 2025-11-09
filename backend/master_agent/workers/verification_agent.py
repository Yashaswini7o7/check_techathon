import requests
CRM_BASE = "http://localhost:5001"
def verify_kyc(customer_id, fields):
    resp = requests.post(f"{CRM_BASE}/crm/verify", json={"customer_id": customer_id, "fields": fields}, timeout=5)
    return resp.json()
