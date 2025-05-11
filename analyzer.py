import time
from datetime import datetime
from main import send_telegram_message
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

def analyze_selected_indices(indices):
    for index in indices:
        logging.info(f"Analyzing {index}...")
        send_telegram_message(f"🔍 Starting analysis for {index}...")

        # Simulate some analysis delay
        time.sleep(2)

        result = f"{index} - Analysis completed at {datetime.now().strftime('%H:%M:%S')}"
        logging.info(result)
        send_telegram_message(f"📈 {result}")
