# OpenRouter AI Chatbot

A web-based AI chatbot that uses OpenRouter to access the DeepSeek Chat v3.1 model.

## Features

- Clean, modern chat interface
- Real-time messaging with AI
- Responsive design that works on desktop and mobile
- Error handling and loading states
- Conversation history maintained during session

## Configuration

The chatbot is configured to use:
- **Model**: `deepseek/deepseek-chat-v3.1:free`
- **API**: OpenRouter (https://openrouter.ai)
- **API Key**: Configured in `server.py`

## Setup & Installation

### Prerequisites

- Python 3.7+
- pip (Python package installer)

### Installation

1. Clone this repository
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Update the API key in `server.py` if needed:
   ```python
   OPENROUTER_API_KEY = 'your-openrouter-api-key'
   ```

4. Start the server:
   ```bash
   python server.py
   ```

5. Open your browser and go to `http://localhost:5000`

## File Structure

- `index.html` - Main HTML interface
- `styles.css` - Stylesheet for the chat interface
- `script.js` - Frontend JavaScript code
- `server.py` - Flask backend server with OpenRouter API proxy
- `requirements.txt` - Python dependencies
- `README.md` - This documentation

## How It Works

1. **Frontend**: The HTML/CSS/JS provides a clean chat interface
2. **Backend Proxy**: Flask server handles API requests to avoid CORS issues
3. **OpenRouter Integration**: Proxies requests to OpenRouter's API
4. **DeepSeek Model**: Uses the free DeepSeek Chat v3.1 model for responses

## API Endpoints

- `GET /` - Serves the main chat interface
- `POST /api/chat` - Proxy endpoint for OpenRouter API calls
- `GET /health` - Health check endpoint

## Demo Mode

In environments with network restrictions, the application runs in demo mode with simulated responses that demonstrate the functionality. The actual OpenRouter API integration is ready and will work in environments with full internet access.

## Production Deployment

For production use:

1. Use a production WSGI server (e.g., Gunicorn)
2. Set environment variables for configuration
3. Implement proper error logging
4. Add rate limiting and authentication as needed
5. Use HTTPS for secure communication

## OpenRouter API

This chatbot uses OpenRouter (https://openrouter.ai) which provides unified access to multiple AI models. OpenRouter offers:

- Access to various AI models including DeepSeek, GPT, Claude, and more
- Competitive pricing with free tier options
- Simple REST API interface
- Good documentation and support

To get your own API key:
1. Visit https://openrouter.ai
2. Sign up for an account
3. Generate an API key from your dashboard
4. Replace the key in `server.py`

## License

This project is open source and available under the MIT License.