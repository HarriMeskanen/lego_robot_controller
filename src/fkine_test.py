# from <module> import <class/function>
from models import Link, Robot
from math import pi

def main():
    links = getLinks()
    robot = Robot(links)
    robot.setSensor("color",1)
    robot.setGearRatio([3,3.25,3])

    q1 = robot.fkine([0,0])
    q2 = robot.fkine([0,-45])
    
    print(q1[3,4])
    print(q2[3,4])

    
 
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
    PWMs = [[30,-30],[10,-30],[50,-50]]
    #------------------------------------------
    links = []
    #for i in range(0,len(d)):
    for i in range(0,len(d)):
        link = Link(d[i],theta[i],a[i],alpha[i],\
                    offset[i],limits[i],PWMs[i])
        links.append(link)

    return links

        

# start point
q0 = [0,0,0]

# first operation piotn
q1up = [-90, -45, 0]
q1down = [-90, -5, 0]

# second operation point
q2up = [-45, -45, 0]
q2down = [-45, -5, 0]

# third operation point
q3up = [45, -45, 0]
q3down = [45, -5, 0]

# assembly point
apup = [90, -45, 0]
apdown = [90, -5, 0]

# operation points
ops = [[q1up, q1down],[q2up, q2down],[q3up, q3down]]
#assembly point
ap = [apup, apdown]
#colors 
colors = ["red", "black", "red"]


if __name__=="__main__":
    main()