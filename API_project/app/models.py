from app import db

# criando primeira classe do BD
class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True)

    # criar funcao para transformar obj em dicionario (tem lugar que pede)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }