from flask import Flask, request, jsonify
from flask_cors import CORS  # Import the CORS module
from modules.speech_to_text import transcribe_audio
from modules.scoring_engine import evaluate_response
from modules.feedback_generator import generate_feedback
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_path = "temp_audio.wav"
    file.save(file_path)

    # Verify the file is not empty
    if os.path.getsize(file_path) == 0:
        return jsonify({"error": "Uploaded file is empty"}), 400

    text = transcribe_audio(file_path)
    scores = evaluate_response(text)
    feedback = generate_feedback(scores)

    os.remove(file_path)
    return jsonify({"feedback": feedback})

if __name__ == '__main__':
    app.run(debug=True, port=5001)