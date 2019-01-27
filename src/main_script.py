# from <module> import <class/function>
from models import Link, Robot
from math import pi
import time

def main():
    links = getLinks()
    robot = Robot(links)
    robot.setGearRatio([3,3.25,3])
        
    initialize_demo(robot)
    robot.setSensor("color",1)
    time.sleep(2)
    
    i = 0
    while i < 2:
        
        if not ops:
            robot.runf([-20,0,0])
            print("done")
            robot.shutdown()
            return 0
       
        if i >= len(ops):
            break
        
        #ops = list of operations points, defined bleow
        robot.runf(ops[i][0])                
        robot.runTool("open")
        robot.runf(ops[i][1])
        robot.runTool("close")
            
        if(robot.runColorCheck(colors[0])):
            # run to assembly point
            #robot.runTool("close")
            robot.runf(ap[0])
            ap[1][0] -= 1*(3-len(ops))
            ap[1][1] -= 2*(3-len(ops))
            robot.runf(ap[1])
            time.sleep(0.5)
            robot.runTool("open")
            time.sleep(0.5)
            robot.runf(ap[0])
            del ops[i]
            del colors[0]
            i = 0
        else:
            robot.runTool("open")
            robot.runf(ops[i][0])
            #robot.runTool("close")
            i += 1
            
    print("something went wrong :D")
    robot.shutdown()
    

 
def getLinks():
        #-------------- DH PARAMETERS--------------
    a = [-9,0,0]
    alpha = [-pi/2, -pi/2, pi/2]
    d = [0, 0,-24]
    theta = [None, None, None]
    offset = [0,pi/2,pi/2]
    limits = [[-100,100],[-90,0],[0,90]] 
    # [PWM(+), PWM(-)]
    # for gravity compensation
    PWMs = [[25,-25],[8,-30],[45,-45]]
    #------------------------------------------
    links = []
    #for i in range(0,len(d)):
    for i in range(0,len(d)):
        link = Link(d[i],theta[i],a[i],alpha[i],\
                    offset[i],limits[i],PWMs[i])
        links.append(link)

    return links


def initialize_demo(robot):
    robot.runf([0,0,65])  

    for i in range(len(ops)):
        coord = ops[i][1]
        coord[0] += 4
        robot.runf(coord)
        ip = raw_input('place an object under my gripper')
        if not ip:
            continue
        else:
            continue
               
    robot.runf(q3up)
    robot.runf([-90,-45,0])
    robot.runf(ap[0])
    robot.runf(ap[1])

# first operation piotn
q3up = [-90, -45]
q3down = [-90, -3]

# second operation point
q2up = [-45, -45]
q2down = [-45, -3]

# third operation point
q1up = [45, -45]
q1down = [45, -3]

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