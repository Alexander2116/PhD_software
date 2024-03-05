"""
    Code for Ambrell induction heating system
    System uses RJ45 (RS485) but it must be converted to USB 
    
"""

import serial


class Ambrell:
    def __init__(self, com:str, baud:int=38400):
        self._com:str = com
        self._instr = serial.Serial(com,baud) # instrument
        
        
    def _send_comm(self,comm:str, arg:str):
        if(arg is not None):
            command =  "1," + command + "," + arg # self._com.replace("COM","")
        else:
            command = "1," + command 
        self._instr.write(command)
    
    def _read(self):
        return self._instr.read_all()