const recordBtn = document.getElementById('recordBtn');
const playback = document.getElementById('playback');
const recordStatus = document.getElementById('recordStatus');

let mediaRecorder;
let recordedChunks = [];

async function startRecording() {
    recordStatus.textContent = '';
    recordedChunks = [];
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.ondataavailable = e => {
        if (e.data.size > 0) recordedChunks.push(e.data);
    };
    mediaRecorder.onstop = async () => {
        const blob = new Blob(recordedChunks, { type: 'audio/webm' });
        const url = URL.createObjectURL(blob);
        playback.src = url;
        playback.hidden = false;

        // Send blob to server as form-data
        const form = new FormData();
        // Use filename with .webm extension
        form.append('file', blob, 'recording.webm');
        // Add current image name
        const currentImage = recordIcon.src.split('/').pop();
        form.append('image', currentImage);

        recordStatus.textContent = 'Uploading...';
        try {
            const resp = await fetch('/recognize', {
                method: 'POST',
                body: form,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            });

            if (!resp.ok) throw new Error('Server error: ' + resp.statusText);

            const data = await resp.json();
            if (data.error) {
                recordStatus.textContent = 'Error: ' + data.error;
            } else {
                const lang = ' (Kết quả: ' + data.language + ')'
                recordStatus.textContent = 'Transcription: ' + data.transcription + '\n' + lang;
            }
        } catch (err) {
            recordStatus.textContent = 'Upload failed: ' + err.message;
        }
    };

    mediaRecorder.start();
    recordBtn.textContent = 'Stop Recording';
    recordStatus.textContent = 'Recording...';
}

function stopRecording() {

    if (mediaRecorder && mediaRecorder.state !== 'inactive') mediaRecorder.stop();
    recordBtn.textContent = 'Start Recording';
}

recordBtn.addEventListener('click', async (e) => {
    e.preventDefault();
    if (!mediaRecorder || mediaRecorder.state === 'inactive') {
        await startRecording();
    } else {
        stopRecording();
    }
});

function copyToClipboard() {
    const copyButton = document.querySelector('.copy-button');
    const transcriptionText = document.querySelector('.transcription-box p');
    navigator.clipboard.writeText(transcriptionText.textContent);
    copyButton.textContent = 'Copied';
    copyButton.disabled = true;
}

// Image navigation
const nextBtn = document.getElementById('nextBtn');
const recordIcon = document.getElementById('recordIcon');

nextBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/next-image');
        if (response.ok) {
            const data = await response.json();
            recordIcon.src = `/static/imgs/${data.image}`;
        } else {
            console.error('Failed to get next image');
        }
    } catch (error) {
        console.error('Error:', error);
    }
});
