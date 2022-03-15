import serial

port = '/dev/ttyACM0'
brate = 9600

ser = serial.Serial(port, brate, timeout=None)

while True :
    try :
        data = ser.readline()
        
        print('distance : ')
        print(data[2:8])
        
    except KeyboardInterrupt:
        break
    
port.close()