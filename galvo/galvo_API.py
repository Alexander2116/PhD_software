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
import cv2
import numpy as np
import matplotlib.pyplot as plt

print(serial.__file__)

class Galvo:
    def __init__(self,com:str):
        self.inst = serial.Serial(com,baudrate = 38400)
    
    
    def _read(self):
        print(self.inst.readline())

    def _set_array_size(self, size:int):
        self.inst.write(("AS_"+str(size)+"/r/n").encode())
    
    def send_pattern(self, x: list, y: list):
        self._set_array_size(len(x))
        self._read()
        time.sleep(0.1)
        self.inst.write(b"GD/r/n")
        time.sleep(0.1)
        for i in range(len(x)):
            self.inst.write((str(x[i])+ "_"+ str(y[i]) + "/r/n").encode())
        self.inst.write(b"END/r/n")
        
class Pattern:
    def __init__(self):
        self.x_array = []
        self.y_array = []
    
    def detect_corners(self, image_path:str, maxCorners: int=27):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
        
        # detect corners with the goodFeaturesToTrack function. 
        corners = cv2.goodFeaturesToTrack(gray, maxCorners, 0.01, 10) 
        corners = np.int0(corners) 
        
        # we iterate through each corner,  
        # making a circle at each point that we think is a corner. 
        for i in corners: 
            x, y = i.ravel()
            self.x_array.append(x)
            self.y_array.append(y)
            

    def show_corners(self):
        for i in range(len(self.x_array)):
            print(self.x_array[i], self.y_array[i])
            
    def get_points(self):
        return self.x_array, self.y_array
    
            
# sorting alghorithm for shortest distance
def my_sort(x:list, y:list, o_x:list =[], o_y:list=[]):
    dis = []
    ordered_x = o_x
    ordered_y = o_y
    indecies = list(range(0,len(x)))
    if(len(ordered_x)==0):
        start_idx = indecies[0]
        ordered_x.append(x[start_idx])
        ordered_y.append(y[start_idx])
        del x[indecies[0]]
        del y[indecies[0]]
        del indecies[0]
        indecies = list(range(0,len(x)))

    for i in indecies:
        dis.append((ordered_x[-1]-x[i])**2 + (ordered_y[-1]-y[i])**2)
    
    ord_dis = sorted(range(len(dis)), key=lambda k: dis[k])
    ordered_x.append(x[ord_dis[0]])
    ordered_y.append(y[ord_dis[0]])
    
    del x[ord_dis[0]]
    del y[ord_dis[0]]
    if(len(indecies) == 1):
        print(ordered_x)
        print(ordered_y)
        return (ordered_x, ordered_y)
    else:
        return my_sort(x,y, ordered_x, ordered_y)
            

gal = Galvo("COM3")
pat = Pattern()
pat.detect_corners("galvo\\square.jpg")
x,y = pat.get_points()
print(my_sort(x,y))

gal.send_pattern(x,y)