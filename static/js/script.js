function sendMessage() {
    const input = document.getElementById('userMessage');
    const message = input.value.trim();
    if (message) {
        const chatbox = document.getElementById('chatbox');
        const newMessage = document.createElement('li');
        newMessage.textContent = message;
        newMessage.className = 'user-message';
        chatbox.appendChild(newMessage);
        input.value = '';

        // Simulate a bot response
        setTimeout(() => {
            const botResponse = document.createElement('li');
            botResponse.textContent = `Echo: ${message}`;
            botResponse.className = 'chatbot-message';
            chatbox.appendChild(botResponse);
        }, 500);
    }
}