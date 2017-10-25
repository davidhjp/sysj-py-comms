from sysj.signal import *
import time

def main():

    def inputHandler(nodeid, actuatorid, val):
        print "received: nodeid: {:02X} actuatorid: {:02X}".format(nodeid, actuatorid) +" value " + str(val)

    x = SysJInput('localhost', 2000, inputHandler)
    sjout = SysJOutput('localhost', 1000)
    while True:
        value = bytearray([20,200,10,200,1,3])
        sjout.send(0x0A, TYPE_THL, value)
        time.sleep(2)
        sjout.send(0x1E, TYPE_POWER, "\x02\xFF")
        time.sleep(2)
        sjout.send(0x1E, TYPE_STATE, "\x01")
        time.sleep(2)

if __name__ == "__main__":
    main()
