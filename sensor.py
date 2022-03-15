import serial

port = '/dev/ttyACM0'
brate = 9600

ser = serial.Serial(port, brate, timeout=None)

while True :
    try :
        data = ser.readline()
        data = data.encode('utf-8')
        
        print('distance : ')
        print(data)
        
    except KeyboardInterrupt:
        break
    
port.close()