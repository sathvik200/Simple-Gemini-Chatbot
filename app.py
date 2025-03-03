import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get API Key from environment variables
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    raise ValueError("GOOGLE_API_KEY is missing. Add it to the .env file.")

# Configure Google Gemini API
genai.configure(api_key=API_KEY)

# Initialize Gemini Model
model = genai.GenerativeModel('gemini-1.5-pro')
chat = model.start_chat(history=[])

# Initialize Flask App
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("Website.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_message = request.json.get("message")

    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Get response from Gemini API
    response = chat.send_message(user_message)
    bot_reply = response.text if response.text else "Sorry, I couldn't understand that."

    return jsonify({"user": user_message, "bot": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)