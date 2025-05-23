# # Blueprint 
# from flask import Blueprint, request, jsonify, session
# from src.model.colaborador_model import Colaborador
# from src.model import db
# from src.security.security import hash_senha, checar_senha
# from flasgger import swag_from
# import bcrypt

# bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

# @bp_colaborador.route('/todos-colaboradores', methods=['GET'])
# @swag_from('../docs/colaborador/todos_colaboradores.yml')
# def pegar_dados_todos_colaboradores():
    
#     colaboradores = db.session.execute(
#         db.select(Colaborador)
#     ).scalars().all()
    
#                     #Expressão                  item            iteravel 
#     colaboradores = [ colaborador.all_data() for colaborador in colaboradores ]
    
#     return jsonify(colaboradores), 200


# # TAREFA -> VALIDAÇÃO DO CAMPO CRACHA. NÃO PODEMOS TER DUPLICATAS

# @bp_colaborador.route('/cadastrar', methods=['POST'])
# @swag_from('../docs/colaborador/cadastrar_colaborador.yml')
# def cadastrar_colaborador():
    
    
#     dados_requisicao = request.get_json()
    
#      # Verificar se o email já existe
#     colaborador_existente = Colaborador.query.filter_by(email=dados_requisicao['email']).first()
#     if colaborador_existente:
#         return jsonify({'mensagem': 'Email já cadastrado'}), 400
    
#     novo_colaborador = Colaborador(
#         nome=dados_requisicao['nome'],
#         email=dados_requisicao['email'],
#         senha=hash_senha(dados_requisicao['senha']),
#         cargo=dados_requisicao['cargo'],
#         salario=dados_requisicao['salario']
#     )
    
# # INSERT INTO tb_colaborador (nome, email, senha, cargo, salario) VALUES ('samuel', 'samueltigrao@gmail.com', '1234', 'Cliente', 120)
#     db.session.add(novo_colaborador) 
#     db.session.commit() # Clique no raio do Workbench
    
#     return jsonify({'mensagem': 'Colaborador cadastrado com sucesso'}), 201
    
# @bp_colaborador.route('/login', methods=['POST'])
# @swag_from('../docs/colaborador/login_colaborador.yml')
# def login():
#     dados_requisicao = request.get_json()
#     email = dados_requisicao.get('email')
#     senha = dados_requisicao.get('senha')

#     if not email or not senha:
#         return jsonify({'mensagem': 'Todos os campos devem ser preenchidos'}), 400

#     colaborador = db.session.execute(
#         db.select(Colaborador).where(Colaborador.email == email)
#     ).scalar()

#     if not colaborador:
#         return jsonify({'mensagem': 'O usuário não foi encontrado'}), 404

#     def checar_senha(senha, senha_hash):
#         if not senha_hash:
#             return False

#         # Verifica se o hash está em string hexadecimal e converte
#         if isinstance(senha_hash, str):
#             if senha_hash.startswith('\\x') or senha_hash.startswith('0x'):
#                 senha_hash = bytes.fromhex(senha_hash[2:])
#             else:
#                 senha_hash = senha_hash.encode('utf-8')

#         return bcrypt.checkpw(senha.encode('utf-8'), senha_hash)

#     # Debug prints úteis (opcional)
#     print("Senha recebida:", senha)
#     print("Hash no banco:", repr(colaborador.senha))  # mostra se tem \x

#     if checar_senha(senha, colaborador.senha):
#         session.permanent = True  # ESSENCIAL PARA MANTER A SESSÃO
#         session['colaborador_id'] = colaborador.id
#         return jsonify({'mensagem': 'Login realizado com sucesso'}), 200

#     return jsonify({'mensagem': 'Senha incorreta'}), 401



# @bp_colaborador.route('/perfil', methods=['GET'])
# @swag_from('../docs/colaborador/perfil_colaborador.yml')
# def pegar_perfil_colaborador():
#     colaborador_id = session.get('colaborador_id')
#     session.permanent = True 
    
#     # Verifica se o colaborador_id está presente na sessão
#     print("Session no perfil:", dict(session))
#     print("Colaborador ID:", colaborador_id)
    
#     if not colaborador_id:
#         # Se não houver colaborador_id na sessão, retorna 401 (não autorizado)
#         return jsonify({'mensagem': 'Colaborador não logado'}), 401

#     # Busca o colaborador no banco de dados usando o ID da sessão
#     # colaborador = db.session.get(Colaborador, colaborador_id)
#     colaborador = db.session.query(Colaborador).filter_by(id=colaborador_id).first()

#     # Se o colaborador não for encontrado, retorna 404 (não encontrado)
#     if not colaborador:
#         return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

#     # Retorna as informações do colaborador no formato JSON
#     return jsonify({
#         'id': colaborador.id,
#         'nome': colaborador.nome,
#         'cargo': colaborador.cargo,
#         'email': colaborador.email
#     }), 200

# @bp_colaborador.route('/atualizar-perfil', methods=['PUT'])
# @swag_from('../docs/colaborador/atualizar_perfil_colaborador.yml')
# def atualizar_perfil_colaborador():
#     colaborador_id = session.get('colaborador_id')
#     session.permanent = True

#     if not colaborador_id:
#         return jsonify({'mensagem': 'Colaborador não logado'}), 401

#     colaborador = db.session.query(Colaborador).filter_by(id=colaborador_id).first()

#     if not colaborador:
#         return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

#     dados = request.get_json()

#     # Atualiza os campos permitidos
#     if 'nome' in dados:
#         colaborador.nome = dados['nome']
#     if 'cargo' in dados:
#         colaborador.cargo = dados['cargo']
#     if 'email' in dados:
#         # Verifica se o novo e-mail já está em uso por outro usuário
#         email_existente = Colaborador.query.filter_by(email=dados['email']).first()
#         if email_existente and email_existente.id != colaborador.id:
#             return jsonify({'mensagem': 'Email já está em uso por outro colaborador'}), 400
#         colaborador.email = dados['email']
#     if 'senha' in dados:
#         colaborador.senha = hash_senha(dados['senha'])

#     db.session.commit()

#     return jsonify({'mensagem': 'Perfil atualizado com sucesso'}), 200

from flask import Blueprint, current_app, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from src.security.jwt_manager import generate_token, token_required
from flasgger import swag_from
import bcrypt

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

@bp_colaborador.route('/todos-colaboradores', methods=['GET'])
@token_required  # Adicione esta linha se quiser restringir a admins
@swag_from('../docs/colaborador/todos_colaboradores.yml')
def pegar_dados_todos_colaboradores(current_user):
    # Verifique se o usuário é admin (opcional)
    # if not is_admin(current_user):
    #     return jsonify({'mensagem': 'Acesso não autorizado'}), 403
    
    colaboradores = db.session.execute(
        db.select(Colaborador)
    ).scalars().all()
    
    colaboradores = [colaborador.all_data() for colaborador in colaboradores]
    
    return jsonify(colaboradores), 200

@bp_colaborador.route('/cadastrar', methods=['POST'])
@swag_from('../docs/colaborador/cadastrar_colaborador.yml')
def cadastrar_colaborador():
    dados_requisicao = request.get_json()
    
    # Verificar se o email já existe
    colaborador_existente = Colaborador.query.filter_by(email=dados_requisicao['email']).first()
    if colaborador_existente:
        return jsonify({'mensagem': 'Email já cadastrado'}), 400
    
    novo_colaborador = Colaborador(
        nome=dados_requisicao['nome'],
        email=dados_requisicao['email'],
        senha=hash_senha(dados_requisicao['senha']),
        cargo=dados_requisicao['cargo'],
        salario=dados_requisicao['salario']
    )
    
    db.session.add(novo_colaborador) 
    db.session.commit()
    
    return jsonify({'mensagem': 'Colaborador cadastrado com sucesso'}), 201
    
@bp_colaborador.route('/login', methods=['POST'])
@swag_from('../docs/colaborador/login_colaborador.yml')
def login():
    dados_requisicao = request.get_json()
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')

    if not email or not senha:
        return jsonify({'mensagem': 'Todos os campos devem ser preenchidos'}), 400

    try:
        colaborador = db.session.execute(
            db.select(Colaborador).where(Colaborador.email == email)
        ).scalar()

        if not colaborador:
            return jsonify({'mensagem': 'Credenciais inválidas'}), 401

        # Verificação segura da senha
        if not checar_senha(senha, colaborador.senha):
            return jsonify({'mensagem': 'Credenciais inválidas'}), 401

        token = generate_token(colaborador.id)
        return jsonify({
            'mensagem': 'Login realizado com sucesso',
            'token': token,
            'colaborador': {
                'id': colaborador.id,
                'nome': colaborador.nome,
                'email': colaborador.email,
                'cargo': colaborador.cargo
            }
        }), 200

    except Exception as e:
        current_app.logger.error(f"Erro no processo de login: {str(e)}", exc_info=True)
        return jsonify({'mensagem': 'Erro interno no servidor'}), 500
    
@bp_colaborador.route('/perfil', methods=['GET'])
@token_required
@swag_from('../docs/colaborador/perfil_colaborador.yml')
def pegar_perfil_colaborador(current_user):
    colaborador = db.session.query(Colaborador).filter_by(id=current_user).first()

    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    return jsonify({
        'id': colaborador.id,
        'nome': colaborador.nome,
        'cargo': colaborador.cargo,
        'email': colaborador.email
    }), 200

@bp_colaborador.route('/atualizar-perfil', methods=['PUT'])
@token_required
@swag_from('../docs/colaborador/atualizar_perfil_colaborador.yml')
def atualizar_perfil_colaborador(current_user):
    colaborador = db.session.query(Colaborador).filter_by(id=current_user).first()

    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    dados = request.get_json()

    # Atualiza os campos permitidos
    if 'nome' in dados:
        colaborador.nome = dados['nome']
    if 'cargo' in dados:
        colaborador.cargo = dados['cargo']
    if 'email' in dados:
        # Verifica se o novo e-mail já está em uso por outro usuário
        email_existente = Colaborador.query.filter_by(email=dados['email']).first()
        if email_existente and email_existente.id != colaborador.id:
            return jsonify({'mensagem': 'Email já está em uso por outro colaborador'}), 400
        colaborador.email = dados['email']
    if 'senha' in dados:
        colaborador.senha = hash_senha(dados['senha'])

    db.session.commit()

    return jsonify({'mensagem': 'Perfil atualizado com sucesso'}), 200