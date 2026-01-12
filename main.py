from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)

# API Key من Google AI Studio (مجاني!)
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY', '')
genai.configure(api_key=GEMINI_API_KEY)

# إعداد الموديل
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        player_name = data.get('player', 'Player')
        
        if not user_message:
            return jsonify({'reply': 'لم أستلم رسالة'}), 400
        
        # تجهيز الـ Prompt
        prompt = f"""You are a helpful and friendly AI assistant in a Roblox game.

IMPORTANT RULES:
- Respond in the SAME LANGUAGE the user writes in
- If they write in Arabic, respond ONLY in Arabic
- If they write in English, respond ONLY in English
- Keep responses SHORT (2-3 sentences maximum)
- Be friendly and helpful

User message: {user_message}

Your response:"""
        
        # إرسال للـ Gemini
        response = model.generate_content(
            prompt,
            generation_config={
                'temperature': 0.7,
                'top_p': 0.95,
                'top_k': 40,
                'max_output_tokens': 200,
            }
        )
        
        # استخراج الرد
        reply = response.text.strip()
        
        return jsonify({'reply': reply, 'status': 'success'})
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error: {error_msg}")
        
        # رسائل خطأ مفيدة
        if "API_KEY_INVALID" in error_msg:
            return jsonify({
                'reply': 'API Key is invalid. Please check your Gemini API Key.',
                'error': 'invalid_key'
            }), 500
        elif "quota" in error_msg.lower():
            return jsonify({
                'reply': 'Daily limit reached. Please try again tomorrow.',
                'error': 'quota_exceeded'
            }), 500
        else:
            return jsonify({
                'reply': 'Sorry, an error occurred. Please try again!',
                'error': str(e)
            }), 500

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'Server is running! 🟢'})

@app.route('/', methods=['GET'])
def home():
    return jsonify({'message': 'Roblox AI Server (Google Gemini)'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
