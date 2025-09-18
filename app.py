from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
import requests
from random import choices
import string

app = Flask(__name__)
app.config["SECRET_KEY"] = "yipyipyooraywehavekiboltoday"
socketio = SocketIO(app)

players = {}
buzzed = None


@app.route("/")
def index():
    return render_template("index.html")

host_code = "".join(choices(string.ascii_lowercase, k=5))
print(f"Host code is {host_code}")
@app.route(f"/{host_code}")
def host():
    return render_template("new_host.html")

@app.route('/api/tossup')
def get_tossup():
    # default difficulties if not provided
    diffs = request.args.get('difficulties', '2,3,4,5')
    url = f"https://qbreader.org/api/random-tossup?difficulties={diffs}&powermarkOnly=true&standardOnly=true"
    try:
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@socketio.on("join")
def handle_join(data):
    global players
    username = data["username"]
    sid = request.sid
    players[sid] = username
    emit("player_list", list(players.values()), broadcast=True)
    print(f"{username} joined")

@socketio.on("buzz")
def handle_buzz():
    global buzzed
    sid = request.sid
    if buzzed is None:
        buzzed = sid
        username = players[sid]
        emit("buzzed", username, broadcast=True)

@socketio.on("reset")
def handle_reset():
    global buzzed
    buzzed = None
    emit("reset", broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    global players
    sid = request.sid
    if sid in players:
        players.pop(sid)
        emit("player_list", list(players.values()), broadcast=True)


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5001)
