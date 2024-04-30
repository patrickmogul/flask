import requests
import os
from flask import Flask, request, jsonify, render_template
from datetime import datetime
from pytz import timezone
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual Telegram bot token
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/incoming/<token>", methods=["POST"])
def handler(token):
    try:
        # Log the incoming request along with the token
        print(f"Incoming request with token: {token}")
        print(f"Request data: {request.json}")

        # Check if request.json is a dictionary
        if not isinstance(request.json, dict):
            raise ValueError("Request data is not in the expected JSON format")

        # Extract message text, chat ID, and message ID from the request
        print("Extracting message text, chat ID, and message ID...")
        print(request.json)
        message_text = request.json.get("message", {}).get("text", "")
        print("Message text:", message_text)
        chat_id = request.json.get("message", {}).get("chat", {}).get("id", "")
        print("Chat ID:", chat_id)
        username = (
            request.json.get("message", {}).get("from", {}).get("username", "User")
        )
        print("Username:", username)

        # Send a "Processing your request..." message
        message_id = send_message(chat_id, "Processing your request...")

        # Define a dictionary to map each command to its corresponding action
        command_actions = {
            "/start": send_welcome_message,
            "/time": send_current_time,
            # Add more commands and their corresponding actions here
        }

        # If the command is recognized, execute its corresponding action
        if message_text in command_actions:
            command_actions[message_text](chat_id, message_id, username)
        else:
            # If the command is unknown, update the message with an error message
            error_message = (
                "We don't recognize that command at this time. Please try again later."
            )
            update_message(chat_id, message_id, error_message)

        return jsonify({"data": "Request received successfully"}), 200

    except Exception as e:
        print("Error in /incoming endpoint:", e)
        return (
            jsonify({"error": "An error occurred while processing the request."}),
            500,
        )


def send_message(chat_id, text):
    """Send a message to a chat using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    message_id = data["result"]["message_id"]
    print(f"Message sent with ID: {message_id}")
    return message_id


def update_message(chat_id, message_id, text):
    """Update a message in a chat using the Telegram Bot API."""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/editMessageText"
    payload = {"chat_id": chat_id, "message_id": message_id, "text": text}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    print(response.text)


def send_welcome_message(chat_id, message_id, username):
    """Send a welcome message to the user."""
    welcome_message = f"Welcome to the ioNetBot, {username}!"
    update_message(chat_id, message_id, welcome_message)


def send_current_time(chat_id, message_id, username):
    """Send the current UTC time to the user."""
    current_time = get_current_utc_time()
    update_message(chat_id, message_id, current_time)


def get_current_utc_time():
    """Get the current UTC time in human-readable format."""
    utc_time = datetime.now(timezone("UTC"))
    return utc_time.strftime("%Y-%m-%d %H:%M:%S UTC")


if __name__ == "__main__":
    app.run(port=5000)
