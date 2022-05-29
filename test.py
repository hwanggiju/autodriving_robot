import serial

ch = input()

port = '/dev/ttyACM0'
brate = 9600
ser = serial.Serial(port, brate, timeout=None)
while True :
    if ch == 'g' :
        ser.write(ch.encode())
        
    if ch == 's' :
        ser.write(ch.encode())  