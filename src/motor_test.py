import time
from brickpi3 import *   #import BrickPi.py file to use BrickPi operations

#BrickPiSetup()  # setup the serial port for communication
bp = BrickPi3()

def main():

    try:
        print("PORT_A: ",bp.get_motor_status(bp.PORT_A))
        print("PORT_B: ",bp.get_motor_status(bp.PORT_B))
        print("PORT_C: ",bp.get_motor_status(bp.PORT_C))
        print("PORT_D: ",bp.get_motor_status(bp.PORT_D))
    except:
        bp.reset_all()
        
    bp.reset_all()

if __name__=="__main__":
    main()