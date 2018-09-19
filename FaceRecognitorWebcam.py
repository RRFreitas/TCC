#!/usr/bin/env python3

import numpy as np
import cv2
import os

from time import sleep

face_recognizer = cv2.face.LBPHFaceRecognizer_create()

subjects = ["", "Rennan", "Silvio", "Unknown"]

def detect_face(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier('haarcascades/haarcascade_frontalface_alt.xml')

    rects = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    faces = [gray[y:y+h, x:x+w] for (x, y, w, h) in rects]

    return faces, rects

def prepare_training_data(data_folder_path):
    # pega diretorios do diretorio de dados
    dirs = os.listdir(data_folder_path)

    # lista de todas as faces
    faces = []

    # lista de etiquetas
    labels = []

    # ler imagens de cada diretorio
    for dir_name in dirs:

        if not dir_name.startswith("s"):
            continue

        # extrair label do nome do diretorio
        label = int(dir_name.replace("s", ""))

        subject_dir_path = data_folder_path + "/" + dir_name

        subject_images_names = os.listdir(subject_dir_path)

        for image_name in subject_images_names:

            if(image_name.startswith('.')):
                continue

            # caminho da imagem
            image_path = subject_dir_path + "/" + image_name

            image = cv2.imread(image_path)

            cv2.imshow("Training on image...", image)
            cv2.waitKey(5)

            # detectar face
            faces_img, rects = detect_face(image)

            if(len(faces_img) > 0):
                face = faces_img[0]

                faces.append(face)
                labels.append(label)

            cv2.destroyAllWindows()

    return faces, labels

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(img):
    faces, rects = detect_face(img)

    for (face, rect) in zip(faces, rects):

        label, percent = face_recognizer.predict(face)
        print(label, percent)

        label_text = subjects[label]

        draw_rectangle(img, rect)
        draw_text(img, label_text, rect[0], rect[1]-5)

    return img

def main():
    print("Preparing data...")
    faces, labels = prepare_training_data("train")
    print("Data prepared")

    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))

    face_recognizer.train(faces, np.array(labels))

    cap = cv2.VideoCapture(0)

    while (True):

        ret, frame = cap.read()

        frame = predict(frame)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
