import websocket
import json
import logging
import time
import threading
from analyzer import analyze_selected_indices
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)

# Deriv WebSocket URL
ws_url = "wss://ws.binaryws.com/websockets/v3?app_id=1089"  # Replace with your app_id if needed

# Selected indices for analysis
selected_indices = ["R_10", "R_25", "R_50", "R_75", "R_100"]  # Modify this list as per your requirement

# This will hold the received market data
market_data = []

def on_message(ws, message):
    try:
        data = json.loads(message)
        logging.info(f"Received message: {data}")
        
        # Append the relevant market data (modify according to the API response format)
        if "ticks" in data:
            market_data.append(data['ticks'])
            
            # Analyze the data once new market data is received
            analysis_results = analyze_selected_indices(selected_indices, market_data)
            
            # Optionally, you could display the analysis on the front-end here
            
            # Send results to Telegram
            send_analysis_to_telegram(analysis_results)
        
    except Exception as e:
        logging.error(f"Error processing message: {e}")

def on_error(ws, error):
    logging.error(f"WebSocket error: {error}")

def on_close(ws, close_status_code, close_msg):
    logging.info(f"WebSocket closed with code: {close_status_code}, message: {close_msg}")

def on_open(ws):
    logging.info("WebSocket connection established!")

    # Example: Send a subscription message to start receiving market data (ticks)
    subscribe_message = {
        "ticks": "R_10",  # Example symbol for volatility index (can be changed)
        "granularity": 60  # Granularity for the ticks (can be changed)
    }

    ws.send(json.dumps(subscribe_message))
    logging.info(f"Sent subscription message: {subscribe_message}")

def run_websocket():
    ws = websocket.WebSocketApp(
        ws_url,
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )

    # Keep WebSocket connection alive
    while True:
        try:
            ws.run_forever()
        except Exception as e:
            logging.error(f"WebSocket encountered an error: {e}")
            time.sleep(5)  # Wait for 5 seconds before trying to reconnect

# Start the WebSocket connection in a separate thread
def start_ws_thread():
    ws_thread = threading.Thread(target=run_websocket)
    ws_thread.daemon = True
    ws_thread.start()

# Start WebSocket connection when the script runs
if __name__ == "__main__":
    start_ws_thread()
    while True:
        time.sleep(1)  # Keep the main thread alive
