import serial


port = '/dev/ttyACM0'
brate = 9600
ser = serial.Serial(port, brate, timeout=None)
while True :
    ch = input()
    if ch == 's' :
        ser.write(ch.encode())
        data = ser.readline()
        data = data.decode()[:len(data)-2]
        print(len(data))
        print(data)
        
    if ch == 'f' :
        ser.write(ch.encode())  
        data = ser.readline()
        data = data.decode()[:len(data)-2]
        print(len(data))
        print(data)