from os import environ # Traz para o arquivo o acesso as variáveis de ambiente
from dotenv import load_dotenv # Traz a funçõa para carregar as variaveis de ambiente nesse arquivo



load_dotenv() # Carrega as variaveis de ambiente para este arquivo

class Config():    
<<<<<<< HEAD
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_DEV1')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 
    # SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD')
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    # print("DATABASE URI:", environ.get("URL_DATABASE_PROD"))
=======
    SQLALCHEMY_DATABASE_URI = environ.get('URL_DATABASE_PROD1')
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') 
    print("DATABASE URI:", SQLALCHEMY_DATABASE_URI)  
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    print("DATABASE URI:", environ.get("URL_DATABASE_PROD1"))
>>>>>>> e39063b938459bbb6eada149ebc77fe9e64687a2
    

