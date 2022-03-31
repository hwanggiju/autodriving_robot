from smtplib import OLDSTYLE_AUTH
import serial
from matplotlib import pyplot as plt
from matplotlib import animation
import numpy
import random
import time
import numpy as np

port = '/dev/ttyACM0'
brate = 9600

ser = serial.Serial(port, brate, timeout=None)

def ReadData():
    data = ser.readline()
    data = int(data.decode()[:len(data)-1])
    return data

fig = plt.figure()
ax = plt.axes(xlim=(0, 50), ylim=(4, 13))
line, _ = ax.plot([], [], lw=1, c='blue', marker='d', ms=2)
max_points = 50
line, _ = ax.plot(np.arange(max_points), np.ones(max_points, dtype=np.float) * np.nan, lw = 1, c='blue',
                  marker='d', ms=2)

def init():
    return line
    
def animate(i) :
    y = ReadData()
    old_y = line.get_ydata()
    new_y = np.r_[old_y[1:, y]]
    line.set_ydata(new_y)
    print(new_y)
    
    return line,

anim = animation.FuncAnimation(fig, animation, init_func=init, frames=200, interval=20, blit=False)
plt.show()