import wx
import sys
import zmq
class ZMQsocket():

    def __init__(self):
        self.connect()

    def reset_my_socket(self):
        if (self.socket != None):
            self.socket.close()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt( zmq.RCVTIMEO, 500 ) # milliseconds
        self.socket.connect("tcp://localhost:5577")

    def connect(self):
        self.socket = None;
        self.context = zmq.Context()
        self.reset_my_socket()
 
    def checkstring(self, str):
        #if isinstance(str, unicode):
        return str.encode("ascii")
        #return str

    def sendcommand(self, cmd):
        cmd = self.checkstring(cmd) # Convert to ASCII if unicode
        self.socket.send(cmd)
        try:
            answer = self.socket.recv()
            print ("received", answer)
            return answer
        except zmq.Again as e:
            self.reset_my_socket()
            return "NOT CONNECTED"        