# # # RESPONSÁVEL PELA CRIAÇÃO DA INSTÂNCIA E CONFIGURAR O FLASK

# from flask import Flask
# from flask_session import Session
# from flask_cors import CORS
# from flasgger import Swagger

# from datetime import timedelta
# from dotenv import load_dotenv
# import os

# # Controllers
# from src.controller.colaborador_controller import bp_colaborador
# from src.controller.reembolso_controller import bp_reembolso

# # Banco de dados
# from src.model import db
# from config import Config

# # Carrega variáveis do .env
# load_dotenv()

# # Configuração Swagger
# swagger_config = {
#     "headers": [],
#     "specs": [
#         {
#             "endpoint": 'apispec',
#             "route": '/apispec.json',
#             "rule_filter": lambda rule: True,
#             "model_filter": lambda tag: True,
#         }
#     ],
#     "static_url_path": "/flasgger_static",
#     "static_ui": True,
#     "specs_route": "/apidocs/",
# }

# def create_app():
#     app = Flask(__name__)

#     # 🔐 Chave secreta para sessões
#     app.secret_key = os.getenv('SECRET_KEY', 'chave-secreta-de-desenvolvimento')

#     # 🔧 Configuração de ambiente
#     app.config.from_object(Config)

#     # # 🛠️ Configurações de sessão
#     # app.config['SESSION_TYPE'] = 'filesystem'
#     # app.config['SESSION_PERMANENT'] = True
#     # app.permanent_session_lifetime = timedelta(days=7)
#     # app.config['SESSION_COOKIE_SECURE'] = False  # Requer HTTPS
#     # app.config['SESSION_COOKIE_SAMESITE'] = 'None'  # Necessário para cookies cross-origin
#     # app.config['SESSION_COOKIE_HTTPONLY'] = True
        
#     # 🛠️ Configurações de sessão para desenvolvimento local
#     app.config.update(
#         SESSION_TYPE='filesystem',
#         SESSION_FILE_DIR='./flask_sessions',
#         SESSION_PERMANENT=True,
#         PERMANENT_SESSION_LIFETIME=timedelta(days=7),
#         SESSION_COOKIE_NAME='flask_session',
#         SESSION_COOKIE_SECURE=False,  # False para localhost
#         SESSION_COOKIE_HTTPONLY=True,
#         SESSION_COOKIE_SAMESITE='Lax',  # 'Lax' para localhost
#         SESSION_SERIALIZATION_FORMAT='json'
#     )

#     Session(app)

#     # # 🔄 CORS habilitado com credenciais
#     # CORS(app, origins=[
#     #     "http://localhost:5173",
#     #     "https://sispar-omega.vercel.app"
#     # ], supports_credentials=True)
    
#      # 🔄 Configuração CORS (DEVE VIR DEPOIS da sessão)
#     CORS(app, resources={
#         r"/*": {
#             "origins": [
#                 "http://localhost:5173",
#                 "https://sispar-omega.vercel.app"
#             ],
#             "supports_credentials": True,  # Permite cookies
#             "allow_headers": ["Content-Type", "Authorization"],
#             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
#         }
#     })
    
#         # Headers CORS adicionais
#     @app.after_request
#     def after_request(response):
#         response.headers.add('Access-Control-Allow-Origin', 'https://sispar-omega.vercel.app')
#         response.headers.add('Access-Control-Allow-Credentials', 'true')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
#         response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
#         return response

#     # Registro de blueprints (rotas)
#     app.register_blueprint(bp_colaborador)
#     app.register_blueprint(bp_reembolso)

#     # Inicializa banco de dados
#     db.init_app(app)

#     # Swagger docs
#     Swagger(app, config=swagger_config)

#     # # Criação de tabelas (se não existirem)
#     # with app.app_context():
#     #     db.create_all()

#     # return app
    
#      # Criação de tabelas (se não existirem)
#     with app.app_context():
#         # Cria diretório para sessões se não existir
#         if not os.path.exists(app.config['SESSION_FILE_DIR']):
#             os.makedirs(app.config['SESSION_FILE_DIR'])
#         db.create_all()

#     return app
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
import redis 

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

    # 🔐 Chave secreta
    app.secret_key = os.getenv('SECRET_KEY', 'chave-secreta-padrao-insegura')

    # 🌍 Detecta ambiente
    is_production = os.getenv("FLASK_ENV") == "production"

    # 🔧 Configurações base
    app.config.update(
        SQLALCHEMY_DATABASE_URI=os.getenv("URL_DATABASE_PROD"),  # Use DATABASE_URL para prod
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_PERMANENT=True,
        PERMANENT_SESSION_LIFETIME=timedelta(days=7),
        SESSION_COOKIE_NAME='flask_session',
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_SERIALIZATION_FORMAT='json',
    )

    if is_production:
        redis_url = os.getenv("REDIS_URL")
        # 🌐 Produção (Ex: Redis, HTTPS, CORS externo)
        app.config.update(
            SESSION_TYPE='redis',
            SESSION_REDIS=redis.from_url(redis_url),  # aqui já passa a instância, não só a string
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_SAMESITE='None',
        )
    else:
        # 🧪 Desenvolvimento local
        app.config.update(
            SESSION_TYPE='filesystem',
            SESSION_FILE_DIR='./flask_sessions',
            SESSION_COOKIE_SECURE=False,
            SESSION_COOKIE_SAMESITE='Lax',
        )

    # Sessão
    Session(app)

    # CORS
    CORS(app, resources={
        r"/*": {
            "origins": [
                "http://localhost:5173",
                "https://sispar-omega.vercel.app"
            ],
            "supports_credentials": True,
            "allow_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
        }
    })

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', 'https://sispar-omega.vercel.app')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response

    # Banco de dados
    db.init_app(app)

    with app.app_context():
        if not is_production:
            # Cria diretório local de sessões, se necessário
            os.makedirs(app.config.get("SESSION_FILE_DIR", ""), exist_ok=True)
        db.create_all()

    # Swagger
    Swagger(app, config=swagger_config)

    # Rotas
    app.register_blueprint(bp_colaborador)
    app.register_blueprint(bp_reembolso)

    return app
