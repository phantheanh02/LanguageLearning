const chatBox = document.getElementById('chatBox');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');

async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;

    // Disable input while processing
    messageInput.disabled = true;
    sendButton.disabled = true;

    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';

    try {
        const response = await fetch('/chat/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message })
        });

        const data = await response.json();

        // Add AI response to chat
        addMessage(data.response, 'ai');
    } catch (error) {
        console.error('Error:', error);
        addMessage('Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại.', 'ai');
    }

    // Re-enable input
    messageInput.disabled = false;
    sendButton.disabled = false;
    messageInput.focus();
}

function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}`;
    messageDiv.innerHTML = `
                <div class="message-content">
                    ${text}
                </div>
            `;
    chatBox.appendChild(messageDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}