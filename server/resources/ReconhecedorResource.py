from flask_restful import Resource, marshal_with, request
from flask import Response
from server.models.Pessoa import Pessoa, pessoa_fields
from server.models.Encoding import Encoding
from server.common.encodings import handler
import face_recognition
import numpy as np
import base64


class ReconhecedorResource(Resource):

    # POST /reconhecer
    @marshal_with(pessoa_fields)
    def post(self):
        try:
            json_data = request.get_json(force=True)
            if not 'foto_b64' in json_data.keys():
                raise Exception("Má formatação.")

            print(json_data['foto_b64'])
            s = json_data['foto_b64']
            imgdata = base64.b64decode(s + '=' * (-len(s) % 4))
            file_name = 'face.jpg'
            with open(file_name, 'wb') as f:
                f.write(imgdata)
            print(file_name)
            img_file = face_recognition.load_image_file(file_name)
            encodings = face_recognition.face_encodings(img_file)
            print("file " + encodings[0])

            if (len(encodings) != 1):
                raise Exception("Nenhuma ou mais de uma face.")

            knownEncodings = np.asarray(Encoding.query.all())
            print("known " + knownEncodings)
            matches = face_recognition.compare_faces(knownEncodings, encodings[0])
            print(matches)
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

            print(p)

            if p:
                return p
            else:
                return Pessoa(nome, email, id=id)
        except Exception as err:
            print(err)
            return Pessoa("Desconhecido", "")