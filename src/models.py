from myMath import SquareMatrix, A, cos, sin, pi
from logic import Controller
import time

# Link object is designed to be similar to Matlab Robotic
# Toolbox's Links. In the beginning of each Link there's frame.
# Frame matrices are constructed with 'modified' notation.
# Initial joint value for all joints 0, if changed make sure to also
# change in Controller.__init__()
class Link(object):
    def __init__(self,d,theta,a,alpha,offset,limits,PWM):
        # joint value
        self.q = 0
        self.a = a
        self.alpha = alpha
        # offset for joint value
        self.offset = offset
        # limit values for joint variables
        self.limits = limits
        # pulse-width modulation [(+)direction, (-)direction]
        # two values for gravity compensation. This implementation only
        # works for the cases where the effects of gravity are constant
        self.PWM = PWM
        
        if(d is None):
            self.linkType = "T" # translation
            self.theta = theta
            # transformation matrix from frame_i to frame_i+1 (modified)
            self.A = A(0+offset,theta,a,alpha)
        else:
            if(theta is None):
                self.linkType = "R" # rotation
                self.d = d
                self.A = A(d,0+offset,a,alpha)
            else:
                print("Either d or theta must be None")
                return False
            
    def getA(self):
        return self.A  

    def getq(self):
        return self.q
    
    # for modifeid
    #def setq(self, val):               
    #   self.q = val
    #    val += self.offset
    #    if(self.linkType == "R"):
    #        self.A[1,1] = cos(val)
    #        self.A[1,2] = -sin(val)
    #        self.A[2,1] = sin(val)*cos(self.alpha)
    #        self.A[2,2] = cos(val)*cos(self.alpha)
    #        self.A[3,1] = sin(val)*sin(self.alpha)
    #        self.A[3,2] = cos(val)*sin(self.alpha)
    #    else:
    #        self.A[2,4] = -sin(self.alpha)*val
    #        self.A[3,4] = cos(self.alpha)*val
    #    return True
    
    # for standard dh params
    def setq(self, val):         
        self.q = val
        # convert into radians
        val = val*pi/180
        val += self.offset
        
        if(self.linkType == "R"):
            self.A[1,1] = cos(val)
            self.A[1,2] = -sin(val)*cos(self.alpha)
            self.A[1,3] = sin(val)*sin(self.alpha)
            self.A[1,4] = self.a*cos(val)
            self.A[2,1] = sin(val)
            self.A[2,2] = cos(val)*cos(self.alpha)
            self.A[2,3] = -cos(val)*sin(self.alpha)
            self.A[2,4] = self.a*sin(val)
        else:
            self.A[3,4] = val
        return True
   
##############################################################################
         
# A base class for robot objects. Robot consists of links, base,
# tool and logic controller. 
class Robot(object):
    def __init__(self,links):
        self.links = links              # container of Link objects
        self.base = SquareMatrix(4)     # frame 0, base frame
        self.tool = None 
        self.sensors = {}               # dictionary of sensors
        self.ctrl = Controller(links) # brickpi here, see module logic.py
     
        
    # 'run' to input joint values
    # forward kinematics
    def runf(self, qvals):
        status = self.ctrl.runf(self.links,qvals)
        if not status:
            print("Error in runf")
            time.sleep(2)
        return status
            
    
    # 'run' to position xyz
    # inverse kinematics
    def runi(self, xyz):
        return self.ctrl.runi(self.links,xyz)
    
    
    # color's first letter must be capitalized (Red, Green, ...)
    def runColorCheck(self,color):
        port = self.sensors.get("color")
        #turn on the sensor
        #self.ctrl.set_sensor_type(port, 20)
        # run the check
        status = self.ctrl.runColorCheck(port,color)
        # turn off the sensor
        #self.ctrl.set_sensor_type(port, 1)
        return status
        
        
    def fkine(self,qvals):
        T = self.ctrl.fkine(self.links,qvals)
        return T+self.base
    
    
    def ikine(self, xyz):
        return self.ctrl.ikine(self.links, xyz)
        
    
    def toolPoint(self):
        return self.fkine(self.ctrl.getq())
    

    def setBase(self, base):
        B = SquareMatrix(4)
        if(len(base) != 3):
            print("invalid robot base")
            return False
        B[1,4] = base[0]
        B[2,4] = base[1]
        B[3,4] = base[2]
        self.base = B
        return True
    
    def runTool(self, action):
        self.ctrl.runTool(self.links,action)
    
    # not workingn
    def setTool(self, tool):
        if(len(tool) != 3):
            print("invalid robot tool")
            return False
        A = self.links[-1].getA()
        if(self.tool != None):
            A[1,4] -= self.tool[0]
            A[2,4] -= self.tool[1]
            A[3,4] -= self.tool[2]
        A[1,4] += tool[0]
        A[2,4] += tool[1]
        A[3,4] += tool[2]
        self.tool = tool
        return True
        
    
    def setSensor(self, sensorType, port):
        if(sensorType == "color"):
            self.sensors["color"] = port
            self.ctrl.set_sensor_type(port, 20)
            return True
        else:
            print("Sensor type not supported")
            return False

    # stupid hack to allow more simple models
    def setGearRatio(self, gr):
        self.ctrl.setGearRatio(gr)
        
    def shutdown(self):
        self.ctrl.reset_all()
        
        
        
        
        
        
        
        