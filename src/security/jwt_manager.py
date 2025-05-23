import jwt
import datetime
from flask import current_app, jsonify, request
from functools import wraps
from typing import Any, Callable, Union
from jwt.exceptions import PyJWTError

def generate_token(colaborador_id: int) -> str:
    """Gera um token JWT válido para autenticação."""
    try:
        payload = {
            'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=7),
            'iat': datetime.datetime.now(datetime.timezone.utc),
            'sub': str(colaborador_id)  # Convertemos para string
        }
        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )
    except Exception as e:
        current_app.logger.error(f"Falha ao gerar token: {str(e)}")
        raise RuntimeError("Falha ao gerar token de autenticação")

def token_required(f: Callable) -> Callable:
    """Decorator para verificar tokens JWT."""
    @wraps(f)
    def decorated(*args: Any, **kwargs: Any) -> Any:
        token = None
        
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            return jsonify({'mensagem': 'Token não fornecido'}), 401
            
        try:
            payload = jwt.decode(
                token, 
                current_app.config['SECRET_KEY'], 
                algorithms=['HS256']
            )
            return f(payload['sub'], *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify({'mensagem': 'Token expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'mensagem': 'Token inválido'}), 401
            
    return decorated