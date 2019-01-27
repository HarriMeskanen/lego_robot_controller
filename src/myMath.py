from math import cos, sin, pi

# class for n*n square matrices
class SquareMatrix(object):
    def __init__(self, n, data=None):
        self.n = n
        nn = n*n
        # if no data then make zero matrix
        if(data == None):
            self.data = [0 for val in range(0,nn)]
        
        elif(data == "I"):
            self.data = []
            diag = 0
            for i in range (0,nn):
                if(i == diag):
                    self.data.append(1)
                    diag += self.n+1
                else:
                    self.data.append(0)
        else:
            if(nn == len(data)):
                self.data = [val for val in data]
            else:
                print("Invalid arguments")
                return
    
    def testMethod(self):
        print("halo")
    
    # set value of element at index=[row, column]
    def __setitem__(self, index, val):
        self.data[self.n*(index[0]-1)+index[1]-1] = val
        
    # access matrix element at index=[row, column]
    def __getitem__(self, index):
        return self.data[self.n*(index[0]-1)+index[1]-1]
    
    # only works with other SquareMatrix objects
    def __add__(self, other):
        if(other.n == self.n):
            sumVal = SquareMatrix(self.n)
            for i in range(0,self.n*self.n):
                sumVal.data[i] = self.data[i]+other.data[i]   
            return sumVal
        else:
            print("cannot add")
    
    # only works with other SquareMatrix objects
    def __mul__(self, other):
        if(other.n == self.n):
            mulVal = SquareMatrix(self.n)
            for i in range(1,self.n+1):      # row for self              
                for j in range(1,self.n+1):  # column for other
                    val = 0
                    for k in range(1,self.n+1): # column for self, row for other
                        val += self[i,k]*other[k,j]
                    mulVal[i,j] = val
            return mulVal
        else:
            print("Cannot multiply")
           
    # output of "print" function
    def __str__(self):
        i = 1
        output = ""
        for element in self.data:
            output += str(element) + " "
            if i == self.n:
                output += "\n"
                i = 1
            else:
                i += 1        
        return output
                
##############################################################################                
                
# frame matrix
# inherits SquareMatrix and its operations
class A(SquareMatrix):
    def __init__(self,d,theta,a,alpha):
        
        stDHparam = [cos(theta),-sin(theta)*cos(alpha), \
                 sin(theta)*sin(alpha), a*cos(theta),\
                 
             sin(theta),cos(theta)*cos(alpha), \
                 -cos(theta)*sin(alpha), a*sin(theta), \
                 
             0, sin(alpha), cos(alpha), d, \
             
             0, 0, 0, 1]

        modDHparam = [cos(theta),-sin(theta),0,a, \
                      
                 sin(theta)*cos(alpha),cos(theta)*cos(alpha),\
                     -sin(alpha),-sin(alpha)*d,\
                     
                 sin(theta)*sin(alpha),cos(theta)*sin(alpha),\
                     cos(alpha),cos(alpha)*d,\
                     
                 0,0,0,1]
        
        # every A must be 4x4 square matrix
        #SquareMatrix.__init__(self,4,modDHparam)
        SquareMatrix.__init__(self,4,stDHparam)
        
                
                
                
            