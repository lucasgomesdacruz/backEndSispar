from datetime import timedelta
from os import environ # Traz para o arquivo o acesso as variáveis de ambiente
from dotenv import load_dotenv # Traz a funçõa para carregar as variaveis de ambiente nesse arquivo
import os



load_dotenv() # Carrega as variaveis de ambiente para este arquivo

class Config():    
    # SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD')
    SQLALCHEMY_DATABASE_URI = os.getenv('URL_DATABASE_PROD') 
    print("DATABASE URI:", SQLALCHEMY_DATABASE_URI)  
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    # print("DATABASE URI:", environ.get("URL_DATABASE_PROD2"))
    
    
      # Novo: Configurações específicas para JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)  # Tempo de vida do token
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)  # Se usar refresh tokens
    JWT_TOKEN_LOCATION = ['headers']  # Onde esperar o token
    JWT_HEADER_NAME = 'Authorization'  # Header padrão
    JWT_HEADER_TYPE = 'Bearer'  # Tipo do token
    

