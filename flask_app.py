from flask import Flask, render_template
from flask_cors import CORS
import threading

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

def run_flask():
    try:
        print("Starting Flask server...")
        app.run(host='0.0.0.0', port=8000)
    except Exception as e:
        print(f"Error starting Flask server: {e}")

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()
