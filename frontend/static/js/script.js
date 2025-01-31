const practiceModeBtn = document.getElementById('practice-mode-btn');
const testModeBtn = document.getElementById('test-mode-btn');
const testSection = document.getElementById('test-section');
const testPart = document.getElementById('test-part');
const testPrompt = document.getElementById('test-prompt');
const startBtn = document.getElementById('start-btn');
const stopBtn = document.getElementById('stop-btn');
const feedbackDiv = document.getElementById('feedback');
const downloadPdfBtn = document.getElementById('download-pdf-btn');

let mediaRecorder;
let audioChunks = [];
let currentMode = 'practice'; // 'practice' or 'test'
let testPartIndex = 0;
let testPrompts = [
    { part: "Part 1: Introduction", prompt: "Tell me about your hometown." },
    { part: "Part 2: Long Turn", prompt: "Describe a book you recently read." },
    { part: "Part 3: Two-Way Discussion", prompt: "Why do you think reading is important?" }
];

// Event listeners for mode selection
practiceModeBtn.addEventListener('click', () => {
    currentMode = 'practice';
    testSection.style.display = 'none';
    feedbackDiv.innerText = "Practice Mode: Start recording to get instant feedback.";
});

testModeBtn.addEventListener('click', () => {
    currentMode = 'test';
    testSection.style.display = 'block';
    testPartIndex = 0;
    startTest();
});

// Start the test mode
function startTest() {
    if (testPartIndex < testPrompts.length) {
        const { part, prompt } = testPrompts[testPartIndex];
        testPart.innerText = part;
        testPrompt.innerText = prompt;
    } else {
        feedbackDiv.innerText = "Test completed. Download your PDF report below.";
        downloadPdfBtn.style.display = 'block';
    }
}

// Event listener for Start Recording button
startBtn.addEventListener('click', async () => {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };
        mediaRecorder.onstop = sendAudioToBackend;
        mediaRecorder.start();
        startBtn.disabled = true;
        stopBtn.disabled = false;
        feedbackDiv.innerText = "Recording started...";
    } catch (error) {
        console.error("Error accessing microphone:", error);
        feedbackDiv.innerText = "Error accessing microphone. Please allow microphone access.";
    }
});

// Event listener for Stop Recording button
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
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('file', audioBlob, 'recording.wav');
        formData.append('mode', currentMode);
        formData.append('part', testPartIndex);

        const response = await fetch('http://127.0.0.1:5001/upload', {
            method: 'POST',
            body: formData,
        });

        const data = await response.json();
        feedbackDiv.innerText = data.feedback || "No feedback received.";

        if (currentMode === 'test') {
            testPartIndex++;
            startTest();
        }
    } catch (error) {
        console.error("Error sending audio to backend:", error);
        feedbackDiv.innerText = "Error processing audio. Please try again.";
    } finally {
        audioChunks = [];
    }
}

// Event listener for Download PDF button
downloadPdfBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('http://127.0.0.1:5001/download-pdf');
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'ielts_feedback_report.pdf';
        a.click();
    } catch (error) {
        console.error("Error downloading PDF:", error);
    }
});