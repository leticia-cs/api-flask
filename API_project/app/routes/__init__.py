from flask import Blueprint

# bp pega a funcao do main de iniciar o servidor flask
bp = Blueprint('main', __name__)

# importa e encapsula as rotas no init usando o blueprint.
from app.routes import clients