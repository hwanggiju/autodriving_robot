import face_recognition
import cv2
import numpy as np

cap = cv2.VideoCapture(0)
output = np.empty((240, 320, 3), dtype=np.uint8)

print("Loading known face image(s)")
obama_image = face_recognition.load_image_file("obama_small.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

giju_image = face_recognition.load_image_file("giju_image.jpg")
giju_face_encoding = face_recognition.face_encodings(giju_image)[0]

face_locations = []
face_encodings = []

while True:
    print("Capturing image.")
    ret, img = cap.read()
    cv2.capture(output, format="rgb")
    face_locations = face_recognition.face_locations(output)
    print("Found {} faces in image.".format(len(face_locations)))
    face_encodings = face_recognition.face_encodings(output, face_locations)

    for face_encoding in face_encodings:
        match = face_recognition.compare_faces([obama_face_encoding, giju_face_encoding], face_encoding)
        name = "<Unknown Person>"

        if match[0]:
            name = "Barack Obama"

        print("{}!".format(name))
