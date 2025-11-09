from flask import Flask, jsonify
import json, os
app=Flask(__name__)
DATA_PATH = os.path.join(os.path.dirname(__file__), "customers.json")
with open(DATA_PATH) as f:
    CUSTOMERS = json.load(f)

@app.route("/credit/<customer_id>", methods=["GET"])
def credit(customer_id):
    cust = next((c for c in CUSTOMERS if c["id"]==customer_id), None)
    if not cust:
        return jsonify({"score":0})
    return jsonify({"score":cust["credit_score"], "max_score":900})
    
if __name__ == "__main__":
    app.run(port=5003, debug=True)
