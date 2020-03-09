import wx
import zmqsocket
from pose import Pose
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

    def setrotation(self):
        self.devices[self.currentDevice].setrotation()
        return;

    def setSelectedDevice(self, dev):
        self.currentDevice = dev

    def sendSystem(self, device):
        cmd = self.systemcmds[device]
        print (cmd)
        print (self.ZMQ.sendcommand(cmd))

    def sendTrigger(self, device):
        cmd = self.triggercmds[device]
        print (cmd)
        print (self.ZMQ.sendcommand(cmd))

    def setRotPos(self, device):
        cmd = self.devicecmds[device] + self.devices[device].posstring
        print (cmd)
        print (self.ZMQ.sendcommand(cmd))
        
        cmd = self.devicecmds[device] + self.devices[device].rotstring
        print (cmd)
        print (self.ZMQ.sendcommand(cmd))

    def setSlider(self, id, value):
        device = self.devices[self.currentDevice]
        device.setSlider(id, value)
        self.setRotPos(self.currentDevice)
        
    def resetSlider(self, id, value):
        device = self.devices[self.currentDevice]
        device.resetSlider(id, value)

    def initRotation(self, m):
        self.lefthandle.setRotation(m)
        self.righthandle.setRotation(m)
        self.HMD.setRotation(m)

    def setRotation(self, m):
        device = self.devices[self.currentDevice]
        device.setRotation(m)

    def changeRotation(self, m):
        device = self.devices[self.currentDevice]
        device.setRotation(m)