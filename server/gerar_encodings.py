#!/usr/bin/env python3

from imutils import paths
import os
import cv2
import face_recognition
import pickle

def gerar(path, encodings_file):
	imagePaths = list(paths.list_images("dataset/"))

	knownEncodings = []
	knownNames = []

	for(i, imagePath) in enumerate(imagePaths):
		print("[INFO] processando imagem {}/{}".format(i + 1, len(imagePaths)))

		name = imagePath.split(os.path.sep)[-2]

		print(name)

		image = cv2.imread(imagePath)
		rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

		boxes = face_recognition.face_locations(rgb)

		encodings = face_recognition.face_encodings(rgb, boxes)

		for encoding in encodings:
			knownEncodings.append(list(encoding))
			knownNames.append(name)

	print("[INFO] serializando encodings...")
	data = {"encodings": knownEncodings, "names": knownNames}
	f = open(encodings_file, "wb")
	f.write(pickle.dumps(data))
	f.close()

if __name__ == '__main__':
	gerar("dataset/", "encodings.pickle")