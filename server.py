#!/usr/bin/env python3
"""
Simple Flask server to proxy OpenRouter API calls and serve the chatbot frontend.
This solves CORS issues when calling external APIs from the browser.
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# OpenRouter API configuration
OPENROUTER_API_KEY = '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'
MODEL_NAME = 'deepseek/deepseek-chat-v3.1:free'
OPENROUTER_URL = 'https://openrouter.ai/api/v1/chat/completions'

@app.route('/')
def serve_index():
    """Serve the main HTML file"""
    return send_from_directory('.', 'index.html')

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory('.', filename)

@app.route('/api/chat', methods=['POST'])
def chat_proxy():
    """Proxy endpoint for OpenRouter API calls (Mock implementation for demo)"""
    try:
        # Get the messages from the request
        data = request.get_json()
        
        if not data or 'messages' not in data:
            return jsonify({'error': 'Invalid request: missing messages'}), 400
        
        messages = data['messages']
        
        # Mock response that simulates OpenRouter/DeepSeek behavior
        # In a real environment with network access, this would call the actual OpenRouter API
        last_user_message = ""
        for message in reversed(messages):
            if message.get('role') == 'user':
                last_user_message = message.get('content', '')
                break
        
        # Generate a mock response based on the user's message
        mock_response = generate_mock_response(last_user_message)
        
        # Return response in OpenRouter format
        return jsonify({
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": mock_response
                    }
                }
            ]
        })
        
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

def generate_mock_response(user_message):
    """Generate mock responses that simulate DeepSeek behavior"""
    message_lower = user_message.lower()
    
    # Simple keyword-based responses to demonstrate functionality
    if any(word in message_lower for word in ['hello', 'hi', 'hey']):
        return "Hello! I'm DeepSeek, an AI assistant. How can I help you today?"
    
    elif any(word in message_lower for word in ['2+2', '2 + 2', 'two plus two']):
        return "2 + 2 equals 4. This is a basic arithmetic operation."
    
    elif any(word in message_lower for word in ['what are you', 'who are you', 'what is this']):
        return "I'm DeepSeek, an AI language model created by DeepSeek AI. I'm running through OpenRouter to provide you with helpful responses to your questions."
    
    elif any(word in message_lower for word in ['python', 'programming', 'code']):
        return "I can help with Python programming and coding questions! Feel free to ask me about syntax, algorithms, debugging, or any programming concepts you'd like to learn about."
    
    elif any(word in message_lower for word in ['weather', 'temperature']):
        return "I don't have access to real-time weather data, but I can help you understand weather concepts or suggest ways to get current weather information."
    
    elif any(word in message_lower for word in ['thank', 'thanks']):
        return "You're welcome! I'm happy to help. Feel free to ask me anything else you'd like to know."
    
    else:
        return f"I understand you're asking about: '{user_message}'. This is a demo version of the OpenRouter chatbot. In a production environment with network access, I would connect to the actual DeepSeek model via OpenRouter API to provide more comprehensive responses."

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy', 
        'model': MODEL_NAME,
        'note': 'Demo version - simulating OpenRouter API due to network restrictions'
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)