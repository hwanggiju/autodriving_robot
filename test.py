import serial


port = '/dev/ttyACM0'
brate = 9600
ser = serial.Serial(port, brate, timeout=None)
while True :
    ch = input()
    
    if ch == 'g' :
        print(type(ch))
        ser.write(ch.encode())
        
    if ch == 's' :
        ser.write(ch.encode())  