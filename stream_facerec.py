import cv2
import numpy as np
import face_recognition
import keyboard

cap = cv2.VideoCapture(0)

def streaming_mode():
    print("camera is Opened")
    delay = int(1000 / cap.get(cv2.CAP_PROP_FPS)) 
    while True:
        ret, img = cap.read()
        if ret:
            cv2.imshow('Camera', img)
            if cv2.waitKey(delay) & 0xFF == 27:
                print("Good Bye~!!\nNext Command Input")
                break
            if keyboard.is_pressed('f7'):
                cv2.destroyAllWindows()
                face_rec_mode()
        else:
            print(ret, img)
            break
        
    cv2.destroyAllWindows()
    
def face_rec_mode():    
    obama_image = face_recognition.load_image_file("obama_small.jpg")
    obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

    biden_image = face_recognition.load_image_file("biden.jpg")
    biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

    giju_image = face_recognition.load_image_file("giju_small_image.jpg")
    giju_face_encoding = face_recognition.face_encodings(giju_image)[0]

    known_face_encodings = [
        obama_face_encoding,
        biden_face_encoding,
        giju_face_encoding
    ]
    known_face_names = [
        "Barack Obama",
        "Joe Biden",
        "giju"
    ]

    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True

    if cap.isOpened():
        print("camera open")
        while True:
            ret, frame = cap.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            rgb_small_frame = small_frame[:, :, ::-1]

            if process_this_frame:
                face_locations = face_recognition.face_locations(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                    
                    name = "Unknown"
                    
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    print("{}".format(name))
                    
                    face_names.append(name)

            process_this_frame = not process_this_frame

            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

            cv2.imshow('Video', frame)

            if cv2.waitKey(1) & 0xFF == 27:
                print("Good Bye~!!\nNext Command Input")
                break
    cv2.destroyAllWindows()

print("Key Input")

while True :
    if keyboard.is_pressed('f2'):
        streaming_mode()

    if keyboard.is_pressed('f3'):
        face_rec_mode()

    if keyboard.is_pressed('f4'):
        print("See You Later~~")
        break
    
cap.release()
cv2.destroyAllWindows()
    