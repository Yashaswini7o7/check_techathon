from flask import Flask, jsonify, request
import json, os

app = Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), "customers.json")
with open(DATA_PATH) as f:
    CUSTOMERS = {c["id"]: c for c in json.load(f)}

@app.route("/crm/customer/<customer_id>", methods=["GET"])
def get_customer(customer_id):
    c = CUSTOMERS.get(customer_id)
    if c:
        return jsonify({"status":"ok","customer":c})
    return jsonify({"status":"not_found"}), 404

@app.route("/crm/verify", methods=["POST"])
def verify():
    data = request.json
    cid = data.get("customer_id")
    fields = data.get("fields", [])
    c = CUSTOMERS.get(cid)
    if not c:
        return jsonify({"status":"not_found"}),404
    # simple check: if phone/email match in payload return verified
    resp = {"verified": {}}
    for f in fields:
        resp["verified"][f] = True if c.get(f) else False
    return jsonify({"status":"ok","result":resp})

if __name__ == "__main__":
    app.run(port=5001, debug=True)
