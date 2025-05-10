import requests
import websocket
import json
import pandas as pd
import time
import logging

# Telegram bot token and chat ID (replace with your actual bot token and chat ID)
BOT_TOKEN = "7819951392:AAFkYd9-sblexjXNqgIfhbWAIC1Lr6NmPpo"
CHAT_ID = "6734231237"

# Set up logging
logging.basicConfig(level=logging.INFO)

# Function to send Telegram message
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
        logging.error(f"Failed to send message: {e}")

# WebSocket callback handlers
def on_message(ws, message):
    try:
        data = json.loads(message)
        if "candles" in data:
            candles = data["candles"]
            df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")

            latest = df.iloc[-1]
            previous = df.iloc[-2]

            # Simple breakout check
            if latest["high"] > previous["high"]:
                send_telegram_message("🚀 Breakout UP Confirmed!")
            elif latest["low"] < previous["low"]:
                send_telegram_message("📉 Breakout DOWN Confirmed!")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

def on_error(ws, error):
    logging.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.info("WebSocket closed")

def on_open(ws):
    logging.info("WebSocket connection opened")
    # Send initial message to Telegram when WebSocket starts
    send_telegram_message("WebSocket connection established! 🚀")

    subscribe_message = {
        "ticks_history": "R_100",
        "style": "candles",
        "granularity": 60,
        "count": 100,
        "subscribe": 1
    }
    ws.send(json.dumps(subscribe_message))

def reconnect_websocket():
    logging.info("Attempting to reconnect...")
    time.sleep(5)
    ws.run_forever()

# Example function (not used in this version, just kept for future logic extension)
def get_signals():
    signals = [
        {"symbol": "BTCUSDT", "action": "BUY", "price": 27500},
        {"symbol": "ETHUSDT", "action": "SELL", "price": 1850}
    ]
    return signals

# Run WebSocket
if __name__ == "__main__":
    send_telegram_message("Working")  # Send 'Working' when the script starts

    socket = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
    
    ws = websocket.WebSocketApp(socket,
                                 on_open=on_open,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    
    # Set the WebSocket to reconnect if the connection is closed
    while True:
        try:
            ws.run_forever()
        except Exception as e:
            logging.error(f"WebSocket encountered an error: {e}")
            reconnect_websocket()
