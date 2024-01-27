import serial
import time

sh = serial.Serial("COM17",9600)

#sh.write(b"help\r")

sh.write(b"H\r\n")
sh.flush()
time.sleep(0.1)
while(True):
    text = sh.read_all()
    if(len(text) > 0):
        print(text)
        