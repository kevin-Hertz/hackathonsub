from flask import Flask, request, jsonify
import re
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests from frontend

# Indicators for different scam types
detection_rules = {
    "romance scam": [
        r"(?i)I'?ve been thinking about you",
        r"(?i)real connection",
        r"(?i)I'?m stuck.*abroad",
        r"(?i)send me some money",
        r"(?i)urgent.*help",
        r"(?i)don'?t tell anyone",
    ],
    "phishing scam": [
        r"(?i)detected suspicious activity",
        r"(?i)verify your identity",
        r"(?i)account has been temporarily suspended",
        r"(?i)clicking the link below",
        r"(?i)failure to verify",
        r"(?i)customer support team",
    ],
    "lottery scam": [
        r"(?i)you won.*lottery",
        r"(?i)claim your prize",
        r"(?i)random selection",
        r"(?i)congratulations.*winner",
    ],
    "tech support scam": [
        r"(?i)contact support immediately",
        r"(?i)virus detected",
        r"(?i)unusual activity",
    ],
}

def detect_scam(message):
    message = message.strip()
    if not message:
        return {"is_scam": False, "scam_type": "", "red_flags": []}

    all_flags = []
    matched_type = None
    highest_matches = 0

    for scam_type, patterns in detection_rules.items():
        matches = [p for p in patterns if re.search(p, message)]
        if len(matches) > highest_matches:
            matched_type = scam_type
            all_flags = [re.search(p, message).group() for p in matches if re.search(p, message)]
            highest_matches = len(matches)

    return {
        "is_scam": matched_type is not None,
        "scam_type": matched_type or "",
        "red_flags": all_flags
    }

@app.route("/analyze", methods=["POST"])
def analyze_message():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    result = detect_scam(message)
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)