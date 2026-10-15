from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Demo logic: replace this with a trained image-classification model for production.
ITEMS = {
    "phone": {
        "label": "Mobile phone",
        "reuse": ["Repair the screen or battery if practical.", "Donate a working phone after securely wiping personal data."],
        "recycle": ["Take it to an authorized e-waste collection centre.", "Remove SIM and memory cards; never put it in household waste."],
        "co2": 8.0
    },
    "laptop": {
        "label": "Laptop / computer",
        "reuse": ["Upgrade RAM or storage to extend its life.", "Donate a working device after securely erasing your data."],
        "recycle": ["Use an authorized e-waste recycler.", "Keep batteries separate only if the recycler instructs you to."],
        "co2": 25.0
    },
    "battery": {
        "label": "Battery",
        "reuse": ["Reuse only if undamaged and compatible with the device."],
        "recycle": ["Do not puncture, burn, or place it in household trash.", "Tape exposed terminals and take it to a battery collection point."],
        "co2": 5.0
    },
    "cable": {
        "label": "Cable / charger",
        "reuse": ["Test whether it works safely with a compatible device."],
        "recycle": ["Collect damaged cables for an authorized e-waste recycler.", "Do not burn wires to recover copper."],
        "co2": 2.0
    },
    "monitor": {
        "label": "Monitor / screen",
        "reuse": ["Check whether the display can be repaired or reused."],
        "recycle": ["Use a certified e-waste facility; screens may contain hazardous materials.", "Do not break the screen."],
        "co2": 18.0
    }
}

def detect_item(filename):
    name = (filename or "").lower()
    keywords = {
        "phone": ["phone", "mobile", "smartphone"],
        "laptop": ["laptop", "computer", "pc"],
        "battery": ["battery", "cell"],
        "cable": ["cable", "charger", "wire"],
        "monitor": ["monitor", "screen", "display", "tv"]
    }
    for key, words in keywords.items():
        if any(word in name for word in words):
            return key
    return "phone"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/analyze", methods=["POST"])
def analyze():
    uploaded = request.files.get("image")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Please choose an image first."}), 400
    if not uploaded.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        return jsonify({"error": "Please upload a JPG, PNG, or WEBP image."}), 400

    filename = secure_filename(uploaded.filename)
    # Keep uploads only for this demo; a production app should add privacy controls and cleanup.
    uploaded.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
    key = detect_item(filename)
    item = ITEMS[key]
    return jsonify({
        "item": item["label"],
        "confidence": "Demo estimate",
        "reuse": item["reuse"],
        "recycle": item["recycle"],
        "co2_saved_kg": item["co2"],
        "note": "Prototype result based on the filename, not actual visual AI recognition. Connect a trained vision model for real image analysis."
    })

if __name__ == "__main__":
    app.run(debug=True)
