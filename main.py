from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os

app = Flask(__name__)
CORS(app)

# API Key من OpenAI
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
client = OpenAI(api_key=OPENAI_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({'reply': 'لم أستلم رسالة'}), 400
        
        # إرسال للـ ChatGPT
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # أو gpt-4 لو عايز
            messages=[
                {"role": "system", "content": "أنت مساعد ذكي ومفيد في لعبة Roblox."},
                {"role": "user", "content": user_message}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content
        return jsonify({'reply': reply, 'status': 'success'})
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'reply': 'عذراً، حدث خطأ', 'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Server is running! 🟢'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Roblox ChatGPT Server'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
