from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from modules.speech_to_text import transcribe_audio
from modules.scoring_engine import evaluate_response
from modules.feedback_generator import generate_feedback, generate_pdf_report
import os

app = Flask(__name__)
CORS(app)

@app.route('/upload', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    mode = request.form.get('mode', 'practice')
    part = int(request.form.get('part', 0))

    file_path = "temp_audio.wav"
    file.save(file_path)

    if os.path.getsize(file_path) == 0:
        return jsonify({"error": "Uploaded file is empty"}), 400

    text = transcribe_audio(file_path)
    scores = evaluate_response(text)
    feedback = generate_feedback(text, scores, mode, part)

    os.remove(file_path)
    return jsonify({"feedback": feedback})

@app.route('/download-pdf', methods=['GET'])
def download_pdf():
    # Generate a sample PDF report (replace with actual data)
    pdf_path = "reports/user_reports/report.pdf"
    generate_pdf_report("Sample Feedback", pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)