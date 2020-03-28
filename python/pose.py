from pyquaternion import Quaternion
import numpy
from util import parsedoubles


class Pose:
    def __init__(self, name):
        self.name = name;
        self.setRotation(Quaternion())
        self.setPosition(0,0,0)
        self.sliderpos = [50,50,50,50]
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

    def getRotation(self):
        return self.rotation

    def setSlider(self, id, value):
        # bookkeeping
        diff = value - self.sliderpos[id]
        self.sliderpos[id] = value        
        # change the wanted axis
        if (id == 0): # X
            self.setPosition(self.x+diff*0.1, self.y, self.z)
        elif (id == 1): # Y
            self.setPosition(self.x, self.y+diff*0.1, self.z)
        elif (id == 2): # Z
            self.setPosition(self.x, self.y, self.z+diff*0.1)
        elif (id == 3): # Y
            self.setPosition(self.x+diff*0.1, self.y+diff*0.1, self.z+diff*0.1)
            
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