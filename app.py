from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app, async_mode="gevent", cors_allowed_origins="*")


# ----- Web Routes -----
@app.route("/")
def index():
    """Renders the page seen by players when they go to <ip>:<port>/"""
    return render_template("index.html")

@app.route("/host")
def host():
    """Renders the host control/question display when the host goes to <ip>:<port>/host"""
    return render_template("host.html")

@app.route("/next_question")
def next_questions():
    """Fetches a question from the QBReader API and returns it as JSON"""
    raise Exception("This function has not been made yet!")
    return jsonify({...})

# ----- Socket Events -----
@socketio.on("buzz")
def handle_buzz(data):
    """Notify the host that someone has buzzed"""
    emit("buzzed", data, broadcast=True)

@socketio.on("reset")
def handle_reset():
    """Reset the buzzer lock to allow buzzing"""
    emit("reset", broadcast=True)


# ----- Main -----
if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
