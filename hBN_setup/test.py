from Ambrell import Ambrell
from time import sleep

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))



# Commands
starting_char = ["","1,"]
terminating = ["","\r\n","\r","\n"]
comm = ["amps,10","AMPS,10","Amps,10","amp,10.0"]
encode = ["ascii",'utf-8','latin','utf-7','utf-16']


dev = Ambrell("COM9")

for i in starting_char:
        for j in terminating:
                for k in comm:
                        for l in encode:
                                dev.send_comm(k,encode=l,terminating_ch=j,start_ch=i)
                                sleep(0.25)

#dev.header() # print header
sleep(1)

#dev.help() # print all the commands
sleep(1)

print("set amps")
dev.set_amps(10) # set amps to 10
sleep(1)

print("stat")
dev.stat() # prints stat
sleep(1)

sleep(1)
print("set max amps")
dev.set_amps(dev.max_amps)
sleep(2)

print("set amps")
dev.set_amps(5)
sleep(1)