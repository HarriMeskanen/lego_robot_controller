from brickpi3 import BrickPi3, SensorError
from myMath import SquareMatrix
import time


class Controller(BrickPi3):
    def __init__(self, links):
        # in brickpi ports are named "PORT_A", "PORT_B", "PORT_C", "PORT_D"
        # and their corresponding port indexing 1,2,4,8 -> dumb and not practical
        # to use. With this container we can use same indexing
        # for brickpi ports as we do for our models
        self.port = [1, 2, 4, 8]
        
        # initialize brickpi
        BrickPi3.__init__(self)
        self.reset_all()
        
        # gear ratios, dumb hack
        self.gr = [1 for i in links]
        # another dumb hack just to get things working
        self.rdy = [True for i in links]
        # on default tool should be in "close" position
        self.toolStatus = "close"                    
                
        # make sure that there's as many motors as there are links.
        # (robot base and tool are not links)
        for i in range(len(links)):
            try:
                self.set_motor_power(self.port[i],0)
                # set motor's position to 0
                offset = self.get_motor_encoder(self.port[i])
                self.offset_motor_encoder(self.port[i],offset)
            except:
                print("couldnt find motor in port ", self.port[i])
                time.sleep(2)
                continue
     
    # run motors to given joint values
    # forward kinematics
    # notation: property "PWM" is created to make it easier to 
    # distinguish what's referring to Link(PWM) and brickpi(power)
    def runf(self, links, qvals):
        # check if given qvals are within limits        
        if(self.checkq(links,qvals) == False):
            return False
        
        # initial q values
        q0 = self.getqvals(links)
        
        # calculate T for time step T_n (target position)
        Tn = self.fkine(links,qvals)
        
        self.rdy = [False for i in qvals]
        try:
            # loop until every joint is in target value
            while False in self.rdy:         
                for i in range(len(qvals)):
                    
                    if(self.rdy[i] == True):
                        continue
                           
                    try:
                        q = int(self.get_motor_encoder(self.port[i])/self.gr[i])
                        power = self.get_motor_status(self.port[i])[1]
                    except:
                        continue
                    
                    qq = qvals[i]
                    dq = qq-q
                    dq0 = q0[i] - q
                    
                    # update model
                    links[i].setq(q)
                    
                    # for debugging
                    print("q: ",q,", qq: ",qq,", dq: ",\
                          dq,", dq0: ",dq0,", power: ",power)
                                    
                    if(dq == 0):
                        self.set_motor_power(self.port[i],0)
                        self.rdy[i] = True
                        continue
                    
                    # unit vector (1 or -1) to see which way to run
                    n = dq/abs(dq)
                    if(n == 1):
                        # default value for motors PWM
                        defPWM = links[i].PWM[0]
                    elif(n == -1):
                        defPWM = links[i].PWM[1]
                        
                    #if (power == 0):
                    #    self.set_motor_power(self.port[i],defPWM)
                    #    continue
                    
                    # get current qvals
                    qivals = self.getqvals(links)
                    # add 1 to the value of current joint's q (i+1)
                    qivals[i] += n
                    # calculate T for time step t_i+1
                    Ti = self.fkine(links,qivals)   
                    # if moving against gravity 
                    # this implementaion only works only for this case
                    if(Tn[3,4] > Ti[3,4]):
                        g = True
                    else:
                        g = False
                    
                    # if running in "right way"
                    if (power <= 0 and dq < 0) or (power >= 0 and dq > 0):
                        if(0 <= abs(dq0) < 10):  
                            # acceleration
                            PWM = self.powerCurve(n,power,1,defPWM,g)
                            self.set_motor_power(self.port[i],PWM)
                            continue
                        if(1 < abs(dq) < 10):
                            # deacceleration
                            PWM = self.powerCurve(n,power,-1,defPWM,g)    
                            self.set_motor_power(self.port[i],PWM)
                            continue 
                        self.set_motor_power(self.port[i],defPWM)                                                   
                        
                    # if running in "wrong way"
                    else:
                        if(0 <= abs(dq0) < 10):  
                            # acceleration
                            PWM = self.powerCurve(n,power,1,defPWM,g)
                            self.set_motor_power(self.port[i],-1*PWM)
                            continue                        
                        if(1 <= abs(dq) < 10):
                            #deacceleartion
                            PWM = self.powerCurve(n,power,-1,defPWM,g)
                            self.set_motor_power(self.port[i],-1*PWM)
                            
                        else:
                            if(power < 0):                            
                                self.set_motor_power(self.port[i],links[i].PWM[0])      
                            else:
                                self.set_motor_power(self.port[i],links[i].PWM[1])
        
        except KeyboardInterrupt:
            return False
            
        time.sleep(0.5)
        return True
        
    def runColorCheck(self,port,color):
        color = color.capitalize()
        colors = ["none", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]
        t = time.time()
        counter = 0
        
        while(time.time() - t < 5):
            try:
                output = colors[self.get_sensor(port)]
                print(output)
                if(output == color):
                    counter += 1
            except SensorError as error:
                print("sensor error")
                
            if(counter > 20):
                return True
            
            time.sleep(0.02)
        return False
    
    
    def runTool(self,links,action):
        if(action == self.toolStatus):
            print("gripper is already ",action)
            return
        self.toolStatus = action
        
        if(action == "open"):
            q = 45

        elif(action == "close"):
            q = 0
        
        qvals = self.getqvals(links)
        qvals[-1] = q
        
        self.runf(links,qvals)      
            
    
    # solve inverse kinematic problem of coordinates xyz
    # and run motors to resulted joint values
    # NOT IMPLEMENTED 
    def runi(self, links, xyz):        
        # qvals = self.ikine(xyz)
        # self.runf(links, qvals)
        return True

    
    # method for checking validness of given joint values
    def checkq(self, links, qvals):        
        for i in range(len(qvals)):
            if(links[i].limits != None): 
                if not(links[i].limits[0] <= qvals[i] <= links[i].limits[1]):
                    print("Error: joint value exceeds limits")
                    time.sleep(1)
                    return False      
        return True
    
    
    def fkine(self, links, qvals):
        T = SquareMatrix(4,"I")
        for i in range(len(links)):        
            try:
                q = qvals[i]
            except IndexError:
                q = self.getqvals(links)[i]
            link = links[i]
            link.setq(q)
            T = T*link.getA()
        return T
    
    
    # NOT IMPLEMENTED
    def ikine(self, links, xyz):
        return 0
            
    
    def getqvals(self,links):
        qvals = []
        for link in links:
            qvals.append(link.getq())
        return qvals
    
    def shutdown(self):
        for i in range(0,4):
            try:
                self.set_motor_power(i,0)
            except:
                continue
        self.reset_all()
    
    # gr = [motor1 gr, motor2 gr, ...]
    def setGearRatio(self, gr):
        self.gr = gr
        
    # for acceleration
    # function max(x +- 1, defPWM/2.5)
    # n = direction, x = current value, dx = dx/dt, defx = x default value
    def powerCurve(self,n,x,dx,defx,g):
        d = 2
        if g == True:
            # if theres gravity denominator is 1.5
            d = 1.25

        if n == 1:
            if dx < 0:
                # if deaccelerating to positive direction
                x = int(max(x-1, defx/d))
            else:
                # if accelerating to positive direction
                x = int(min(x+1, defx/d))
        else:
            if dx < 0:
                # if accelerating to engative direction
                x = int(max(x-1, defx/d))   
            else:
                # if deaccelerating to negative direction
                x = int(min(x+1, defx/d))
        
        return x
        
        
        
        