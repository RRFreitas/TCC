from server.common.database import db
from flask_restful import fields

pessoa_fields = {
    'id': fields.Integer,
    'nome': fields.String,
    'email': fields.String
}

class Pessoa(db.Model):
    __tablename__ = 'pessoas'

    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column('nome', db.String(50))
    email = db.Column('email', db.String(50))

    def __init__(self, nome, email):
        self.nome = nome
        self.email = email

    def __repr__(self):
        return "<Pessoa [id = %s, nome = %s, email = %s]>" % (self.id, self.nome, self.email)