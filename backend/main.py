from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from modules.speech_to_text import transcribe_audio
from modules.scoring_engine import evaluate_response
from modules.feedback_generator import generate_feedback, generate_pdf_report
import os
import openai

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")  # Store your API key in environment variables

def generate_examiner_response(user_input):
    """
    Generate an examiner-like response using OpenAI GPT-4.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # Use GPT-4
            messages=[
                {"role": "system", "content": "You are an IELTS examiner. Ask follow-up questions or provide feedback based on the candidate's response."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=100,  # Limit the response length
            temperature=0.7,  # Control creativity (0 = strict, 1 = creative)
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error generating response: {str(e)}"

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

    # Transcribe the audio
    text = transcribe_audio(file_path)

    # Generate examiner response
    examiner_response = generate_examiner_response(text)

    # Evaluate the response
    scores = evaluate_response(text)
    feedback = generate_feedback(text, scores, mode, part)

    os.remove(file_path)
    return jsonify({
        "feedback": feedback,
        "examiner_response": examiner_response
    })

@app.route('/download-pdf', methods=['GET'])
def download_pdf():
    # Generate a sample PDF report (replace with actual data)
    pdf_path = "reports/user_reports/report.pdf"
    generate_pdf_report("Sample Feedback", pdf_path)
    return send_file(pdf_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True, port=5001)