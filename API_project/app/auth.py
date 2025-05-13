# autenticacao

import datetime
import jwt

from functools import wraps
from flask import request, jsonify, Blueprint, current_app

auth_bp = Blueprint('auth', __name__)

# criando rota de login
@auth_bp.route('/login', methods=['POST'])
def login():
    # toda vez que alguem mandar um login, recupera os dados do json. se nao tiver, vai dar erro.
    auth_data = request.get_json()
    # dos dados de autenticacao, pegue o campo xyz
    username = auth_data.get('username')
    password = auth_data.get('password')

    # verifica se tem credencial valida
    if username == "admin" and password == "password":
        # se entrou como adm (autenticado), cria token
        token = jwt.encode(
            {
                'user': username,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=10),
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

        #caso de certo, converte o token para um json e devolve ao cliente
        return jsonify({'token': token}), 200 # codigo de OK
    return jsonify({'message': 'Invalid username or password'}), 401 # codigo de erro autenticacao

# funcao para controlar token
def token_required(f):
    @wraps(f) #transforma em notacao
    def decorated(*args, **kwargs):
        token = None # inicializa token como vazio
        # recupera token, verifica se existe no cabecalho da requisicao
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            # tenta decodificar os dados usando o token na chave
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['user']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token is expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token is invalid'}), 401

        return f(current_user, *args, **kwargs)

    return decorated