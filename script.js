// OpenRouter API configuration
const API_URL = '/api/chat';  // Use local proxy endpoint

// DOM elements
const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const sendButton = document.getElementById('sendButton');
const sendButtonText = document.getElementById('sendButtonText');
const loadingSpinner = document.getElementById('loadingSpinner');

// Chat history to maintain context
let chatHistory = [
    {
        role: "system",
        content: "You are a helpful AI assistant. Be friendly, informative, and concise in your responses."
    }
];

// Initialize the chatbot
document.addEventListener('DOMContentLoaded', function() {
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);
});

// Function to send a message
async function sendMessage() {
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Disable input while processing
    setLoading(true);
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Clear input
    messageInput.value = '';
    
    // Add user message to history
    chatHistory.push({
        role: "user",
        content: message
    });

    try {
        // Call OpenRouter API
        const response = await callOpenRouterAPI();
        
        if (response && response.content) {
            // Add bot response to chat
            addMessageToChat(response.content, 'bot');
            
            // Add bot response to history
            chatHistory.push({
                role: "assistant",
                content: response.content
            });
        } else {
            throw new Error('Invalid response format');
        }
    } catch (error) {
        console.error('Error:', error);
        addErrorMessage('Sorry, I encountered an error. Please try again.');
    } finally {
        setLoading(false);
    }
}

// Function to call OpenRouter API via proxy
async function callOpenRouterAPI() {
    const response = await fetch(API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            messages: chatHistory,
            temperature: 0.7,
            max_tokens: 1000
        })
    });

    if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(`API request failed: ${response.status} ${response.statusText}. ${errorData.error || ''}`);
    }

    const data = await response.json();
    
    if (!data.choices || !data.choices[0] || !data.choices[0].message) {
        throw new Error('Invalid API response structure');
    }

    return {
        content: data.choices[0].message.content
    };
}

// Function to add a message to the chat
function addMessageToChat(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = content;
    
    messageDiv.appendChild(messageContent);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to add an error message
function addErrorMessage(content) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = content;
    
    chatMessages.appendChild(errorDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to set loading state
function setLoading(isLoading) {
    sendButton.disabled = isLoading;
    messageInput.disabled = isLoading;
    
    if (isLoading) {
        sendButtonText.style.display = 'none';
        loadingSpinner.style.display = 'inline';
    } else {
        sendButtonText.style.display = 'inline';
        loadingSpinner.style.display = 'none';
    }
}
