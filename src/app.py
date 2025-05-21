# # RESPONSÁVEL PELA CRIAÇÃO DA INSTÂNCIA E CONFIGURAR O FLASK

from flask import Flask
from flask_session import Session
from flask_cors import CORS
from flasgger import Swagger
from datetime import timedelta
from dotenv import load_dotenv
import os

# Controllers
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso

# Banco de dados
from src.model import db
from config import Config

# Carrega variáveis do .env
load_dotenv()

# Configuração Swagger
swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec',
            "route": '/apispec.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "static_ui": True,
    "specs_route": "/apidocs/",
}

def create_app():
    app = Flask(__name__)

    # 🔐 Chave secreta para sessões
    app.secret_key = os.getenv('SECRET_KEY', 'chave-secreta-de-desenvolvimento')

    # 🔧 Configuração de ambiente
    app.config.from_object(Config)

    # 🛠️ Configurações de sessão
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.permanent_session_lifetime = timedelta(days=7)
    app.config['SESSION_COOKIE_SECURE'] = True  # Requer HTTPS
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Necessário para cookies cross-origin
    app.config['SESSION_COOKIE_HTTPONLY'] = True

    Session(app)

    # 🔄 CORS habilitado com credenciais
    CORS(app, origins=[
        "http://localhost:5173",
        "https://sispar-omega.vercel.app"
    ], supports_credentials=True)

    # Registro de blueprints (rotas)
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)

    # Inicializa banco de dados
    db.init_app(app)

    # Swagger docs
    Swagger(app, config=swagger_config)

    # Criação de tabelas (se não existirem)
    with app.app_context():
        db.create_all()

    return app
