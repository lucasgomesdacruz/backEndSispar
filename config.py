from os import environ # Traz para o arquivo o acesso as variáveis de ambiente
from dotenv import load_dotenv # Traz a funçõa para carregar as variaveis de ambiente nesse arquivo
import os


load_dotenv() # Carrega as variaveis de ambiente para este arquivo

class Config():    
    # SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD1')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    print("DATABASE URI:", environ.get("URL_DATABASE_PROD1"))
    

