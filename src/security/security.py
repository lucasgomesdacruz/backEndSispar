import bcrypt
import re

def hash_senha(senha: str) -> str:
    """Gera um hash BCrypt seguro para a senha"""
    if not senha:
        raise ValueError("Senha não pode ser vazia")
    
    salt = bcrypt.gensalt()
    hash_bytes = bcrypt.hashpw(senha.encode('utf-8'), salt)
    return hash_bytes.decode('utf-8')

def checar_senha(senha: str, senha_hash: str) -> bool:
    """Verifica se a senha corresponde ao hash"""
    if not senha or not senha_hash:
        return False
    
    try:
        # Converte o hash para bytes se necessário
        if isinstance(senha_hash, str):
            if senha_hash.startswith('\\x') or senha_hash.startswith('0x'):
                # Se estiver em formato hexadecimal
                senha_hash = bytes.fromhex(senha_hash[2:])
            elif senha_hash.startswith('$2b$'):
                # Formato BCrypt padrão
                senha_hash = senha_hash.encode('utf-8')
            else:
                # Tentativa de decodificar como string normal
                senha_hash = senha_hash.encode('utf-8')
        
        return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)
    except Exception as e:
        current_app.logger.error(f"Erro ao verificar senha: {str(e)}")
        return False