import time
from datetime import datetime, timedelta
from main import send_telegram_message
import logging
import random

# Set up logging
logging.basicConfig(level=logging.INFO)

def predict_signal_occurrence(index):
    """
    Simulates signal prediction for an index. You can replace this with ML or strategy-based logic.
    Returns a dict with prediction info.
    """
    # Simulate prediction: 60% chance signal may occur within 15 minutes
    signal_probability = random.uniform(0, 1)
    will_occur = signal_probability > 0.4

    predicted_time = datetime.now() + timedelta(minutes=random.randint(1, 15)) if will_occur else None
    signal_action = random.choice(["BUY", "SELL"]) if will_occur else "NONE"

    return {
        "index": index,
        "will_occur": will_occur,
        "predicted_time": predicted_time,
        "signal_action": signal_action,
        "probability": signal_probability
    }

def analyze_selected_indices(indices):
    for index in indices:
        logging.info(f"🔍 Predicting signal for {index}...")
        send_telegram_message(f"🔍 Analyzing {index}...")

        prediction = predict_signal_occurrence(index)

        if prediction["will_occur"]:
            time_str = prediction["predicted_time"].strftime("%H:%M:%S")
            message = (f"✅ Predicted {prediction['signal_action']} signal for {index} "
                       f"likely within 15 minutes (ETA: {time_str}, Confidence: {prediction['probability']:.2f})")
        else:
            message = f"❌ No strong signal predicted for {index} within 15 minutes."

        logging.info(message)
        send_telegram_message(message)

        time.sleep(2)  # Simulate processing time
