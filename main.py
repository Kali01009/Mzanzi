import websocket
import json
import pandas as pd
from datetime import datetime
from win10toast import ToastNotifier
import requests
import threading

# Replace this with your actual chat ID
TELEGRAM_TOKEN = '7819951392:AAFkYd9-sblexjXNqgIfhbWAIC1Lr6NmPpo'
CHAT_ID = '6734231237'

candles_5min = []
candles_1min = []
notifier = ToastNotifier()

def send_notification(title, message):
    print(f"[ALERT] {title}: {message}")
    notifier.show_toast(title, message, duration=5)
    
    telegram_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': f"{title}\n{message}"
    }
    try:
        requests.post(telegram_url, data=payload)
    except Exception as e:
        print(f"Error sending Telegram message: {e}")

def detect_trend(candles):
    df = pd.DataFrame(candles)
    df['ma'] = df['close'].rolling(window=10).mean()
    if len(df['ma'].dropna()) < 1:
        return None
    return "UP" if df['close'].iloc[-1] > df['ma'].iloc[-1] else "DOWN"

def detect_patterns():
    global candles_5min, candles_1min
    df_5min = pd.DataFrame(candles_5min)
    df_1min = pd.DataFrame(candles_1min)
    
    if len(df_5min) < 20 or len(df_1min) < 5:
        return
    
    support = df_5min['low'].min()
    resistance = df_5min['high'].max()
    last_close_1min = df_1min['close'].iloc[-1]
    trend = detect_trend(candles_5min)
    
    message = None
    if abs(last_close_1min - resistance) / resistance < 0.001:
        message = f"🔍 Price NEAR RESISTANCE: {last_close_1min}\nTrend: {trend}"
    elif abs(last_close_1min - support) / support < 0.001:
        message = f"🔍 Price NEAR SUPPORT: {last_close_1min}\nTrend: {trend}"
    elif last_close_1min > resistance:
        message = f"🚀 BREAKOUT ABOVE RESISTANCE!\nPrice: {last_close_1min}\nTrend: {trend}"
    elif last_close_1min < support:
        message = f"📉 BREAKDOWN BELOW SUPPORT!\nPrice: {last_close_1min}\nTrend: {trend}"
    
    if message:
        send_notification("Breakout Alert (V75)", message)

def on_message(ws, message):
    global candles_5min, candles_1min
    data = json.loads(message)
    if 'tick' in data:
        return
    
    candle = data['ohlc']
    timeframe = candle['granularity']
    new_candle = {
        'epoch': int(candle['epoch']),
        'open': float(candle['open']),
        'high': float(candle['high']),
        'low': float(candle['low']),
        'close': float(candle['close'])
    }

    if timeframe == 60:
        candles_1min.append(new_candle)
        candles_1min = candles_1min[-200:]
    elif timeframe == 300:
        candles_5min.append(new_candle)
        candles_5min = candles_5min[-200:]
        threading.Thread(target=detect_patterns).start()

def on_open(ws):
    print("Connected to Deriv WebSocket (V75)")
    ws.send(json.dumps({
        "ticks_history": "R_75",
        "style": "candles",
        "granularity": 60,
        "count": 200,
        "subscribe": 1
    }))
    ws.send(json.dumps({
        "ticks_history": "R_75",
        "style": "candles",
        "granularity": 300,
        "count": 200,
        "subscribe": 1
    }))

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("WebSocket closed, reconnecting in 10s...")
    threading.Timer(10, run_ws).start()

def run_ws():
    socket = websocket.WebSocketApp("wss://ws.binaryws.com/websockets/v3?app_id=1089",
                                    on_open=on_open,
                                    on_message=on_message,
                                    on_error=on_error,
                                    on_close=on_close)
    socket.run_forever()

if __name__ == "__main__":
    run_ws()
