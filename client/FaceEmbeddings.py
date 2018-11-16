#!/usr/bin/env python3

from PIL import Image, ImageDraw, ImageFont
import face_recognition
import os

def detect_face(img):

    # medidas de todas as faces encontradas
    faces_encode = face_recognition.face_encodings(img)
    # localização de todas as faces encontradas (x,y,w,h)
    faces_locations = face_recognition.face_locations(img)

    #faces = [img[y:y+h, x:x+w] for (x, y, w h) in face_locations]

    return faces_encode, faces_locations

def prepare_training_data(data_folder_path):
    # lista com nome das imagens no diretório
    subject_images_names = os.listdir(data_folder_path)

    # lista de encodings das faces
    encodings = []

    # lista de posições das faces
    locations = []

    # lista de nomes
    names = []

    # percorre lista de imagens
    for image_name in subject_images_names:
        if(image_name.startswith('.')): # se for arquivo do sistema, pular
            continue

		# caminho da imagem
        image_path = data_folder_path + "/" + image_name

        # leitura da imagem passado o caminho por parâmetro
        image = face_recognition.load_image_file(image_path)

        # medidas e localizações de todas as faces encontradas na imagem
        faces_encodes, faces_locations = detect_face(image)

        print("Training image: " + image_name)

        if(len(faces_encodes) > 0):
            if(len(faces_encodes) > 1):
                print("[WARN] Imagem %s contém mais de uma face!" % image_name)

            # É esperado que nas imagens só tenham uma face, logo face de index 0
            face_encode = faces_encodes[0]
            # Adicionar medidas da face na lista
            encodings.append(face_encode)
            # Adicionar nome do indivíduo na lista de nomes, baseado no nome do arquivo
            names.append(image_name.split('.')[0])

    return encodings, names

def recognize(known_encodings, nomes, image):
    # font pillow
    fnt = ImageFont.truetype('FreeSansBold.ttf', 18)

    # Pega o encoding de todas as faces da foto
    faces_encodings = face_recognition.face_encodings(image)
    # Pega as localizações das faces na foto (top, right, bottom, left)
    face_locations = face_recognition.face_locations(image)

    pil_image = Image.fromarray(image)
    draw = ImageDraw.Draw(pil_image)

    # Percorre cada face da foto
    for index, face_encoding in enumerate(faces_encodings):
        # Compara a face 1:1
        results = face_recognition.compare_faces(known_encodings, face_encoding)

        # lista de nomes das pessoas reconhecidas
        recognizeds = [nomes[i] for i, known in enumerate(results) if known]
        print(recognizeds)

        for name in recognizeds:
            top, right, bottom, left = face_locations[index]  # locations da face

            # Desenha retângulo nos locations da face
            draw.rectangle(((left, top), (right, bottom)), outline=(0, 255, 0))
            draw.text((left, top - 20), name, (0, 255, 0), fnt)

    return pil_image

def main():
    print("Preparing data...")

    # Diretório com imagens pessoas conhecidas para treinar o algoritmo
    training_data_dir = "dataset"
    # Diretório com imagens de testes para reconhecimento de faces conhecidas
    image_test_dir = "examples"

    # Medidas da face e nome das pessoas registradas (no diretório passado por parâmetro)
    encodings, names = prepare_training_data(training_data_dir)

    # Lista de nomes de imagens no diretório de teste
    pics = os.listdir(image_test_dir)

    # Percorrer lista de imagens de teste
    for pic in pics:
        # Carrega foto
        image_array = face_recognition.load_image_file(image_test_dir + "/" + pic)

        # Reconhece e desenha as faces na foto
        pil_image = recognize(encodings, names, image_array)
        # Mostra foto
        pil_image.show()

if __name__ == '__main__':
	main()
