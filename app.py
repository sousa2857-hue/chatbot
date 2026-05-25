from flask import Flask, request, jsonify
from core.prompt_mestre import PromptMestre
from flask_cors import CORS
from groq import Groq

from services.ia_service import IAService

# cria aplicação
app = Flask(__name__)

# libera comunicação com frontend
CORS(app)

# conecta API Groq
# cria um cliente Groq em nível de módulo (não usar `self` fora de classes)
cliente = Groq(
    api_key="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"
)

# Inicializa os serviços de IA e o prompt mestre
ia_service = IAService()
prompt_mestre = PromptMestre()
# Rota para a página inicial (/) - serve o arquivo index.html
@app.route('/')
def index():
    return app.send_static_file('index.html')

# Rota para o chat (/chat) - recebe as mensagens do usuário
@app.route('/chat', methods=['POST'])
def chat():

    user_message = request.json.get('mensagem')

    if not user_message:
        return jsonify({
            'resposta': 'Por favor, forneça uma mensagem.'
        }), 400

    system_prompt = prompt_mestre.get_prompt()

    historico = [
        {
            "role": "user",
            "content": user_message
        }
    ]

    response = ia_service.enviar_mensagem(
        historico,
        system_prompt
    )

    return jsonify({
        'resposta': response
    })

# Inicia o servidor Flask quando o script é executado diretamente
if __name__ == '__main__':
    app.run(
debug=True,
port=5000
)