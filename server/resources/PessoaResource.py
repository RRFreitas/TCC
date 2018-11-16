from flask_restful import Resource, marshal_with, reqparse, request, abort
from flask import Response
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
            return Pessoa.query.filter_by(id=pessoa_id).first()

    # POST /pessoas
    def post(self):
        try:
            json_data = request.get_json(force=True)
            if(not('nome' in json_data.keys() and 'email' in json_data.keys()
                   and 'encoding' in json_data.keys())):
                raise Exception("Má formatação.")

            pessoa = Pessoa(json_data['nome'], json_data['email'])
            db.session.add(pessoa)
            db.session.commit()

            handler.adicionarEncoding(pessoa.id, json_data['encoding'])

            return Response('OK', 200)
        except Exception as err:
            return Response(str(err), 400)

    # DELETE /pessoas/<pessoa_id>
    def delete(self, pessoa_id):
        try:
            pessoa = Pessoa.query.filter_by(id=pessoa_id).first()

            if pessoa is None:
                return Response("Pessoa não encontrada.", 404)

            db.session.delete(pessoa)
            db.session.commit()
            return Response("OK", 200)
        except Exception as err:
            return Response(str(err), 500)