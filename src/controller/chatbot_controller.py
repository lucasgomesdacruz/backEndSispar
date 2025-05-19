
# src/controller/chatbot_controller.py
from flask import Blueprint, request, jsonify
import openai
import os

from dotenv import load_dotenv
load_dotenv()

chatbot_bp = Blueprint('chatbot', __name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

@chatbot_bp.route('/chatbot', methods=['POST'])
def chatbot_response():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"error": "Mensagem não fornecida"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente virtual chamado 'Assistente SISPAR'. "
                        "Seu papel é ajudar usuários a entender e utilizar o sistema de reembolso SISPAR. "
                        "Explique como solicitar reembolso, como acompanhar o status, e outras dúvidas comuns. "
                        "Seja claro, objetivo e cordial."
                    )
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        return jsonify({"response": reply})
    except Exception as e:
        print("Erro:", e) 
        return jsonify({"error": str(e)}), 500
