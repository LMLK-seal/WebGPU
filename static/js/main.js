document.addEventListener('DOMContentLoaded', () => {
    const pdfFile = document.getElementById('pdf-file');
    const uploadPdfBtn = document.getElementById('upload-pdf');
    const pdfStatus = document.getElementById('pdf-status');
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendMessageBtn = document.getElementById('send-message');
    const clearConversationBtn = document.getElementById('clear-conversation');

    uploadPdfBtn.addEventListener('click', uploadPdf);
    sendMessageBtn.addEventListener('click', sendMessage);
    clearConversationBtn.addEventListener('click', clearConversation);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    function uploadPdf() {
        const file = pdfFile.files[0];
        if (!file) {
            pdfStatus.textContent = 'Please select a PDF file.';
            return;
        }

        const formData = new FormData();
        formData.append('pdf', file);

        pdfStatus.textContent = 'Uploading and analyzing PDF...';

        fetch('/upload_pdf', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                pdfStatus.textContent = data.message;
                addMessage('ai', 'PDF analysis complete. You can now ask questions about the document.');
            } else {
                throw new Error(data.message || 'Unknown error occurred');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            pdfStatus.textContent = `Error: ${error.message}`;
        });
    }

    function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage('user', message);
        userInput.value = '';

        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ messages: [{"role": "user", "content": message}] })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === 'success') {
                data.messages.forEach(msg => addMessage('ai', msg));
            } else {
                throw new Error(data.message || 'Unknown error occurred');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('ai', `Error: ${error.message}`);
        });
    }

    function addMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message', `${sender}-message`);
        
        if (sender === 'ai') {
            // Use marked to convert Markdown to HTML
            messageElement.innerHTML = marked.parse(message);
        } else {
            messageElement.textContent = message;
        }
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    function clearConversation() {
        chatMessages.innerHTML = '';
    }
});
