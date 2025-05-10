import requests
import websocket
import json
import pandas as pd
import time
import logging

# Telegram bot token and chat ID
BOT_TOKEN = "7819951392:AAFkYd9-sblexjXNqgIfhbWAIC1Lr6NmPpo"
CHAT_ID = "6734231237"

# Set up logging
logging.basicConfig(level=logging.INFO)

# Global variables
candle_data = []
live_signals = []

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

# WebSocket callbacks
def on_message(ws, message):
    global candle_data
    try:
        data = json.loads(message)
        if "candles" in data:
            candles = data["candles"]
            df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close"])
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="s")
            candle_data = df
            signal = get_signals(df)
            if signal:
                live_signals.append(signal)
                send_telegram_message(signal)
    except Exception as e:
        logging.error(f"Error processing message: {e}")

def on_error(ws, error):
    logging.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.info("WebSocket closed")

def on_open(ws):
    logging.info("WebSocket connection opened")
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

# Signal generation logic
def get_signals(df=None):
    if df is not None and len(df) >= 2:
        latest = df.iloc[-1]
        previous = df.iloc[-2]
        if latest["high"] > previous["high"]:
            return f"🚀 BUY Signal @ {latest['high']} (Breakout UP)"
        elif latest["low"] < previous["low"]:
            return f"📉 SELL Signal @ {latest['low']} (Breakout DOWN)"
    return None

# Method for Flask to call
def get_signal_list():
    return live_signals[-10:]  # Return last 10 signals for dashboard

# Start WebSocket
if __name__ == "__main__":
    send_telegram_message("Working")  # Notify on start
    socket = "wss://ws.binaryws.com/websockets/v3?app_id=1089"
    ws = websocket.WebSocketApp(socket,
                                 on_open=on_open,
                                 on_message=on_message,
                                 on_error=on_error,
                                 on_close=on_close)
    while True:
        try:
            ws.run_forever()
        except Exception as e:
            logging.error(f"WebSocket encountered an error: {e}")
            reconnect_websocket()
