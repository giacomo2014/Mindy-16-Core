import json
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Prevents the browser from blocking data traffic between engine and dashboard

def load_all_targets():
    combined_deck = []
    
    # Check File 1: Senate/Combined Targets
    try:
        with open("targets.json", "r") as file:
            combined_deck.extend(json.load(file))
    except Exception:
        pass

    # Check File 2: Representatives Data
    try:
        with open("representatives.json", "r") as file:
            combined_deck.extend(json.load(file))
    except Exception:
        pass
        
    return combined_deck

@app.route("/")
def index():
    return "API Engine Active."

@app.route("/api/targets")
def get_targets():
    """Broadcasts every single loaded candidate to the dashboard."""
    return jsonify(load_all_targets())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=18408, debug=True)