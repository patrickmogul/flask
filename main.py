import requests
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

@app.route('/api/incoming/<token>', methods=['POST'])
def handler(token):
    try:
        # Log the incoming request along with the token
        print(f"Incoming request with token: {token}")
        print(f"Request data: {request.json}")

        # Extract message text and username from the request
        message_text = request.json.get('message', {}).get('text', '')
        username = request.json.get('message', {}).get('from', {}).get('username', 'User')

        # Check if the message text is '/start'
        if message_text == '/start':
            # Craft the welcome message
            welcome_message = f"Welcome to the ioNetBot, {username}!"

            # Send the welcome message to the user
            chat_id = request.json.get('message', {}).get('chat', {}).get('id', '')
            send_message(chat_id, welcome_message)

        return jsonify({"data": "Request received successfully"}), 200

    except Exception as e:
        print("Error in /incoming endpoint:", e)
        return jsonify({"error": "An error occurred while processing the request."}), 500

def send_message(chat_id, text):
    """Send a message to a chat using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': text
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()

if __name__ == '__main__':
    app.run(port=5000)
