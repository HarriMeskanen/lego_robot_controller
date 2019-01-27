# Dexter Industries
# Initial Date: Sep 19, 2017
# Borja Ramis
# This code may be used for rotating two motors the specified amount of degrees at the same time

from BrickPi import *
BrickPiSetup()
BrickPiSetupSensors()
BrickPiUpdateValues()

BrickPi.MotorEnable[PORT_A] = 1 #Enable the Motor A
BrickPi.MotorEnable[PORT_D] = 1 #Enable the Motor D

##set_motor_position(PORT_A, 60)

# Following lines for reseting the LEGO Motor Encoder value.
# This is needed because motorRotateDegree() does not reset the encoder value and if this function is executed 2 times will not work at second time
BrickPiUpdateValues()
for i in range(len(BrickPi.MotorEnable)):
    if not BrickPi.MotorEnable[i]: continue
    if BrickPi.Encoder[i] is 0: continue
    BrickPi.EncoderOffset[i] = BrickPi.Encoder[i]
while BrickPiUpdateValues():
    pass
# Now, the value of the LEGO Motor Encoder is 0

power = [15,15]
deg = [90,90]
port = [PORT_A,PORT_D]

motorRotateDegree(power,deg,port)

a = BrickPi.Encoder[PORT_A]
b = BrickPi.Encoder[PORT_D]
c = a %720 /2
d = b %720 /2

print ( "PORT_A:Count: %s ||| PORT_D:Count: %s" % (a,b)) # print the encoder degrees
print ( "PORT_A:Degrees: %s ||| PORT_D:Degrees: %s" % (c,d)) # print the encoder degrees