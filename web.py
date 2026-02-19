import os
from flask import Flask, render_template, send_from_directory
from flask_socketio import SocketIO, emit
from audio_engine import AudioEngine
RECORDINGS_DIR = "recordings"
os.makedirs(RECORDINGS_DIR, exist_ok=True)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading"
                    )

engine = AudioEngine(RECORDINGS_DIR)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/recordings/<path:filename>")
def recordings(filename):
    return send_from_directory(RECORDINGS_DIR, filename)


# ---------- SOCKET EVENTS ----------

@socketio.on("connect")
def handle_connect():
    emit_status()
    emit_file_list()


@socketio.on("start_record")
def start_record():
    try:
        engine.start_record()
        socketio.emit("status", {"msg": "Recording started"})
    except RuntimeError as e:
        emit("app_error", {"msg": str(e)})

@socketio.on("stop_record")
def stop_record():
    engine.stop_record()
    emit_status()
    emit_file_list()


@socketio.on("play")
def play(data):
    try:
        engine.play(data["file"])
        emit_status()
    except Exception as e:
        emit("app_error", {"msg": str(e)})

@socketio.on("stop_play")
def stop_play():
    engine.stop()
    emit_status()


@socketio.on("rename")
@socketio.on("rename")
def rename(data):
    try:
        os.rename(
            safe_path(data["old"]),
            safe_path(data["new"])
        )
    except Exception as e:
        emit("app_error", {"message": str(e)})


@socketio.on("delete")
def delete(data):
    try:
        os.remove(safe_path(data["file"]))
        emit_file_list()
    except Exception as e:
        emit("app_error", {"message": str(e)})


# ---------- HELPERS ----------

def safe_path(filename):
    return os.path.join(RECORDINGS_DIR, os.path.basename(filename))

def emit_status():
    socketio.emit("status", engine.status())


def emit_file_list():
    files = sorted(os.listdir(RECORDINGS_DIR))
    socketio.emit("files", files)


# ---------- RUN ----------
if __name__ == "__main__":
    print("Starting X32 Web Server...")
    socketio.run(app, host="0.0.0.0", port=5000, debug=False)
