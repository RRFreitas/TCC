from flask_restful import Resource, marshal_with, request
from flask import Response
from server.models.Pessoa import Pessoa, pessoa_fields
from server.common.encodings import handler
import face_recognition

class ReconhecedorResource(Resource):

    # POST /reconhecer
    @marshal_with(pessoa_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            if not 'encoding' in json_data.keys():
                raise Exception("Má formatação.")

            matches = face_recognition.compare_faces(handler.encodings['encodings'],
                                                     json_data['encoding'])
            nome = "Desconhecido"
            email = ""
            id = 0

            if True in matches:
                # encontra os índices de todas as faces que deram match
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}

                for i in matchedIdxs:
                    id = handler.encodings["ids"][i]
                    counts[id] = counts.get(id, 0) + 1

                # determina a face reconhecida com o maior número de votos
                id = max(counts, key=counts.get)

            p = Pessoa.query.filter_by(id=id).first()

            if p:
                return p
            else:
                return Pessoa(nome, email, id=id)
        except Exception as err:
            return Response(str(err), 400)