import serial


port = '/dev/ttyACM0'
brate = 9600
ser = serial.Serial(port, brate, timeout=None)
while True :
    ch = input()
    
    if ch == 1 :
        print(type(ch))
        ser.write(ch.encode())
        
    if ch == 2 :
        ser.write(ch.encode())  