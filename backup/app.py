
from flask import Flask, request, jsonify, send_file
import subprocess
import os
import uuid

app = Flask(__name__)

MODEL_PATH = "models/pt_BR/pt_BR-faber-medium.onnx"
CONFIG_PATH = "models/pt_BR/pt_BR-faber-medium.onnx.json"

@app.route("/tts", methods=["POST"])
def tts():
    data = request.json
    text = data.get("text")
    if not text:
        return jsonify({"error": "Missing 'text'"}), 400

    output_path = f"output_{uuid.uuid4().hex}.wav"

    command = [
        "python3", "piper/piper.py",
        "--model", MODEL_PATH,
        "--config", CONFIG_PATH,
        "--output_file", output_path
    ]

    try:
        subprocess.run(command, input=text.encode(), check=True)
    except subprocess.CalledProcessError as e:
        return jsonify({"error": "Piper failed", "details": str(e)}), 500

    return send_file(output_path, mimetype="audio/wav")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
