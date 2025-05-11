from flask import Flask, render_template_string, request, redirect, url_for
from main import get_signal_list, send_telegram_message, analyze_selected_indices

app = Flask(__name__)

VOLATILITY_INDICES = [
    "R_10", "R_25", "R_50", "R_75", "R_100",
    "R_10_1s", "R_25_1s", "R_50_1s", "R_75_1s", "R_100_1s"
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Signal Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; background: #f4f4f4; }
        h1, h2 { color: #333; }
        ul { list-style: none; padding: 0; }
        li { background: #fff; margin: 10px 0; padding: 10px; border-left: 5px solid #6a1b9a; }
        form { margin-top: 30px; }
        button {
            background-color: #6a1b9a;
            color: white;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            font-size: 16px;
        }
        button:hover {
            background-color: #8e24aa;
        }
        .checkboxes { margin-bottom: 20px; }
        .checkboxes label {
            display: inline-block;
            margin: 5px 15px 5px 0;
            background: #fff;
            padding: 8px 12px;
            border: 1px solid #ccc;
            border-left: 5px solid #6a1b9a;
        }
    </style>
</head>
<body>
    <h1>Live Signals</h1>
    <ul>
        {% for signal in signals %}
            <li>{{ signal }}</li>
        {% endfor %}
    </ul>

    <form action="{{ url_for('send_hello') }}" method="post">
        <button type="submit">Send Hello to Telegram</button>
    </form>

    <h2>Select Indices to Analyze</h2>
    <form action="{{ url_for('start_analysis') }}" method="post">
        <div class="checkboxes">
            {% for index in indices %}
                <label>
                    <input type="checkbox" name="selected_indices" value="{{ index }}"> {{ index }}
                </label>
            {% endfor %}
        </div>
        <button type="submit">Start Analysis</button>
    </form>
</body>
</html>
"""

@app.route('/')
def home():
    signals = get_signal_list()
    return render_template_string(HTML_TEMPLATE, signals=signals, indices=VOLATILITY_INDICES)

@app.route('/send-hello', methods=['POST'])
def send_hello():
    send_telegram_message("hello")
    return redirect(url_for('home'))

@app.route('/start-analysis', methods=['POST'])
def start_analysis():
    selected_indices = request.form.getlist('selected_indices')
    if selected_indices:
        analyze_selected_indices(selected_indices)
        send_telegram_message(f"Started analysis for: {', '.join(selected_indices)}")
    else:
        send_telegram_message("No indices selected for analysis.")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
