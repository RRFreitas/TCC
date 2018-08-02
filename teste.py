from PIL import Image, ImageDraw
import face_recognition

# Carrega foto eu.jpg
minha_foto = face_recognition.load_image_file("eu.jpg")
# Encoding da foto eu.jpg
minha_face = face_recognition.face_encodings(minha_foto)[0]

# Lista de fotos com várias pessoas para encontrar a face da foto eu.jpg
fotos = ["1.jpg", "2.jpg", "3.jpg"]

# Percorre cada foto do array fotos
for foto in fotos:
	# Carrega foto
	turma_foto = face_recognition.load_image_file(foto)
	# Pega o encoding de todas as faces da foto
	turma_faces = face_recognition.face_encodings(turma_foto)
	# Pega as localizações das faces na foto (top, right, bottom, left)
	face_locations = face_recognition.face_locations(turma_foto)

	# Percorre cada face da foto
	for index, face in enumerate(turma_faces):
		# Compara face eu.jpg com a face atual (true ou false)
		results = face_recognition.compare_faces([minha_face], face)

		if(results[0] == True): # Se for parecido
			print("its me")

			top, right, bottom, left = face_locations[index] # locations da face

			pil_image = Image.fromarray(turma_foto) 
			draw = ImageDraw.Draw(pil_image)
			#Desenha retângulo nos locations da face
			draw.rectangle(((left, top), (right, bottom)), outline="red")
			pil_image.show()

			
			#face_img = turma_foto[top:bottom, left:right]
			#pil_image2 = Image.fromarray(face_img)
			#pil_image2.show()
		

"""
faces_turma = face_recognition.face_locations(turma_foto)

print("I found {} face(s) in this photograph.".format(len(face_locations)))

for face_location in face_locations:

	# Print the location of each face in this image
	top, right, bottom, left = face_location
	print("A face is located at pixel location Top: {}, Left: {}, Bottom: {}, Right: {}".format(top, left, bottom, right))

	# You can access the actual face itself like this:
	face_image = image[top:bottom, left:right]
	pil_image = Image.fromarray(face_image)
	pil_image.show()"""
