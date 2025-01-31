// Get references to the buttons and feedback div
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const feedbackDiv = document.getElementById('feedback');

let mediaRecorder;
let audioChunks = [];

// Event listener for the Start Recording button
startBtn.addEventListener('click', async () => {
    try {
        // Request access to the user's microphone
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        // Collect audio data chunks
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        // When recording stops, send the audio to the backend
        mediaRecorder.onstop = sendAudioToBackend;

        // Start recording
        mediaRecorder.start();
        startBtn.disabled = true;
        stopBtn.disabled = false;
        feedbackDiv.innerText = "Recording started...";
    } catch (error) {
        console.error("Error accessing microphone:", error);
        feedbackDiv.innerText = "Error accessing microphone. Please allow microphone access.";
    }
});

// Event listener for the Stop Recording button
stopBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        startBtn.disabled = false;
        stopBtn.disabled = true;
        feedbackDiv.innerText = "Recording stopped. Processing...";
    }
});

// Function to send the recorded audio to the backend
async function sendAudioToBackend() {
    try {
        // Create a Blob from the recorded audio chunks
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });

        // Create a FormData object and append the audio file
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.wav');

        // Send the audio file to the backend
        const response = await fetch('http://127.0.0.1:5001/upload', {
            method: 'POST',
            body: formData,
        });

        // Parse the JSON response
        const data = await response.json();

        // Display the feedback
        feedbackDiv.innerText = data.feedback || "No feedback received.";
    } catch (error) {
        console.error("Error sending audio to backend:", error);
        feedbackDiv.innerText = "Error processing audio. Please try again.";
    } finally {
        // Reset the audio chunks for the next recording
        audioChunks = [];
    }
}