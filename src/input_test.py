# from <module> import <class/function>
from models import Link, Robot
from math import pi
import time

# tämä on testi kommentti :)
def main():
    links = getLinks()
    robot = Robot(links)
    #robot.setSensor("color",1)
    robot.setGearRatio([3,3.25,3])
     
    robot.runf([0,0,75])  

    for i in range(len(ops)):
        robot.runf(ops[i][1])
        ip = raw_input('place an object under my gripper')
        if not ip:
            continue
        else:
            continue
        
        
    robot.runf(q3up)
    robot.runf([-90,-45,0])
    robot.runf(ap[0])
    robot.runf(ap[1])
        
    robot.shutdown()
    

 
def getLinks():
        #-------------- DH PARAMETERS--------------
    a = [-9,0,0]
    alpha = [-pi/2, -pi/2, pi/2]
    d = [0, 0,-24]
    theta = [None, None, None]
    offset = [0,pi/2,pi/2]
    limits = [[-90,90],[-90,0],[0,90]] 
    # [PWM(+), PWM(-)]
    # for gravity compensation
    PWMs = [[25,-25],[8,-30],[35,-35]]
    #------------------------------------------
    links = []
    #for i in range(0,len(d)):
    for i in range(0,len(d)):
        link = Link(d[i],theta[i],a[i],alpha[i],\
                    offset[i],limits[i],PWMs[i])
        links.append(link)

    return links



# first operation piotn
q3up = [-90, -45]
q3down = [-90, 0]

# second operation point
q2up = [-45, -45]
q2down = [-45, 0]

# third operation point
q1up = [45, -45]
q1down = [45, 0]

# assembly point
apup = [0, -45]
apdown = [0, -3]

# operation points
ops = [[q1up, q1down],[q2up, q2down],[q3up, q3down]]
#assembly point
ap = [apup, apdown]
#colors 
colors = ["red", "black", "red"]


if __name__=="__main__":
    main()