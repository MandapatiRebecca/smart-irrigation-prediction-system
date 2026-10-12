from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import os

app = Flask(__name__)
DATA_FILE = os.path.join(os.path.dirname(__file__), "irrigation_history.json")

def load_history():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_history(rows):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(rows[-50:], f, indent=2)

def predict_irrigation(moisture, temperature, humidity, rain_expected):
    """
    Demonstration prediction logic. Replace with a trained ML model
    once you have a labelled crop/soil dataset.
    """
    score = 0
    if moisture < 30:
        score += 2
    elif moisture < 40:
        score += 1
    if temperature >= 32:
        score += 1
    if humidity < 40:
        score += 1
    if rain_expected:
        score -= 2

    needed = score >= 2
    if needed:
        reason = "Soil moisture is low and current conditions suggest watering may be needed."
        litres = max(5, round((40 - moisture) * 1.5))
    else:
        reason = "Current conditions do not indicate an immediate need for irrigation."
        litres = 0
    return {
        "irrigation_needed": needed,
        "recommendation": "IRRIGATION REQUIRED" if needed else "NO IRRIGATION NEEDED",
        "estimated_water_litres": litres,
        "reason": reason,
        "score": score
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True) or {}
    try:
        moisture = float(data["moisture"])
        temperature = float(data["temperature"])
        humidity = float(data["humidity"])
        rain_expected = bool(data.get("rain_expected", False))
    except (KeyError, TypeError, ValueError):
        return jsonify({"error": "Please provide valid numeric sensor values."}), 400

    if not 0 <= moisture <= 100:
        return jsonify({"error": "Soil moisture must be between 0 and 100%."}), 400
    if not -10 <= temperature <= 70:
        return jsonify({"error": "Temperature must be between -10 and 70 °C."}), 400
    if not 0 <= humidity <= 100:
        return jsonify({"error": "Humidity must be between 0 and 100%."}), 400

    result = predict_irrigation(moisture, temperature, humidity, rain_expected)
    row = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "moisture": moisture,
        "temperature": temperature,
        "humidity": humidity,
        "rain_expected": rain_expected,
        **result
    }
    history = load_history()
    history.append(row)
    save_history(history)
    result["record"] = row
    return jsonify(result)

@app.route("/api/history", methods=["GET"])
def history():
    return jsonify(load_history()[::-1][:10])

@app.route("/api/pump", methods=["POST"])
def pump():
    data = request.get_json(silent=True) or {}
    # Demo only: this records a software state. Connect a properly isolated
    # relay/controller and add safety controls before operating real hardware.
    enabled = bool(data.get("enabled", False))
    return jsonify({
        "pump_enabled": enabled,
        "message": "Demo pump state updated. No physical pump is connected."
    })

if __name__ == "__main__":
    app.run(debug=True)
