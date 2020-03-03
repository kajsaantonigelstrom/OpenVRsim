import wx
import sys
import zmq
class ZMQsocket():

    def __init__(self):
        self.connect()

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        res = self.socket.connect("tcp://localhost:5577")
        print ("res ", res)
        if (res != None):
            print ("connected");
            self.connected = True;
        else:
            print ("Connect failed");
            self.connected = False;

    def checkstring(self, str):
        #if isinstance(str, unicode):
        return str.encode("ascii")
        #return str

    def sendcommand(self, cmd):
        cmd = self.checkstring(cmd) # Convert to ASCII if unicode
        if (not self.connected):
            self.connect()
        if (not self.connected):
            return "NOT CONNECTED"
        self.socket.send(cmd)
        answer = self.socket.recv()
        print ("received", answer)
        return answer
        