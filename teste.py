#!/usr/bin/env python3

from PIL import Image, ImageDraw
import face_recognition
import os

"""# Carrega foto eu.jpg
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
			#pil_image2.show()"""
		
def detect_face(img):
	faces_encode = face_recognition.face_encodings(img)
	faces_locations = face_recognition.face_locations(img)

	#faces = [img[y:y+h, x:x+w] for (x, y, w h) in face_locations]

	return faces_encode, faces_locations

def prepare_training_data(data_folder_path):
	# pega as imagens no diretório
	subject_images_names = os.listdir(data_folder_path)

	# lista de encodings das faces
	encodings = []

	# lista de posições das faces
	locations = []

	# lista de nomes
	nomes = []

	for image_name in subject_images_names:
		if(image_name.startswith('.')):
			continue

		# caminho da imagem	
		image_path = data_folder_path + "/" + image_name

		image = face_recognition.load_image_file(image_path)	
		
		faces_encodes, faces_locations = detect_face(image)

		print("Training image: " + image_name)

		if(len(faces_encodes) > 0):
			# É esperado que nas imagens só tenham uma face, logo face de index 0
			face_encode = faces_encodes[0]
			encodings.append(face_encode)
			nomes.append(image_name.split('.')[0])

	return encodings, nomes

def main():
	print("Preparing data...")

	encodings, nomes = prepare_training_data("known_people")

	print(encodings)

	fotos = ["3people.jpeg"]

	for foto in fotos:
		#Carrega foto
		turma_foto = face_recognition.load_image_file(foto)
		# Pega o encoding de todas as faces da foto
		turma_faces = face_recognition.face_encodings(turma_foto)
		# Pega as localizações das faces na foto (top, right, bottom, left)
		face_locations = face_recognition.face_locations(turma_foto)

		# Percorre cada face da foto
		for index, face in enumerate(turma_faces):
			# Compara face eu.jpg com a face atual (true ou false)
			results = face_recognition.compare_faces([encodings[0]], face)
				
			print(results)			
			
			if(results[0] == True): # Se for parecido

				top, right, bottom, left = face_locations[index] # locations da face

				pil_image = Image.fromarray(turma_foto) 
				draw = ImageDraw.Draw(pil_image)
				#Desenha retângulo nos locations da face
				draw.rectangle(((left, top), (right, bottom)), outline="red")
				pil_image.show()

	

if __name__ == '__main__':
	main()
