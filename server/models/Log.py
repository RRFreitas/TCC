from server.common.database import db
from flask_restful import fields

log_fields = {
    'pessoa_id': fields.Integer,
    'data_hora': fields.DateTime
}


class Log(db.Model):
    __tablename__ = 'logs'

    data_hora = db.Column('data_hora', db.Date)

    pessoa_id = db.Column('pessoa_id', db.ForeignKey("pessoas.id"))

    pessoa = db.relationship("Pessoa")

    def __init__(self, pessoa_id, data_hora):
        self.pessoa_id = pessoa_id
        self.data_hora = data_hora

    def __repr__(self):
        return "<Log [pessoa_id = %s, data_hora = %s]>" % (self.pessoa_id, self.data_hora)