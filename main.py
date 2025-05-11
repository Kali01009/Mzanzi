import requests
import logging
import random
from datetime import datetime

BOT_TOKEN = "7819951392:AAFkYd9-sblexjXNqgIfhbWAIC1Lr6NmPpo"
CHAT_ID = "6734231237"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Send a message to Telegram
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logging.info("Message sent successfully")
        else:
            logging.error(f"Failed to send message: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending message: {e}")

# Generate sample signals for display
def get_signal_list():
    indices = ["R_10", "R_25", "R_50", "R_75", "R_100"]
    actions = ["BUY", "SELL", "HOLD"]
    signals = []

    for index in indices:
        action = random.choice(actions)
        timestamp = datetime.now().strftime("%H:%M:%S")
        signals.append(f"{index} - {action} at {timestamp}")

    return signals
