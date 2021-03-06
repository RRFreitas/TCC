from flask_restful import Resource, marshal_with, request
from models.Pessoa import Pessoa, pessoa_fields
from models.Encoding import Encoding
import face_recognition


class ReconhecedorResource(Resource):

	# POST /reconhecer
	@marshal_with(pessoa_fields)
	def post(self):
		try:
			if not ('foto' in request.files):
				raise Exception("Foto inválida.")

			file = request.files['foto']

			image = face_recognition.load_image_file(file)
			encodings = face_recognition.face_encodings(image)

			if (len(encodings) != 1):
				raise Exception("Nenhuma ou mais de uma face.")

			knownEncodingsQuery = Encoding.query.all()

			knownEncodings = [list(enc.medidas) for enc in knownEncodingsQuery]

			matches = face_recognition.compare_faces(knownEncodings, encodings[0])
			nome = "Desconhecido"
			email = ""
			id = 0

			if True in matches:
				# encontra os índices de todas as faces que deram match
				matchedIdxs = [i for (i, b) in enumerate(matches) if b]
				counts = {}

				for i in matchedIdxs:
					id = knownEncodingsQuery[i].pessoa_id
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