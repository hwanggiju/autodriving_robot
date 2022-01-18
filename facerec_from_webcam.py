import face_recognition
import cv2
import numpy as np
import gc
cap = cv2.VideoCapture(0)

obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

biden_image = face_recognition.load_image_file("biden.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

giju_image = face_recognition.load_image_file("giju_image.jpg")
giju_face_encoding = face_recognition.face_encodings(giju_image)[0]

known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    giju_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Biden",
    "giju"
]

if cap.isOpened():
    print("Camera is opened")
    delay = int(1000 / cap.get(cv2.CAP_PROP_FPS)) 
    while True:
        ret, frame = cap.read()
        rgb_frame = frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):

            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"
            
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]
            print(name)

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        if cv2.waitKey(delay) & 0xFF == 27:
            break
        cv2.imshow("Video", frame)

gc.collect(generation=2)
cap.release()
cv2.destroyAllWindows()
