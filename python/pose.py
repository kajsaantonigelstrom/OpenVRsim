from pyquaternion import Quaternion
import numpy

def base_splitstring(src, sep):

	#// Empty string must not generate anything in vector
	if (len(src) == 0):
		return;

	first = 0;
	last = len(src);
	dest = []
	while(True):
		next = src.find(sep, first);
		if (next < 0):
			next = len(src)
		part = ""
		if (next > first):
			part = src[first: next]
			dest.append(part)

		first = next + 1;       #// + 1 to remove the separator
		if (first >= last):
			break

	return dest

def parsedoubles(s):

	try:
		values = base_splitstring(s, " ");
		res = []
		for i in range(0,len(values)):
			v = (float)(values[i])
			res.append(v)
		return res
	except:
		return []


class Pose:
    def __init__(self, name):
        self.name = name;
        self.setRotation(Quaternion())
        self.setPosition(0,0,0)
        self.sliderpos = [50,50,50,50]
    
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
