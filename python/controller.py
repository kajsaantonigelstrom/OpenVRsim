import wx
import zmqsocket
from pose import Pose
from pyquaternion import Quaternion

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
        
        # System button S/L grip G/H app:F/J trig:D/K
        self.allowedKeysLeft = "SDFG";
        self.allowedKeysRight = "LKJH"
        self.lastcmd = ""

    def setSelectedDevice(self, dev):
        self.currentDevice = dev

    def sendAndRcv(self, cmd):
        #print (cmd)
        answer = self.ZMQ.sendcommand(cmd)
        if (answer.lower() != "ok"):
            print (cmd,"answer is:", answer)

    def sendRotPos(self, device):
        cmd = self.devicecmds[device] + self.devices[device].posstring
        self.sendAndRcv(cmd)
        
        cmd = self.devicecmds[device] + self.devices[device].rotstring
        self.sendAndRcv(cmd)

    def sendButtonState(self, device):
        cmd = self.devicecmds[device] + "b" + str(self.devices[device].getButtonState())
        if (cmd != self.lastcmd):
            self.lastcmd = cmd
            self.sendAndRcv(cmd)
        
    def setSlider(self, id, value):
        device = self.devices[self.currentDevice]
        device.setSlider(id, value)
        self.sendRotPos(self.currentDevice)
        
    def resetSlider(self, id, value):
        device = self.devices[self.currentDevice]
        device.resetSlider(id, value)

    def setRotation(self, q):
        device = self.devices[self.currentDevice]
        device.setRotation(q)
        self.sendRotPos(self.currentDevice)


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

        