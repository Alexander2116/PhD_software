"""
Simple serial reader to communicate with source meter: kei
"""

import serial
import serial.tools.list_ports
import sys
import time
import pyvisa
import pymeasure.instruments

# Should be GPIB
#keithley = rm.open_resource() 

def show_resources():
    rm = pyvisa.ResourceManager()
    print(rm.list_resources())


class Keithley:

    def __init__(self, connStr: str):
        self._instr = pymeasure.instruments.keithley.Keithley2400(connStr)

    def apply_voltage(self,V_range, comp_I):
        self._instr.apply_voltage(V_range,comp_I)

    def apply_current(self, I_range, comp_V):
        self._instr.apply_current(I_range,comp_V)

    def use_front(self):
        self._instr.use_front_terminals()
    
    def use_read(self):
        self._instr.use_rear_terminals()

    def disable_output_trigger(self):
        self._instr.disable_output_trigger()

    def source(self, on: bool=True):
        if(on):
            self._instr.enable_source()
        else:
            self._instr.disable_source()

    def ramp_to_current(self,target, steps:int=10, pause:float=0.05):
        self._instr.ramp_to_current(target,steps,pause)

    def ramp_to_voltage(self,target, steps:int=10, pause:float=0.05):
        self._instr.ramp_to_voltage(target,steps,pause)

    def shutdown(self):
        self._instr.shutdown()

"""
#ins = Keithley("GPIB0::12::INSTR")
#ins.Output("OFF")
instr = pymeasure.instruments.keithley.Keithley2400("GPIB0::12::INSTR")
#instr.disable_source()
instr.use_front_terminals()
#print(instr.measure_voltage())
#instr.disable_source()
instr.apply_voltage(10000000, 1.1)
instr.apply_current(2,20)
instr.disable_output_trigger()
instr.source_current_range = 2
instr.source_current = 2 
#print(instr.max_current)
instr.enable_source()
#instr.auto_output_off = True
#instr.ramp_to_voltage(15,50,0.1)
instr.ramp_to_current(2,20,0.1)

instr.disable_source()
instr.shutdown()

ports = serial.tools.list_ports.comports()
#print(ports)

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

se = serial.Serial("COM15", 9600)

se.write(b":OUTP:STAT 1\n\r")
se.write(b":FORM:ELEM RES\n\r")

while True:
    #se.write(b":OUTP?")
    #se.write(b"SomeBullshit\n\r") # still receiving /x00
    print(se.read_all())
    #se.write(b":STAT:MEAS?")
    time.sleep(1)

"""
show_resources()