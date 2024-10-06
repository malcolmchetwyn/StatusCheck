

async function sendMessage() {
    const messageInput = document.getElementById('message');
    const chatBox = document.getElementById('chat');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    messageInput.value = ''; // Clear the input field after submission

    // Display user's message aligned to the right
    const userMessageDiv = document.createElement('div');
    userMessageDiv.className = 'message user';
    
    // Structure the user message with label and content
    userMessageDiv.innerHTML = `<div class="label">Me:</div><p>${message}</p>`;
    chatBox.appendChild(userMessageDiv);

    // Prepare AI response container on the left
    const aiMessageDiv = document.createElement('div');
    aiMessageDiv.className = 'message ai';
    aiMessageDiv.innerHTML = '<strong>Shadow Analyst:</strong> <em>Typing...</em>';
    chatBox.appendChild(aiMessageDiv);

    // Scroll to the bottom
    chatBox.scrollTop = chatBox.scrollHeight;

    try {
        // Send the message to the server
        const response = await fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.statusText}`);
        }

        if (!response.body) {
            throw new Error('ReadableStream not supported in this browser.');
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder('utf-8');

        let aiResponseBuffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            const chunk = decoder.decode(value, { stream: true });
            aiResponseBuffer += chunk;

            // Parse and sanitize the accumulated Markdown text
            const html = DOMPurify.sanitize(marked.parse(aiResponseBuffer));

            // Update the AI message div's innerHTML with sanitized HTML
            aiMessageDiv.innerHTML = '<strong>Shadow Analyst:</strong> ' + html;

            // Scroll to the bottom as new content arrives
            chatBox.scrollTop = chatBox.scrollHeight;
        }
    } catch (error) {
        aiMessageDiv.innerHTML = '<strong>Shadow Analyst:</strong> [Error] ' + error.message;
    }
}

// Send message on Enter key press
document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('message');
    
    // Trigger sendMessage function when 'Enter' is pressed
    messageInput.addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            event.preventDefault();
            sendMessage();
        }
    });
});
