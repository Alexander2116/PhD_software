from pyrometer import Raytek
from Ambrell import Ambrell
from my_pid import PID
import asyncio
import schedule
import time
import matplotlib.pyplot as plt
from datetime import datetime
import os
import numpy as np

TEMP_pyro = 0
TEMP_heater = 0
AMP = 0

def create_txt():
    name = datetime.now().strftime("%d_%m_%Y_%H_%M")
    if not os.path.exists("./data"):
        os.mkdir("./data")

    with open("./data/"+name+".txt", "w") as f:
    # Write some text to the file
        f.write("time [s], temperature [C]")
    f.close()
    return name

# Could be better than just openning and closing
# preferably open once save line by line and close
def add_data(name:str, time:float, temp:float):
    with open("./data/"+name+".txt", "w") as f:
    # Write some text to the file
        f.write(time+","+temp)
    f.close()
    

async def run_pyro(device:Raytek):
    TEMP_pyro = device.read_N_temp()
    
async def run_heater(device:Ambrell):
    TEMP_heater = device.temp()
    
def set_temperature(device1:Raytek, device2:Ambrell, set_temp:float) -> float:
    device2.set_amps(device2.max_amps)
    pid = PID(set_temp, 1, 0.1, 0.1)
    stable_amps = 0
    temp = device1.read_N_temp()
    max_amps = device2.max_amps()
    # max amp till point of interest
    while temp < set_temp-1:
        temp = device1.read_N_temp()
        time.sleep(0.01)
    # set amps untill stable
    i = 0
    tem_diff = np.abs(temp - set_temp )
    while i < 1000 :
        i+=1
        out = pid.update(device1.read_N_temp())
        device2.set_amps(out/max_amps)
        if(tem_diff > 0.5):
            i=0
    
    stable_amps = out/max_amps
    
    return stable_amps
    
async def hold_temperature(set_temp:float, duration:int):
    start_time = time()

    current_time = start_time
    while current_time <= start_time + duration:

        current_time = time()

async def decrease_temp(set_temp:float, decrease_Rate:float):
    #decrease_Rate: C/h
    a = 2
    
    
def read_pyro_temp(device:Raytek):
    return device.read_N_temp()

    
async def main(pyro:Raytek, heater:Ambrell):
    
    tasks = []
    tasks.append(asyncio.create_task(run_pyro(pyro)))
    tasks.append(asyncio.create_task(run_heater(heater)))
    
"""
schedule.every(10).seconds.do(read_pyro_temp)
asyncio.run(main())
"""

create_txt()