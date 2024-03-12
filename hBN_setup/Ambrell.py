"""
    Code for Ambrell induction heating system
    System uses RJ45 (RS485) but it must be converted to USB 
    
"""

import serial
import time

class Ambrell:
    def __init__(self, com:str, baud:int=38400):
        self._com:str = com
        self._instr = serial.Serial(com,baud) # instrument
        self.var_max_amps = 0
        self.__max_amps()
        
    def __send_comm(self,comm:str, arg:str=None):
        if(arg is not None):
            command =  "1," + comm + "," + arg # self._com.replace("COM","")
        else:
            command = "1," + comm 
        self._instr.write(command.encode('utf-8'))
    
    def __read(self) -> str:
        l = 0
        text:str = ""
        while(l<4):
            text=self._instr.read_all()
            l = len(text)
        if("\r\n" not in str(text[0:len(text)].decode("utf-8"))):
            return "0\r\n".encode("utf-8")
        else:
            return text
        
    def __max_amps(self):
        self.__send_comm("maxamps")
        self.var_max_amps = int(self.__read())
    
    @property
    def max_amps(self) -> float:
        return self.var_max_amps
    
    def help(self):
        self.__send_comm("?")
        print(self.__read())
        
    def header(self):
        # Shows CHDR and Ctime
        # CHDR (pronounced "Cheddar", like the cheese) or "Compressed Header" packets
        # Ctime is the time the file's inode was last changed, while mtime is the last time the file's contents were changed
        self.__send_comm("c?")
        print(self.__read())
    
    def rtemp(self):
        # raw temperature
        self.__send_comm("rtemp")
        return self.__read()
    
    def temp(self):
        # raw temperature
        self.__send_comm("temp")
        return self.__read()
    
    def set_amps(self, value:float) -> None:
        # can be set from 0 to max_amps
        self.__send_comm("amps", value)
        
    def stat(self):
        self.__send_comm("stat")
        print(self.__read())
        
    def timer(self, timer:float):
        self.__send_comm("timer",timer)
        
class Ambrellv2:
    def __init__(self, Tcom:str,Rcom, baud:int=38400):
        self._com=Tcom
        self._re = serial.Serial(Rcom, baud)
        self._wr = serial.Serial(Tcom, baud)
        self.var_max_amps = 0
        #self.__max_amps()
        
    def __send_comm(self,comm:str, arg:str=None):
        if(arg is not None):
            command =  "1," + comm + "," + str(arg) + "\r\n" # self._com.replace("COM","")
        else:
            command = "1," + comm + "\r\n"
        self._wr.write(command.encode('utf-8'))
    
    def __read(self) -> str:
        l = 0
        text:str = ""
        while(l<4):
            text=self._re.read_all()
            l = len(text)
            if(l>1):
                print(text)
        if("\r\n" not in str(text[0:len(text)].decode("utf-8"))):
            return "0\r\n".encode("utf-8")
        else:
            return text
        
    def __max_amps(self):
        self.__send_comm("maxamps")
        self.var_max_amps = int(self.__read())
    
    @property
    def max_amps(self) -> float:
        return self.var_max_amps
    
    def help(self):
        self.__send_comm("?")
        print(self.__read())
        
    def header(self):
        # Shows CHDR and Ctime
        # CHDR (pronounced "Cheddar", like the cheese) or "Compressed Header" packets
        # Ctime is the time the file's inode was last changed, while mtime is the last time the file's contents were changed
        self.__send_comm("c?")
        print(self.__read())
    
    def rtemp(self):
        # raw temperature
        self.__send_comm("rtemp")
        return self.__read()
    
    def temp(self):
        # raw temperature
        self.__send_comm("temp")
        return self.__read()
    
    def set_amps(self, value:float) -> None:
        # can be set from 0 to max_amps
        self.__send_comm("amps", value)
        
    def stat(self):
        self.__send_comm("stat")
        print(self.__read())
        
    def timer(self, timer:float):
        self.__send_comm("timer",timer)