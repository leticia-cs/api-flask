from flask import jsonify, request, abort
from app import db
from app.models import Client
from app.routes import bp
from app.auth import token_required


@bp.route('/clients', methods=['GET'])
@token_required
def get_clients(current_user):
    # recebe por json
    client_id = request.args.get('client_id')
    # verifica se recuperou (se existe, é 1
    if client_id:
        try:
            # se nao existe, retorna erro de not found
            client = Client.query.get_or_404(client_id)
            return jsonify(client.to_dict()), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 # cod erro interno

    # se nao tiver id, mostra todo mundo
    else:
        try:
            # retornar todos os clientes do DB
            clients = Client.query.all()
            # para cada uma das entradas, transforma em cliente
            return jsonify([client.to_dict() for client in clients]), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500 # cod erro interno

# criar cliente (POST pq n pode ver)
@bp.route('/clients', methods=['POST'])
@token_required
def create_client(current_user):
    try:
        data = request.get_json()
        # verificar erros e exceções
        if 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400 # bad request
        # pesquisa por xyz do cliente e recupera o primeiro registro
        if Client.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Name already registered'}), 400 # bad request
        if Client.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400 # bad request

        # cria obj
        client = Client(name=data['name'], email=data['email'])
        # add obj no DB
        db.session.add(client)
        # confirma alteracoes
        db.session.commit()
        return jsonify(client.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# rota para atualizar cliente - UPDATE
@bp.route('/clients/<int:id>', methods=['PUT'])
@token_required
def update_client(current_user, id):
    try:
        # recuperar cliente do banco
        client = Client.query.get_or_404(id)
        # recuperar dados enviados via json (
        data = request.get_json() or {}

        # ver se BD tem nome ou email (se preencheu todos os campos)
        if 'name' not in data or 'email' not in data:
            return jsonify({'error': 'Name and email are required'}), 400

        # verifica se nome esta no banco
        if Client.query.filter_by(name=data['name']).first():
            return jsonify({'error': 'Name already registered'}), 400
        # verifica se email esta no banco
        if Client.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400

        # atualiza cliente no BD
        client.name = data['name']
        client.email = data['email']
        db.session.commit()
        return jsonify(client.to_dict()), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500 # erro servidor
    
# rota para deletar cliente - DELETE
@bp.route('/clients/<int:id>', methods=['DELETE'])
@token_required
def delete_client(current_user, id):
    try:
        # recuperar cliente do banco
        client = Client.query.get_or_404(id)
        # deletar
        db.session.delete(client)
        # salvar
        db.session.commit()
        return jsonify({'message':'Successfully deleted client'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500 # erro servidor