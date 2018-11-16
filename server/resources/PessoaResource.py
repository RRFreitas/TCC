from flask_restful import Resource, marshal_with, reqparse, request, abort
from server.models.Pessoa import Pessoa, pessoa_fields
from server.common.database import db
from server.common.encodings import handler

class PessoaResource(Resource):
    # GET /pessoas
    # GET /pessoas/<pessoa_id>
    @marshal_with(pessoa_fields)
    def get(self, pessoa_id=None):
        if pessoa_id is None:
            return Pessoa.query.all()
        else:
            return Pessoa.query.filter_by(id=pessoa_id)

    # POST /pessoas
    def post(self):
        try:
            json_data = request.get_json(force=True)

            pessoa = Pessoa(json_data['nome'], json_data['email'])
            db.session.add(pessoa)
            db.session.commit()

            print(pessoa)

            return 200
        except Exception as err:
            return err