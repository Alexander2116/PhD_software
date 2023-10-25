"""
Python 3.10.
Galvarometer scanner PROTOTYPE

API for the galvarometer (SCANLAB Hurry) that uses XY2-100 protocol and is controlled using teensy 4.0.
API should send data points to be stored in the controler OR vectors (commands for line etc). Vector functions should be defined in the controller.
Flash memory of teensy 4.0 is 2 Mbyte. It would be better NOT to send the whole bunch of code.
 

FROM API:
- set DELAY
- create figure/pattern with Start and End point (vector like) instead of invidual points.

IDEAS FOR TEENSY:
- VOID DrawLine (start point, end point, step)
even better, instead of vectors (start, end), use array of next points e.g [p1,p2,p3,p4]: p1->p2->p3->p4->p1->p2->...
so instead of 4 arrays we would require 2 (memory efficient)

HOW TO MAKE IT FASTER:
- program teensy in C (now in Arduino-like code)
- create C / C++ / C# API for higher speed
- Teensy seems fast enough but the issue is the scanner that cannot handle high speed from teensy (is it because of differential line driver?)
- Different scanner 
"""

import serial
import time

class Galvo:
    
    def __init__(self,com:str):
        self.inst = serial.Serial(com,baudrate = 38600)
        
    def _set_array_size(self, size:int):
        self.inst.write(("AS_"+str(size)+"/r/n").encode())
    
    def send_pattern(self, x: list, y: list):
        self.inst.write(b"GD/r/n")
        time.sleep(1)
        for i in range(len(x)):
            self.inst.write((str(x[i])+ "_"+ str(y[i]) + "/r/n").encode())
        self.inst.write(b"END/r/n")