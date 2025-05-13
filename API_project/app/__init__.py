# pip install Flask-Migrate
# toda vez que altera a classe do Cliente, aciona o Migrate (p/ ñ dar erro)

from flask import Flask, jsonify
from flask_migrate import Migrate
from config import Config
from app.db import db
from app.auth import token_required, auth_bp

# usar para fazer alteracoes no DB e validar
migrate = Migrate()

# importar todas as configuracoes que estao no config
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # faz uma chave so pra aplicacao, q eh a principal. o das rotas cria pra so mudar quem eh dev
    app.config['SECRET_KEY'] = 'your-secret-key'

    db.init_app(app)
    # faz migracao dos dados
    migrate.init_app(app, db)

    # cada rota tem o seu routes_bp, importa isso e registra.
    from app.routes import bp as routes_bp
    # registra bp que tem as rotas do Client
    app.register_blueprint(routes_bp)

    # registra rotas de autenticacao com prefixo /auth
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # TRATAR ERROS GLOBAIS

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'message': 'Bad Request'}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({'message': 'Unauthorized'}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'message': 'Not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': 'Internal Server Error'}), 500

    @app.errorhandler(503)
    def server_unavailable(error):
        return jsonify({'message': 'Server unavailable'}), 503

    return app

