import requests
import logging

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

# Send analysis results to Telegram
def send_analysis_to_telegram(analysis_results):
    for index, result in analysis_results.items():
        message = f"📊 Analysis for {index}:\n"
        message += f"Touches: {', '.join(map(str, result['Touches']))}\n"
        message += f"Patterns: {', '.join(result['Patterns'])}\n"
        message += f"Breakouts: {', '.join(map(str, result['Breakouts']))}\n"
        
        # Send the message to Telegram
        send_telegram_message(message)
