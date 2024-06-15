from pyquaternion import Quaternion
import numpy
from util import parsedoubles

class Pose_base:
    def __init__(self, name):
        self.name = name;

class PoseEye(Pose_base):
    def __init__(self, name):
        super().__init__(name)
        self.xdir = 0.0
        self.ydir = 0.0
        self.setposstring()
        
    def getTabbedData(self):
        return "{:.3f}".format(self.xdir) + '\t' + "{:.3f}".format(self.ydir)
        
    def setDir(self, x, y):
        self.xdir = x
        self.ydir = y
        self.setposstring()

    def setposstring(self):
        self.posstring = "{:.3f}".format(self.xdir) + ' ' + "{:.3f}".format(self.ydir)


class Pose(Pose_base):
    def __init__(self, name):
        super().__init__(name)
        self.setRotation(Quaternion())
        self.setPosition(0,0,0)
        self.sliderpos = [50,50,50,50]
        self.delta = 0.5;
        self.buttons = 0

    def setPosition(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.posstring = "{:.2f}".format(self.x) + ' ' + "{:.2f}".format(self.y) + ' ' + "{:.2f}".format(self.z)

    def setposstring(self, s):
        l = parsedoubles(s)
        if (len(l) == 3):
            self.setPosition(l[0],l[1],l[2])
    def setrotstring(self, s):
        l = parsedoubles(s)
        if (len(l) == 4):
            q = Quaternion(l[0], l[1], l[2],l[3])
            self.setRotation(q)

    def setRotation(self, q):
        self.rotation = q
        self.rotstring = "{:.2f}".format(q.elements[0])+ ' ' + "{:.2f}".format(q.elements[1]) + ' ' + "{:.2f}".format(q.elements[2]) + ' ' + "{:.2f}".format(q.elements[3])
        return

    def getTabbedPos(self):
        return "{:.2f}".format(self.x) + '\t' + "{:.2f}".format(self.y) + '\t' + "{:.2f}".format(self.z)
 
    def getTabbedRot(self):
        q = self.rotation
        return "{:.2f}".format(q.elements[0])+ '\t' + "{:.2f}".format(q.elements[1]) + '\t' + "{:.2f}".format(q.elements[2]) + '\t' + "{:.2f}".format(q.elements[3])

    def getTabbedData(self):
        return self.getTabbedPos() + "\t" + self.getTabbedRot()

    def getRotation(self):
        return self.rotation
        
    def setSlider(self, id, value):
        # bookkeeping
        diff = value - self.sliderpos[id]
        self.sliderpos[id] = value        
        # change the wanted axis
        if (id == 0): # X
            self.setPosition(self.x+diff*0.01, self.y, self.z)
        elif (id == 1): # Y
            self.setPosition(self.x, self.y+diff*0.01, self.z)
        elif (id == 2): # Z
            self.setPosition(self.x, self.y, self.z+diff*0.01)
        elif (id == 3): # Y
            self.setPosition(self.x+diff*0.01, self.y+diff*0.01, self.z+diff*0.01)

    def incrementPos(self, x, y, z):
        # change the wanted axis
        diffx = self.delta * x
        diffy = self.delta * y
        diffz = self.delta * z
        self.setPosition(self.x+diffx, self.y+diffy, self.z+diffz)
            
    def resetSlider(self, id, value):
        self.sliderpos[id] = value

    def setButton(self, state, code):
        bit = 1 << code
        if (state):
            self.buttons = self.buttons|bit
        else:
            bits = 15 - bit
            self.buttons = self.buttons&bits

    def getButtonState(self):
        return self.buttons