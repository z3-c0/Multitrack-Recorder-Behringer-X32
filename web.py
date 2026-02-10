#!/usr/bin/env python3
from flask import Flask, render_template, request, jsonify
from audio_engine import AudioEngine

app = Flask(__name__)
engine = AudioEngine()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/status")
def status():
    return jsonify(engine.status())

@app.route("/record/start", methods=["POST"])
def rec_start():
    engine.start_record(request.json.get("name"))
    return jsonify(ok=True)

@app.route("/record/stop", methods=["POST"])
def rec_stop():
    engine.stop_record()
    return jsonify(ok=True)

@app.route("/play/start", methods=["POST"])
def play_start():
    engine.play(request.json["file"])
    return jsonify(ok=True)

@app.route("/play/seek", methods=["POST"])
def play_seek():
    engine.seek(float(request.json["pos"]))
    return jsonify(ok=True)

@app.route("/play/stop", methods=["POST"])
def play_stop():
    engine.stop()
    return jsonify(ok=True)

@app.route("/file/rename", methods=["POST"])
def file_rename():
    engine.rename_file(
        request.json["old"],
        request.json["new"]
    )
    return jsonify(ok=True)

@app.route("/file/delete", methods=["POST"])
def file_delete():
    engine.delete_file(request.json["file"])
    return jsonify(ok=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
