#pip install flask
import secrets

from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

# pip install flask-sqlalchemy

app = Flask(__name__, template_folder='templates')
# configurando onde salva o Banco Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///teste.db'
#chave secreta para criptografar as sessões
secret_key = secrets.token_hex(32)
# configurar a chave no app
app.config['SECRET_KEY'] = secret_key
# ativa contexto do app (varias pessoas acessar o seu banco dados
app.app_context().push()
# cria banco dados (se nao existir)
db = SQLAlchemy(app)

# criando classe
class Estudante(db.Model):
    id = db.Column("student_id", db.Integer, primary_key=True)
    nome = db.Column(db.String(200))
    cidade = db.Column(db.String(100))
    email = db.Column(db.String(100))
    pin = db.Column(db.String(10))

    # inicializador/construtor do obj
    def __init__(self, nome, cidade, email, pin):
        self.nome = nome
        self.cidade = cidade
        self.email = email
        self.pin = pin

# criando classe
class Telefone(db.Model):
    id = db.Column("phone_id", db.Integer, primary_key=True)
    descricao = db.Column(db.String(20))
    numero = db.Column(db.String(15))
    estudante_id = db.Column(db.Integer, db.ForeignKey('estudante.student_id'))
    estudante = relationship('Estudante', backref='telefones')

    # inicializador/construtor do obj
    def __init__(self, descricao, numero, estudante):
        self.descricao = descricao
        self.numero = numero
        self.estudante = estudante

# rotas padrao (default)
@app.route('/')
def show_all():
    return render_template('show_all.html', estudantes=Estudante.query.all()) # linha estudante --> SELECT estudante * etc

# rota para novo registro
@app.route('/new', methods=['GET', 'POST'])
def new():
    # verifica se recebendo por POST
    if request.method == 'POST':
        # verifica se user preencheu campos
        if not request.form['nome'] or not request.form['cidade'] or not request.form['email'] or not request.form['pin']:
            flash("Preencha todos os campos", "Erro")
        else:
            estudante = Estudante(request.form['nome'], request.form['cidade'], request.form['email'], request.form['pin'])
            # colocar esse obj no BD. se der erro ele vai dar erro em tudo e vai parar
            db.session.add(estudante)
            # grava alteracoes no BD
            db.session.commit()
            # retorna msg de OK
            flash("Estudante " + estudante.nome + " foi add ao banco de dados")
            # chama funcao do show_all (aquela do @app.route)
            return redirect(url_for('show_all'))

    return render_template('new.html')

# rota para atualizar registro
@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    # pega estudante pelo id
    estudante = Estudante.query.get(id)

    #MESMO IF DO NEW()
    if request.method == 'POST':
        # verifica se user preencheu campos
        if not request.form['nome'] or not request.form['cidade'] or not request.form['email'] or not request.form['pin']:
            flash("Preencha todos os campos", "Erro")
        else:
            # coloca as coisas nos campos
            estudante.nome = request.form['nome']
            estudante.cidade = request.form['cidade']
            estudante.email = request.form['email']
            estudante.pin = request.form['pin']

            # colocar esse obj no BD. se der erro ele vai dar erro em tudo e vai parar
            db.session.add(estudante)
            # grava alteracoes no BD
            db.session.commit()
            # retorna msg de OK
            flash("Estudante " + estudante.nome + " foi updated ao banco de dados")
            # chama funcao do show_all (aquela do @app.route)
            return redirect(url_for('show_all'))

    return render_template('update.html', estudante=estudante)

# rota para deletar registro
@app.route('/delete/<int:id>', methods=['GET'])
def delete(id):
    # pega estudante pelo id
    estudante = Estudante.query.get(id)
    # deleta estudante do bd
    db.session.delete(estudante)
    # salva alteracoes no bd
    db.session.commit()
    # coloca msg
    flash("Estudante " + estudante.nome + " foi delete do bd.")

    return redirect(url_for('show_all'))

@app.route('/add/<int:id>')
def add(id):
    # pega estudante pelo id
    estudante = Estudante.query.get(id)
    # cria obj telefone c/ estudante
    telefone = Telefone("Smartphone", "+5547999990000", estudante)
    # add no bd
    db.session.add(telefone)
    # salva no bd
    db.session.commit()
    # avisa
    flash("estudante " + estudante.nome + " foi add to banco de dados")
    #mostra pag
    return redirect(url_for('show_all'))

@app.route('/filtrar/<string:cidade>')
def filtrar(cidade):
    # filtra por coluna "Cidade" que tenha "Jaragua" no bd original
    estudante_filtro = Estudante.query.filter_by(cidade=cidade).all()
    # igual return do show_all(), mostra so os filtrados.
    return render_template('show_all.html', estudante=estudante_filtro)

if __name__ == '__main__':
    # cria as tabelas
    db.create_all()
    # rodar o server
    app.run(debug=True, host='0.0.0.0', port=5000)

