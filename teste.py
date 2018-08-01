from PIL import Image
import face_recognition

minha_foto = face_recognition.load_image_file("eu.jpg")
minha_face = face_recognition.face_encodings(minha_foto)[0]

turma_foto = face_recognition.load_image_file("turma.jpg")
turma_faces = face_recognition.face_encodings(turma_foto)

face_locations = face_recognition.face_locations(turma_foto)

for index, face in enumerate(turma_faces):
	results = face_recognition.compare_faces([minha_face], face)
	if(results[0] == True):
		print("hello its me")

		top, right, bottom, left = face_locations[index]
		face_img = turma_foto[top:bottom, left:right]
		pil_image = Image.fromarray(face_img)
		pil_image.show()
		

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
