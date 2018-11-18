from flask_restful import Resource, marshal_with, reqparse, request, abort
from flask import Response
from server.models.Pessoa import Pessoa, pessoa_fields
from server.models.Encoding import Encoding
from server.common.database import db
import base64
import face_recognition

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
                   and 'foto_b64' in json_data.keys())):
                raise Exception("Má formatação.")

            imgdata = base64.decodebytes(json_data['foto_b64'])
            encodings = face_recognition.face_encodings(imgdata)

            if(len(encodings) != 1):
                raise Exception("Nenhuma ou mais de uma face.")

            pessoa = Pessoa(json_data['nome'], json_data['email'])
            db.session.add(pessoa)
            db.session.commit()

            encoding = Encoding(pessoa.id, encodings[0])
            db.session.add(encoding)
            db.session.commit()

            return Response('OK', 200)
        except Exception as err:
            return Response(str(err), 400)

    # DELETE /pessoas/<pessoa_id>
    def delete(self, pessoa_id=None):
        try:
            if pessoa_id is None:
                all = Pessoa.query.all()
                for pessoa in all:
                    encs = Encoding.query.filter_by(pessoa_id=pessoa.id).all()
                    for enc in encs:
                        db.session.delete(enc)
                    db.session.delete(pessoa)
                db.session.commit()
                return Response("OK", 200)

            pessoa = Pessoa.query.filter_by(id=pessoa_id).first()

            if pessoa is None:
                return Response("Pessoa não encontrada.", 404)

            encs = Encoding.query.filter_by(pessoa_id=pessoa.id).all()
            for enc in encs:
                db.session.delete(enc)

            db.session.delete(pessoa)
            db.session.commit()
            return Response("OK", 200)
        except Exception as err:
            return Response(str(err), 500)