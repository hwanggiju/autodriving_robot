import serial

port = '/dev/ttyACM0'
brate = 9600

ser = serial.Serial(port, brate, timeout=None)

while True :
    try :
        data = port.readline()
        
        print('distance : ')
        print(data)
        
    except KeyboardInterrupt:
        break
    
port.close()