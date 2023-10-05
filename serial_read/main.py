"""
Program is supposed to connect to Keithley SourceMeter, setup a voltage/current to a lamp. 
It should connect to pyrometer as well and take readings of lamp's temperature.

__ Initial Concept __ 

Flow:
1. Set voltage/current
2. Read temperature (wait till stabilizes)
3. Change temperature (different voltage/current)

Classes:
1. Keithley
    - requires 1 USB
2. Pyrometer (Raytek, marathon series)
    - requires 2 USBs: one for Rx, second for Tx
    - It can be reduced to only Rx if we setup continous string output


Methods:
1. Check-if-temperature-is-stable -> bool/void
    - How do I define "stable"?
2. Sub-main 
    - It's a loop that works until temperature-is-stable 
3. Turn on voltage
4. Read temperature
"""

import Keithley
import pyrometer
import time

pyrometer.show_ports()
Keithley.show_resources()

keit = Keithley.Keithley("GPIB0::12::INSTR")
pyro = pyrometer.Raytek("COM11","COM14")


def set_current(current, voltage):
    keit.apply_current(current, voltage)
    keit.disable_output_trigger()
    keit.ramp_to_current(current,10,0.1)

# Need to test it first
def read_temp():
    temp = pyro.read_W_temp()
    print(temp)
    if("EUUU" in str(temp[0:len(temp)-2].decode("utf-8"))):
        return 0
    else:
        print(temp)
        return float(str(temp[0:len(temp)-2].decode("utf-8")).replace("W","").replace("\r\n","").replace("!",""))

def is_stable(tolerance:float = 1, time_step:float = 1) -> bool:
    temp0 = read_temp()
    time.sleep(time_step)
    temp1 = read_temp()
    print(temp0)
    print("Temperature difference after ", time_step, "s: ", temp1-temp0)
    if abs((temp1-temp0)) < tolerance:
        return True
    else:
        return False
        
def wait_till_stable(tolerance:float = 1, time_step:float = 1):
    stable = False
    while(stable != True):
        stable = is_stable(tolerance, time_step)
    print("Final temperature: ", read_temp())

def set_temperature(target:float):
    temp = read_temp()
    print(temp)
    vol=15
    while(abs(target-temp)>0.5):
        set_current(1,vol)
        wait_till_stable()
        temp=read_temp()
        if(target-temp >0.5):
            vol += 0.1

def main():
    set_temperature(1000)


#main()
keit.shutdown()

#set_current(1,10)
#keit.source(True)
#keit.shutdown()