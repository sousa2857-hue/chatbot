import sys,os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
from core.prompt_mestre import PromptMestre

app = Flask(__name__)
CORS(app)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
prompt = PromptMestre()

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    
    resposta = client.chat.completitions.create(
        model="llama-3.1-8b-instruct",
        messages=[
            {"role": "system", "content": prompt.get_prompt()},
            {"role": "user", "content": user_message}
        ]
    )

    return jsonify({"resposta": resposta.choices[0].message.content})