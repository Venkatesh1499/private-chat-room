from flask import Flask, request, jsonify, render_template
from flask_socketio import SocketIO, emit, join_room
import eventlet

eventlet.monkey_patch()

app = Flask(__name__)
app.config['SECERT_KEY'] = "secret123"
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="eventlet",
    ping_interval=25,   # seconds
    ping_timeout=60     # seconds
      )


@app.route('/')
def home():
    return render_template("index.html")


@socketio.on("join_room")
def handle_join(data):
    room = data["room"]
    join_room(room)
    emit("room_message", {"message": f"Joined room {room}"}, room = room)


@socketio.on("room_message")
def handle_message(data):
    print("message received", data["message"], data["room"])
    room = data["room"]
    message = data["message"]
    emit("room_message", {"message":message}, room=room)


if __name__ == "__main__":
    socketio.run(app, debug=True)