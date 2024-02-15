"""
4-channel 500MHz 1GS/s Digital Scope
RS232/GPIB interface
"""

import pyvisa


def show_resources():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())

class LeCroy:
    def __init__(self, conn_string:str = "GPIB::0::INSTR"):
        rm = pyvisa.ResourceManager()
        self.instr = rm.open_resource(conn_string)
        #self.instr.open()
        # determine what model this scope is
        (self.manufacturer, self.model, self.serial_number, self.firmware_version) = self.instr.query('*IDN?').split(',')
        
    def info(self):
        print(self.manufacturer, self.model, self.serial_number, self.firmware_version)
        
    def reset(self):
        self.instr.query("*RST")
    
    
        
        

show_resources()
    