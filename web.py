from flask import Flask, render_template_string, request, redirect
from analyzer import analyze_selected_indices
from main import send_telegram_message

app = Flask(__name__)

# List of volatility indices with proper names
VOLATILITY_INDICES = [
    "Volatility_10", "Volatility_25", "Volatility_50", "Volatility_75", "Volatility_100",
    "Volatility_10_1s", "Volatility_25_1s", "Volatility_50_1s", "Volatility_75_1s", "Volatility_100_1s"
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Volatility Signal Dashboard</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(to right, #6a11cb, #2575fc);
            margin: 0;
            padding: 0;
            color: white;
        }
        .container {
            max-width: 700px;
            margin: 80px auto;
            background: #ffffff0d;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 0 15px rgba(0,0,0,0.3);
        }
        h1 {
            text-align: center;
            margin-bottom: 30px;
        }
        form {
            display: flex;
            flex-direction: column;
        }
        label {
            background: #ffffff1a;
            padding: 10px;
            margin: 8px 0;
            border-radius: 8px;
            display: flex;
            align-items: center;
        }
        input[type="checkbox"] {
            margin-right: 10px;
            transform: scale(1.3);
        }
        .btn {
            background: #ffffff;
            color: #2575fc;
            border: none;
            padding: 12px 20px;
            margin-top: 25px;
            font-size: 18px;
            font-weight: bold;
            border-radius: 8px;
            cursor: pointer;
            transition: background 0.3s ease;
        }
        .btn:hover {
            background: #ddd;
        }
        .price {
            color: #ffcc00;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Volatility Index Analyzer</h1>
        <form method="POST" action="/analyze">
            {% for index, price in indices %}
                <label>
                    <input type="checkbox" name="selected_indices" value="{{ index }}"> 
                    {{ index }} - <span class="price">${{ price }}</span>
                </label>
            {% endfor %}
            <button type="submit" class="btn">🚀 Start Analysis</button>
        </form>
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    # Fetch the indices along with their predicted prices
    indices_with_prices = [(index, get_predicted_price(index)) for index in VOLATILITY_INDICES]
    return render_template_string(HTML_TEMPLATE, indices=indices_with_prices)

@app.route('/analyze', methods=['POST'])
def analyze():
    selected = request.form.getlist('selected_indices')
    if not selected:
        send_telegram_message("⚠️ No indices selected for analysis.")
        return redirect('/')
    
    send_telegram_message(f"🟢 Starting analysis for: {', '.join(selected)}")
    analyze_selected_indices(selected)
    return redirect('/')

def get_predicted_price(index):
    # Dummy logic: Replace this with the actual logic to get the price
    # For now, it returns a random price
    import random
    return round(random.uniform(100, 200), 2)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
