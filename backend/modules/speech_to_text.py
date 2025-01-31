import speech_recognition as sr

def transcribe_audio(file_path):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)  # Read the entire audio file
        text = recognizer.recognize_google(audio)  # Use Google's Speech-to-Text API
        return text
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "API unavailable"
    except Exception as e:
        return f"Error processing audio: {str(e)}"