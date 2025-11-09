from flask import Flask, jsonify
import json, os
app=Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), "customers.json")
with open(DATA_PATH) as f:
    CUSTOMERS = json.load(f)

@app.route("/offers/<customer_id>", methods=["GET"])
def offers(customer_id):
    cust = next((c for c in CUSTOMERS if c["id"]==customer_id), None)
    if not cust: return jsonify({"offers":[]})
    offers = [
      {"offer_id":"O1","amount":cust["preapproved_limit"],"tenure_months":24,"rate_annual_percent":12.5}
    ]
    # add cross-sell
    return jsonify({"customer_id":customer_id,"offers":offers})

if __name__ == "__main__":
    app.run(port=5002, debug=True)
