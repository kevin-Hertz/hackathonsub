from flask import Flask, request, jsonify
import re

app = Flask(__name__)

# Heuristic rules (scam indicators) with weights
SCAM_INDICATORS = [
    (r"(?i)(urgent|immediately|asap|24 hours|limited time)", 2),  # Urgency
    (r"(?i)(verify your account|provide your password|confirm your identity)", 2),  # Personal info request
    (r"(?i)(congratulations|you won|claim your prize|free money|investment opportunity)", 2),  # Too good to be true
    (r"(?i)(dear customer|dear user|hello friend|hey beautiful)", 1),  # Generic greeting
    (r"(?i)(i\s?need\s?your\s?help|send\s?money|transfer\s?funds)", 2),  # Money request
    (r"(?i)(click here|verify now|link below|open attachment)", 2),  # Suspicious link
    (r"(?i)(keep this between us|don’t tell anyone|private matter)", 1),  # Secrecy request
    (r"(?i)(gift cards|bitcoin|wire transfer)", 2),  # Unusual payment
    (r"(?i)(bank support|IRS|customs|official notification|security team)", 1),  # Authority impersonation
    (r"(?i)(i love you|thinking about you|we have a connection)", 1),  # Emotional manipulation
]

SCAM_TYPES = {
    'romance scam': ["love", "connection", "money", "urgent", "beautiful"],
    'phishing scam': ["verify", "identity", "account", "click", "suspended"],
    'lottery scam': ["won", "prize", "claim", "free", "congratulations"],
    'tech support scam': ["virus", "support", "Microsoft", "malware", "login"],
    'generic scam': []  # fallback
}

def analyze_message(text):
    score = 0
    indicators_triggered = []
    
    for pattern, weight in SCAM_INDICATORS:
        if re.search(pattern, text):
            score += weight
            indicators_triggered.append((pattern, weight))

    if score >= 4:
        # Try to classify based on keywords
        text_lower = text.lower()
        for scam_type, keywords in SCAM_TYPES.items():
            if any(kw in text_lower for kw in keywords):
                return scam_type
        return "generic scam"
    else:
        return "not a scam"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    message = data.get("text", "")
    result = analyze_message(message)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)