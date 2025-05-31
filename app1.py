from flask import Flask, request, jsonify, render_template
import pytesseract
from PIL import Image
import io
import base64
import openai
import json
import os
from dotenv import load_dotenv


load_dotenv()


openai.api_key = os.getenv("OPENAI_API_KEY")


app = Flask(__name__)


def detect_scam_heuristic(message):
    red_flags = []
    scam_type = None
    is_scam = False

    if any(word in message.lower() for word in ["congratulations", "claim your prize", "winner", "gift card"]):
        red_flags.append("Suspicious promotional language")
        scam_type = "lottery scam"

    if any(word in message.lower() for word in ["click the link", "verify your account", "login to win"]):
        red_flags.append("Request to click suspicious link")
        scam_type = scam_type or "phishing scam"

    if red_flags:
        is_scam = True

    return {
        "is_scam": is_scam,
        "scam_type": scam_type if scam_type else "unknown",
        "red_flags": red_flags
    }


def detect_scam_with_gpt(message):
    prompt = f"""
You are an AI trained to detect scam messages. Analyze the message below and classify whether it's a scam or not. If it's a scam, identify the scam type and list red flags.

Message: "{message}"

Respond in JSON format with the fields: is_scam (true/false), scam_type (string), red_flags (list of strings).
"""
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0,
        max_tokens=300,
    )
    return json.loads(response.choices[0].text.strip())

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    image_data = data['image'].split(',')[1]
    image_bytes = base64.b64decode(image_data)
    image = Image.open(io.BytesIO(image_bytes))
    extracted_text = pytesseract.image_to_string(image)

    try:
        detection_result = detect_scam_with_gpt(extracted_text)
    except Exception as e:
        print(f"GPT detection failed: {e}")
        detection_result = detect_scam_heuristic(extracted_text)

    return jsonify({
        'extracted_text': extracted_text,
        'detection_result': detection_result
    })

if __name__ == '__main__':
    app.run(debug=True)
