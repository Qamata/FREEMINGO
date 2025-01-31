from flask import Flask, request, jsonify
from modules.speech_to_text import transcribe_audio
from modules.examiner import generate_examiner_response
from modules.scoring_engine import evaluate_response
from modules.feedback_generator import generate_feedback
import os

app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    file_path = "temp_audio.wav"
    file.save(file_path)

    text = transcribe_audio(file_path)
    scores = evaluate_response(text)
    feedback = generate_feedback(scores)

    os.remove(file_path)
    return jsonify({"feedback": feedback})


if __name__ == '__main__':
    app.run(debug=True, port=5001)
