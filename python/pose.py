class Pose:
    def __init__(self, name):
        self.name = name;
        self.w = 0.0
        self.i = 0.0
        self.j = 0.0
        self.k = 0.0
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
        self.posstring = "0 0 0"
        self.rotstring = "0 0 0 0"
        self.sliderpos = [50,50,50,50]
    def setposition(self,x,y,z):
        self.x = x
        self.y = y
        self.z = z
        self.posstring = "{:.2f}".format(self.x) + ' ' + "{:.2f}".format(self.y) + ' ' + "{:.2f}".format(self.z)

    def setrotation(self):
        print (self.name)
        return

    def setSlider(self, id, value):
        # bookkeeping
        diff = value - self.sliderpos[id]
        self.sliderpos[id] = value        
        # change the wanted axis
        if (id == 0): # X
            self.setposition(self.x+diff*0.1, self.y, self.z)
        elif (id == 1): # Y
            self.setposition(self.x, self.y+diff*0.1, self.z)
        elif (id == 2): # Z
            self.setposition(self.x, self.y, self.z+diff*0.1)
        elif (id == 3): # Y
            self.setposition(self.x+diff*0.1, self.y+diff*0.1, self.z+diff*0.1)
            
    def resetSlider(self, id, value):
        self.sliderpos[id] = value
