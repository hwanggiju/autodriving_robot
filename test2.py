import cv2

cap = cv2.VideoCapture(0)

while True :
    _, frame = cap.read()
    
    cv2.imshow('test', frame)
    
    if cv2.waitKey() & 0xFF == 27 :
        break
    
cap.release()
cv2.destroyAllWindows()