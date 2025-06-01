from flask import Blueprint, request, jsonify, session
from src.model.reembolso_model import Reembolso
from src.model import db
from datetime import datetime
from flasgger import swag_from

bp_reembolso = Blueprint('reembolsos', __name__, url_prefix='/colaborador')


@bp_reembolso.route('/reembolsos', methods=['POST', 'OPTIONS'])
@swag_from('../docs/reembolso/create_reembolso.yml')
def criar_reembolso():
    if request.method == "OPTIONS":
        return '', 200

    if 'colaborador_id' not in session:
        return jsonify({'mensagem': 'Login necessário para criar reembolso'}), 401

    data = request.json
    try:
        novo_reembolso = Reembolso(
            colaborador=data['colaborador'],
            empresa=data['empresa'],
            num_prestacao=data['num_prestacao'],
            descricao=data.get('descricao'),
            data=datetime.strptime(data['data'], '%Y-%m-%d'),
            tipo_reembolso=data['tipo_reembolso'],
            centro_custo=data['centro_custo'],
            ordem_interna=data.get('ordem_interna'),
            divisao=data.get('divisao'),
            pep=data.get('pep'),
            moeda=data['moeda'],
            distancia_km=data.get('distancia_km'),
            valor_km=data.get('valor_km'),
            valor_faturado=data['valor_faturado'],
            despesa=data.get('despesa'),
            id_colaborador=session.get('colaborador_id'),  # PEGA O COLABORADOR DA SESSÃO
            status=data.get('status', 'Em analise')
        )
        db.session.add(novo_reembolso)
        db.session.commit()
        return jsonify({'message': 'Reembolso criado com sucesso!'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

    
@bp_reembolso.route('/reembolsos/<int:num_prestacao>', methods=['GET'])
# @swag_from('../docs/reembolso/get_reembolso_por_get_reembolso_por_num_prestacao.yml')
def visualizar_reembolso(num_prestacao):
    try:
        reembolso = Reembolso.query.filter_by(num_prestacao=num_prestacao).first()
        if not reembolso:
            return jsonify({'error': 'Reembolso não encontrado'}), 404

        return jsonify({
            'id': reembolso.id,
            'colaborador': reembolso.colaborador,
            'empresa': reembolso.empresa,
            'num_prestacao': reembolso.num_prestacao,
            'descricao': reembolso.descricao,
            'data': reembolso.data.strftime('%Y-%m-%d'),
            'tipo_reembolso': reembolso.tipo_reembolso,
            'centro_custo': reembolso.centro_custo,
            'ordem_interna': reembolso.ordem_interna,
            'divisao': reembolso.divisao,
            'pep': reembolso.pep,
            'moeda': reembolso.moeda,
            'distancia_km': reembolso.distancia_km,
            'valor_km': reembolso.valor_km,
            'valor_faturado': reembolso.valor_faturado,
            'despesa': reembolso.despesa,
            'id_colaborador': reembolso.id_colaborador,
            'status': reembolso.status
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# # Listar todos os reembolsos
@bp_reembolso.route('/pegar-todos-reembolsos', methods=['GET'])
# @swag_from('../docs/reembolso/get_todos_reembolsos.yml')
def listar_todos_reembolsos():
    reembolsos = Reembolso.query.all()
    resultado = []
    for r in reembolsos:
        resultado.append({
            'id': r.id,
            'colaborador': r.colaborador,
            'empresa': r.empresa,
            'num_prestacao': r.num_prestacao,
            'descricao': r.descricao,
            'data': r.data.isoformat(),
            'tipo_reembolso': r.tipo_reembolso,
            'centro_custo': r.centro_custo,
            'ordem_interna': r.ordem_interna,
            'divisao': r.divisao,
            'pep': r.pep,
            'moeda': r.moeda,
            'distancia_km': r.distancia_km,
            'valor_km': str(r.valor_km) if r.valor_km else None,
            'valor_faturado': str(r.valor_faturado),
            'despesa': str(r.despesa) if r.despesa else None,
            'id_colaborador': r.id_colaborador,
            'status': r.status
        })
    return jsonify(resultado), 200

@bp_reembolso.route('/reembolsos', methods=['GET'])
# @swag_from('../docs/reembolso/get_reembolsos_colaborador.yml')    
def listar_reembolsos():
    colaborador_id = session.get('colaborador_id')
    print("Colaborador ID da sessão:", colaborador_id) 
    if not colaborador_id:
        return jsonify({'mensagem': 'Colaborador não logado'}), 401
    
    # Agora, busque os reembolsos do colaborador logado
    reembolsos = Reembolso.query.filter_by(id_colaborador=colaborador_id).all()
    print("Reembolsos encontrados:", reembolsos)
    if not reembolsos:
        return jsonify([]), 200  # Retorna um array vazio se não houver reembolsos
    
    resultado = []
    for r in reembolsos:
        resultado.append({
            'id': r.id,
            'colaborador': r.colaborador,
            'empresa': r.empresa,
            'num_prestacao': r.num_prestacao,
            'descricao': r.descricao,
            'data': r.data.isoformat(),
            'tipo_reembolso': r.tipo_reembolso,
            'centro_custo': r.centro_custo,
            'ordem_interna': r.ordem_interna,
            'divisao': r.divisao,
            'pep': r.pep,
            'moeda': r.moeda,
            'distancia_km': r.distancia_km,
            'valor_km': str(r.valor_km) if r.valor_km else None,
            'valor_faturado': str(r.valor_faturado),
            'despesa': str(r.despesa) if r.despesa else None,
            'id_colaborador': r.id_colaborador,
            'status': r.status
        })
    return jsonify(resultado), 200

# Buscar um reembolso por ID
@bp_reembolso.route('/reembolsos/<int:id>', methods=['GET'])
def obter_reembolso(id):
    reembolso = Reembolso.query.get(id)
    if not reembolso:
        return jsonify({'message': 'Reembolso não encontrado'}), 404

    return jsonify({
        'id': reembolso.id,
        'colaborador': reembolso.colaborador,
        'empresa': reembolso.empresa,
        'num_prestacao': reembolso.num_prestacao,
        'descricao': reembolso.descricao,
        'data': reembolso.data.isoformat(),
        'tipo_reembolso': reembolso.tipo_reembolso,
        'centro_custo': reembolso.centro_custo,
        'ordem_interna': reembolso.ordem_interna,
        'divisao': reembolso.divisao,
        'pep': reembolso.pep,
        'moeda': reembolso.moeda,
        'distancia_km': reembolso.distancia_km,
        'valor_km': str(reembolso.valor_km) if reembolso.valor_km else None,
        'valor_faturado': str(reembolso.valor_faturado),
        'despesa': str(reembolso.despesa) if reembolso.despesa else None,
        'id_colaborador': reembolso.id_colaborador,
        'status': reembolso.status
    }), 200

# Atualizar status de um reembolso
@bp_reembolso.route('/reembolsos/<int:id>', methods=['PUT'])
# @swag_from('../docs/reembolso/put_atualizar_status.yml')
def atualizar_status(id):
    reembolso = Reembolso.query.get(id)
    if not reembolso:
        return jsonify({'message': 'Reembolso não encontrado'}), 404

    data = request.json
    reembolso.status = data.get('status', reembolso.status)

    try:
        db.session.commit()
        return jsonify({'message': 'Status atualizado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp_reembolso.route('/reembolsos', methods=['DELETE'])
# @swag_from('../docs/reembolso/delete_reembolso_colaborador.yml')   
def deletar_reembolso_do_colaborador():
    if 'colaborador_id' not in session:
        return jsonify({'message': 'Login necessário para deletar reembolso'}), 401

    dados = request.get_json()
    id_reembolso = dados.get('id')

    if not id_reembolso:
        return jsonify({'message': 'ID do reembolso é obrigatório'}), 400

    reembolso = Reembolso.query.filter_by(id=id_reembolso, id_colaborador=session['colaborador_id']).first()

    if not reembolso:
        return jsonify({'message': 'Reembolso não encontrado ou não pertence ao usuário logado'}), 404

    try:
        db.session.delete(reembolso)
        db.session.commit()
        return jsonify({'message': 'Reembolso deletado com sucesso'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    
#Resumo de todos os reebolsos
@bp_reembolso.route('/reembolsos/resumo', methods=['GET'])
def resumo_reembolsos():
    try:
        total_solicitados = db.session.query(Reembolso).count()

        aprovados = db.session.query(Reembolso).filter(Reembolso.status == 'Aprovado').count()
        rejeitados = db.session.query(Reembolso).filter(Reembolso.status == 'Rejeitado').count()

        # Tudo que **não é Aprovado nem Rejeitado** será tratado como "Em análise"
        em_analise = db.session.query(Reembolso).filter(
            ~Reembolso.status.in_(['Aprovado', 'Rejeitado'])
        ).count()

        return jsonify({
            'total_solicitados': total_solicitados,
            'em_analise': em_analise,
            'aprovados': aprovados,
            'rejeitados': rejeitados
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@bp_reembolso.route('/reembolsos/resumo/unico', methods=['GET'])
def resumo_unico_reembolsos():
    try:
        id_colaborador = session.get('colaborador_id')

        if not id_colaborador:
            return jsonify({'error': 'Usuário não autenticado'}), 401

        total_solicitados = db.session.query(Reembolso).filter_by(id_colaborador=id_colaborador).count()

        aprovados = db.session.query(Reembolso).filter_by(id_colaborador=id_colaborador, status='Aprovado').count()

        rejeitados = db.session.query(Reembolso).filter_by(id_colaborador=id_colaborador, status='Rejeitado').count()

        em_analise = db.session.query(Reembolso).filter(
            Reembolso.id_colaborador == id_colaborador,
            ~Reembolso.status.in_(['Aprovado', 'Rejeitado'])
        ).count()

        return jsonify({
            'total_solicitados': total_solicitados,
            'em_analise': em_analise,
            'aprovados': aprovados,
            'rejeitados': rejeitados
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
