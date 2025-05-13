from app import create_app, db
from app.models import Client

# criar instancia do app flask
app = create_app()

# qnd iniciar a aplicacao, da pra usar cmd shell pra acessar os dados da aplicacao
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Client': Client}