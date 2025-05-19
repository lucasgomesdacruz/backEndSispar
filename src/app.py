# RESPONSÁVEL PELA CRIAÇÃO DA INSTÂNCIA E CONFIGURAR O FLASK
# CREATE_APP() -> 
from flask import Flask, request
from src.controller.colaborador_controller import bp_colaborador
from src.controller.reembolso_controller import bp_reembolso 
from src.controller.chatbot_controller import chatbot_bp
from flask_session import Session

from datetime import timedelta



from src.model import db
from config import Config
from flask_cors import CORS
from flasgger import Swagger
import os

# Carregando variáveis de ambiente
from dotenv import load_dotenv
load_dotenv()

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
    "static_url_path": '/flasgger_static', 
    "static_ui": True,
    "specs_route": '/apidocs/',
}

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv('SECRET_KEY')
    # CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:5173", "https://sispar-omega.vercel.app"]}}, supports_credentials=True)
    
    

    
    app.register_blueprint(bp_reembolso)
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(chatbot_bp)
    
    app.config.from_object(Config) # Trouxemos a configuração do ambiente de desenvolvimento
    db.init_app(app) # Se inicia a conexão com o banco de dados

    Swagger(app, config=swagger_config) # <- Instanciando o Swagger e adicionando as configurações
    
    
    app.secret_key = os.environ.get('SECRET_KEY', 'chave-secreta-de-desenvolvimento')

    
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.permanent_session_lifetime = timedelta(days=7)
    # app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # ou 'None' se estiver em domínios diferentes + HTTPS
    app.config['SESSION_COOKIE_SECURE'] = True       # Necessário se o backend usar HTTPS
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Para permitir cookies cross-origin
    
    Session(app)
    
    
    @app.after_request
    def after_request(response):
        origin = request.headers.get('Origin')
        if origin in ['http://localhost:5173', 'https://sispar-omega.vercel.app']:
            response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization'
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,PUT,DELETE,OPTIONS'
        return response
    
    with app.app_context():
        db.create_all() #Cria as tabelas caso elas não existam

    return app