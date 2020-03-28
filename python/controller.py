import wx
import zmqsocket
from pose import Pose
from pyquaternion import Quaternion
from testcasereader import TestCaseReader
class Controller():
    def __init__(self):
        self.lefthandle = Pose("Left")
        self.righthandle = Pose("Right")
        self.HMD = Pose("HMD")
        self.currentDevice = 0
        self.systemcmds = ["", "Ls", "Rs"]
        self.triggercmds = ["", "Lt", "Rt"]
        self.devicecmds = ["H ", "L ", "R "]
        self.devices = [ self.HMD, self.lefthandle, self.righthandle ] ## order corresponds to currendDevie
        self.ZMQ = zmqsocket.ZMQsocket()
        self.testcaseinprogress = False
        # System button S/L grip G/H app:F/J trig:D/K
        self.allowedKeysLeft = "SDFG";
        self.allowedKeysRight = "LKJH"
        self.lastcmd = ""
        self.statusstring = "No Test Case Loaded"

    def setSelectedDevice(self, dev):
        self.currentDevice = dev

    def sendAndRcv(self, cmd):
        #print (cmd)
        answer = self.ZMQ.sendcommand(cmd)
        if (answer.lower() != "ok"):
            print (cmd,"answer is:", answer)

    def sendPos(self, device):
        if (self.testcaseinprogress):
            return
        cmd = self.devicecmds[device] + "P " + self.devices[device].posstring
        self.sendAndRcv(cmd)

    def sendRot(self, device): 
        if (self.testcaseinprogress):
            return
        cmd = self.devicecmds[device] + "R " + self.devices[device].rotstring
        self.sendAndRcv(cmd)

    def sendButtonState(self, device):
        if (self.testcaseinprogress):
            return
        cmd = self.devicecmds[device] + "K " + str(self.devices[device].getButtonState())
        if (cmd != self.lastcmd):
            self.lastcmd = cmd
            self.sendAndRcv(cmd)
        
    def setSlider(self, id, value):
        device = self.devices[self.currentDevice]
        device.setSlider(id, value)
        self.sendPos(self.currentDevice)
        
    def resetSlider(self, id, value):
        device = self.devices[self.currentDevice]
        device.resetSlider(id, value)

    def setRotation(self, q):
        device = self.devices[self.currentDevice]
        device.setRotation(q)
        self.sendRot(self.currentDevice)


    def getRotation(self):
        device = self.devices[self.currentDevice]
        return device.getRotation()

    def resetxyz(self, xy):
        q = Quaternion(1,0,0,0)
        if (xy==1):
            q = Quaternion(axis=[1.0, 0.0, 0.0], degrees=90)
        elif (xy==2):
            q = Quaternion(axis=[0.0, 1.0, 0.0], degrees=-90)
        self.setRotation(q)

    def KeyEvent(self, down, key):
        keystring = str(chr(key))
        pos = self.allowedKeysLeft.find(keystring)
        if (pos >= 0):
            self.devices[1].setButton(down, pos)
            self.sendButtonState(1)

        pos = self.allowedKeysRight.find(keystring)
        if (pos >= 0):
            self.devices[2].setButton(down, pos)
            self.sendButtonState(2)

    def startTest(self, folder):
        self.testcaseinprogress = True
        cmd = "G T s"
        self.sendAndRcv(cmd)

    def stopTest(self):
        self.testcaseinprogress = False
        cmd = "G T e"
        self.sendAndRcv(cmd)

    def loadTestCase(self, folder):
        self.statusstring = ""
        readers = []
        readers.append(TestCaseReader(folder+"\\HMD.csv"))
        readers.append(TestCaseReader(folder+"\\Left.csv"))
        readers.append(TestCaseReader(folder+"\\Right.csv"))
        for i in range(0,3):
            if readers[i].error != "":
                self.statusstring = readers[i].filename + " " + readers[i].error
                return
        
        # clear previous test case
        cmd = "G T c"
        self.sendAndRcv(cmd)

        for i in range(0,3):
            print (readers[i].filename, readers[i].size())
            if readers[i].size() > 0:
                for j in range(0, readers[i].size()):
                    cmd =  self.devicecmds[i] + "T " + readers[i].data[j]
                    self.sendAndRcv(cmd)
                self.statusstring = self.statusstring + " " + readers[i].tellfilename()
        if (self.statusstring == ""):
            self.statusstring = "No Files Found"
        else:
            self.statusstring = "Loaded: " + folder + " " + self.statusstring