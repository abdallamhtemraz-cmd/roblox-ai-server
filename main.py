from flask import Flask, request, jsonify
from flask_cors import CORS
import anthropic
import os

app = Flask(__name__)
CORS(app)

# هناخد الـ API Key من Environment Variables
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'reply': 'لم أستلم رسالة'}), 400
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=500,
            messages=[{"role": "user", "content": user_message}]
        )
        
        reply = message.content[0].text
        return jsonify({'reply': reply, 'status': 'success'})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'reply': 'عذراً، حدث خطأ'}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Server is running! 🟢'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Roblox AI Server is running!'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
