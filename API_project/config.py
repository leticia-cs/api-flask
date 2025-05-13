# colocar o sistema operacional
import os

# criando um caminho relativo pra aplicacao (caminho relativo = onde vc iniciou a aplicacao)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # nao e legal ter chave salva no app, entao procura a chave.
    SECRET_KEY = os.environ.get("SECRET_KEY") or 'you-will-never-guess'
    # caminho do banco
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")
    # ativa para registrar alteracoes no banco. por enquanto, deixa off.
    SQLALCHEMY_TRACK_MODIFICATIONS = False