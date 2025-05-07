from os import environ # Traz para o arquivo o acesso as variáveis de ambiente
from dotenv import load_dotenv # Traz a funçõa para carregar as variaveis de ambiente nesse arquivo 

load_dotenv() # Carrega as variaveis de ambiente para este arquivo

class Config():
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_DEV')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 