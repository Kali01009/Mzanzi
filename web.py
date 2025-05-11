from flask import Flask, render_template_string, request, redirect, url_for
from main import get_signal_list, send_telegram_message

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Signal Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 40px; background: #f4f4f4; }
        h1 { color: #333; }
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
</body>
</html>
"""

@app.route('/')
def home():
    signals = get_signal_list()
    return render_template_string(HTML_TEMPLATE, signals=signals)

@app.route('/send-hello', methods=['POST'])
def send_hello():
    send_telegram_message("hello")
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
