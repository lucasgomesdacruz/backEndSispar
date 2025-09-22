from datetime import timedelta
from os import environ
from dotenv import load_dotenv
import os

# Carregar variáveis do .env localmente (em produção no Render, as variáveis já vêm do ambiente)
load_dotenv()

class Config:
    # Banco de dados
    SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_PROD") or os.getenv("URL_DATABASE_PROD")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug opcional – só imprime se variável estiver vazia
    if not SQLALCHEMY_DATABASE_URI:
        print("⚠️ URL_DATABASE_PROD não encontrada nas variáveis de ambiente!")

    # JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = "Authorization"
    JWT_HEADER_TYPE = "Bearer"
