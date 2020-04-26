import os
import wx
import zmqsocket
import ntpath
from pose import Pose
from pose import PoseEye
from pyquaternion import Quaternion
from testcasereader import TestCaseReader
from util import base_splitstring

class Controller():
    def __init__(self):
        self.lefthandle = Pose("Left")
        self.righthandle = Pose("Right")
        self.HMD = Pose("HMD")
        self.eyehandle = PoseEye("Eye")
        self.currentDevice = 0
        self.systemcmds = ["", "Ls", "Rs"]
        self.triggercmds = ["", "Lt", "Rt"]
        self.devicecmds = ["H ", "L ", "R ", "E "]
        self.devices = [ self.HMD, self.lefthandle, self.righthandle, self.eyehandle ] ## order corresponds to currendDevie
        self.ZMQhmd = zmqsocket.ZMQsocket(5577)
        self.ZMQeye = zmqsocket.ZMQsocket(5555)
        self.testcaseinprogress = False
        # System button S/L grip G/H app:F/J trig:D/K
        self.allowedKeysLeft = "SDFG";
        self.allowedKeysRight = "LKJH"
        self.lastcmd = ""
        self.statusstring = "No Test Case Loaded"

    def setSelectedDevice(self, dev):
        self.currentDevice = dev

    def sendAndRcvEye(self, cmd):
        #print ("eye " + cmd) ## for debug
        #return
        answer = self.ZMQeye.sendcommand(cmd)
        if (answer.lower() != "ok"):
            print (cmd,"answer is:", answer)

    def sendAndRcv(self, cmd):
        #print (cmd) ## for debug
        #return

        answer = self.ZMQhmd.sendcommand(cmd)
        if (answer.lower() != "ok"):
            print (cmd,"answer is:", answer)
    
    def sendEyeDirection(self, directionstring):
        if (self.testcaseinprogress):
            return
        cmd = "E D " +  directionstring;
        self.sendAndRcvEye(cmd)

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

    def setEyeDir(self, posx, posy):
        self.eyehandle.setDir(posx, posy)
        self.sendEyeDirection(self.eyehandle.posstring)


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
        self.stopTest()
        self.loadTestCase(folder)
        self.testcaseinprogress = True
        cmd = "G T r"
        self.sendAndRcv(cmd)
        self.sendAndRcvEye(cmd)

    def stopTest(self):
        self.testcaseinprogress = False
        cmd = "G T e"
        self.sendAndRcv(cmd)
        self.sendAndRcvEye(cmd)

    def loadTestCase(self, folder):
        self.statusstring = ""
        readers = []
        readers.append(TestCaseReader(folder+"\\HMD.csv"))
        readers.append(TestCaseReader(folder+"\\Left.csv"))
        readers.append(TestCaseReader(folder+"\\Right.csv"))
        readers.append(TestCaseReader(folder+"\\Eye.csv"))
        for i in range(0,4):
            if readers[i].error != "":
                self.statusstring = readers[i].filename + " " + readers[i].error
                return
        
        # clear previous test case
        cmd = "G T c"
        self.sendAndRcv(cmd)
        self.sendAndRcvEye(cmd)

        # Send test data to HDM/L/R
        for i in range(0,3):
            print (readers[i].filename, readers[i].size())
            if readers[i].size() > 0:
                for j in range(0, readers[i].size()):
                    cmd =  self.devicecmds[i] + "T " + readers[i].data[j]
                    self.sendAndRcv(cmd)
                self.statusstring = self.statusstring + " " + readers[i].tellfilename()
        # Send test data to Eye dll
        if (len(readers) == 4):
            print (readers[3].filename, readers[3].size())
            if readers[3].size() > 0:
                for j in range(0, readers[3].size()):
                    cmd =  "E T " + readers[3].data[j]
                    self.sendAndRcvEye(cmd)
                self.statusstring = self.statusstring + " " + readers[3].tellfilename()

        if (self.statusstring == ""):
            self.statusstring = "No Files Found"
        else:
            self.statusstring = "Loaded: " + folder + " " + self.statusstring

    def checkfileexists(self, filename):
        try:
            f = open(filename, "r")
            f.close()
            return 1
        except:
            return 0 #ok
    def generateTestCase(self, folder):
#        head, tail = ntpath.split(folder)
        try:
            os.makedirs(folder)
        except:
            pass
        print ("generate on ", folder)
        hmdfile = folder+"\\HMD.csv"
        lfile = folder+"\\Left.csv"
        rfile = folder+"\\Right.csv"
        eyefile = folder+"\\Eye.csv"
        
        # Check if the files exist to preven accidently overwrite
        existingfiles = 0
        existingfiles = existingfiles + self.checkfileexists(hmdfile)
        existingfiles = existingfiles + self.checkfileexists(lfile)
        existingfiles = existingfiles + self.checkfileexists(rfile)
        existingfiles = existingfiles + self.checkfileexists(eyefile)
        if existingfiles > 0:
            # At least one file exists, ask the user
            dial = wx.MessageDialog(None, 'The Test Case already exists and will be overwritten. Go one?', 'WARNING!!!',
            wx.YES_NO | wx.NO_DEFAULT | wx.ICON_QUESTION)
            if dial.ShowModal() != wx.ID_YES:
                return

        try:
            os.remove(hmdfile)
        except:
            pass
        try:
            os.remove(lfile)
        except:
            pass
        try: 
            os.remove(rfile)
        except:
            pass
        try: 
            os.remove(eyefile)
        except:
            pass
        self.writetestcase(hmdfile, self.HMD)
        self.writetestcase(lfile, self.lefthandle)
        self.writetestcase(rfile, self.righthandle)
        self.writetestcase(eyefile, self.eyehandle)

    def writetestcase(self, filename, device):
        f = open(filename, "w")
        datastring = device.getTabbedData()
        f.write("0.0\t" + datastring + "\n")
        f.close()

    def addToTestCase(self, folder, incr):
        hmdfile = folder+"\\HMD.csv"
        lfile = folder+"\\Left.csv"
        rfile = folder+"\\Right.csv"
        eyefile = folder+"\\Eye.csv"

        # First get last time in the test Case
        try:
            f = open(hmdfile, "r")
        except:
            print (hmdfile,"does not exist")
            return
        contents = f.readlines()
        f.close()
        lastline = contents[len(contents)-1]
        res = base_splitstring(lastline,"\t")
        time = 0.0
        if (len(res) > 0):
            time = float(res[0])
        time = time + incr

        self.writetestcasesample(hmdfile, self.HMD, time)
        self.writetestcasesample(lfile, self.lefthandle, time)
        self.writetestcasesample(rfile, self.righthandle, time)
        self.writetestcasesample(eyefile, self.eyehandle, time)

    def writetestcasesample(self, filename, device, time):
        tstr = "{:.3f}".format(time)
        f = open(filename, "a")
        datastring = device.getTabbedData()
        f.write(tstr + "\t" + datastring + "\n")
        f.close()
