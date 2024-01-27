import sys
import usb.core
import usb.util

device = usb.core.find(idVendor=0x198D, idProduct=0x4000)
if device is None:
    print("Is the brick connected and turned on?")
    sys.exit(1)