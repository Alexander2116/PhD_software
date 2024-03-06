from pyrometer import Raytek
from Ambrell import Ambrell
import asyncio
import schedule

TEMP_pyro = 0
TEMP_heater = 0
AMP = 0


async def run_pyro(device:Raytek):
    TEMP_pyro = device.read_N_temp()
    
async def run_heater(device:Ambrell):
    TEMP_heater = device.temp()
    
    
def read_pyro_temp(device:Raytek):
    return device.read_W_temp()

    
async def main(pyro:Raytek, heater:Ambrell):
    
    tasks = []
    tasks.append(asyncio.create_task(run_pyro(pyro)))
    tasks.append(asyncio.create_task(run_heater(heater)))
    

schedule.every(10).seconds.do(read_pyro_temp)
asyncio.run(main())