"""
Simple serial reader to communicate with pyrometer: Raytek marathon series 
"""

import serial

instr = serial.Serial("COM10")

instr.write(0x02)