from flask import Flask, render_template, request, jsonify
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv('TOKEN', 'changeme')


# Cloud-based LLaMA 3 API (Groq only)
class CloudLLaMA3:
    def __init__(self):
        self.conversation_history = []
        self.api_url = 'https://api.groq.com/openai/v1/chat/completions'
        self.model = 'llama3-8b-8192'
        self.api_key = os.getenv('TOKEN', 'changeme')

    def chat(self, message):
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': self.model,
            'messages': [
                {'role': 'system', 'content': 'You are a helpful AI assistant powered by LLaMA 3.'},
                {'role': 'user', 'content': message}
            ],
            'temperature': 0.7,
            'max_tokens': 1000
        }
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                ai_reply = response.json()['choices'][0]['message']['content']
            elif response.status_code == 401:
                ai_reply = "❌ Invalid Groq API key. Get free key at: https://console.groq.com/keys"
            else:
                ai_reply = f"❌ Groq API error: {response.status_code}"
        except Exception as e:
            ai_reply = f"❌ Groq error: {str(e)}"

        self.conversation_history.append({
            'user': message,
            'ai': ai_reply,
            'timestamp': datetime.now().isoformat()
        })
        return ai_reply


# Initialize cloud LLaMA 3 (Groq only)
llama3_cloud = CloudLLaMA3()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    response = llama3_cloud.chat(message)
    return jsonify({
        'response': response,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/clear', methods=['POST'])
def clear_history():
    llama3_cloud.conversation_history.clear()
    return jsonify({'status': 'History cleared'})


# Remove setup guide for other providers


if __name__ == '__main__':
    print("🦙 Cloud LLaMA 3 (Groq only) - No Downloads Needed!")
    print("\n🌐 Access: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)