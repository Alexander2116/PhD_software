from Ambrell import Ambrellv2
from time import sleep

import serial.tools.list_ports
ports = serial.tools.list_ports.comports()

for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))


dev = Ambrellv2("COM8","COM9")

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