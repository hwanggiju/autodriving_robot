import cv2

cap = cv2.VideoCapture(0)

if cap.isOpened():
    print("camera is Opened")
    delay = int(1000 / cap.get(cv2.CAP_PROP_FPS)) 
    while True:
        ret, img = cap.read()
        if ret:
            img = cv2.flip(img, 1)
            cv2.imshow('Camera', img)
            if cv2.waitKey(delay) & 0xFF == 27:
                print('exit')
                break
        else:
            print(ret, img)
            break
else:
    print('Camera not opened')

cap.release()
cv2.destroyAllWindows()


