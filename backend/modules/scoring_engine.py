def evaluate_response(text):
    # Placeholder scoring logic
    fluency_score = len(text.split()) / 10  # Words per second
    grammar_score = 0.8  # Placeholder
    vocabulary_score = 0.7  # Placeholder
    return {
        "fluency": fluency_score,
        "grammar": grammar_score,
        "vocabulary": vocabulary_score,
    }
