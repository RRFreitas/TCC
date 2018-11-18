from server.common.database import db
from flask_restful import fields

encoding_fields = {
    'pessoa_id': fields.Integer,
    'medidas': fields.List
}


class Encoding(db.Model):
    __tablename__ = 'encodings'

    medidas = db.Column('medidas', db.ARRAY(db.Integer, 128))

    pessoa_id = db.Column('pessoa_id', db.ForeignKey("pessoas.id"))

    pessoa = db.relationship("Pessoa")

    def __init__(self, pessoa_id, medidas):
        self.pessoa_id = pessoa_id
        self.medidas = medidas

    def __repr__(self):
        return "<Encoding [pessoa_id = %s, medidas = %s]>" % (self.pessoa_id, self.medidas)