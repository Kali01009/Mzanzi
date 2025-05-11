import requests

# ✅ Replace these with your actual values
TELEGRAM_TOKEN = "your_actual_bot_token"
TELEGRAM_CHAT_ID = "your_actual_chat_id"

def send_telegram_message(message: str):
    """Send formatted alert to Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print(f"Telegram Error: {e}")
