"""
Simple serial reader to communicate with pyrometer: Raytek marathon series 
"""

import serial
import serial.tools.list_ports

def show_ports():
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))

# Class assumes 2 USB connections: one to Tx, one to Rx
class Raytek:
    def __init__(self, Rx_com:str, Tx_com:str, baud_rate = 38400):
        self._re = serial.Serial(Rx_com, baud_rate)
        self._wr = serial.Serial(Tx_com,baud_rate)
    
    def _read(self):
        l = 0
        text:str = ""
        while(l<4):
            text=self._re.read_all()
            l = len(text)
        if("\r\n" not in str(text[0:len(text)].decode("utf-8"))):
            return "0\r\n".encode("utf-8")
        else:
            return text
    
    def _write(self, comm:str):
        text = comm + "\r\n"
        self._wr.write(str.encode(text))

    def read_N_temp(self):
        self._write("?N")
        return self._read()
    
    def read_W_temp(self):
        self._write("?W")
        return self._read()
    
    # poll/burst mode
    def PB_mode(self, mode:str = "P"):
        self._write("V="+mode)
