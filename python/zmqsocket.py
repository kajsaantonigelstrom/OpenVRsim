import wx
import sys
import zmq
class ZMQsocket():

    def __init__(self, port):
        self.tcpstring = "tcp://localhost:" + str(port)
        print (self.tcpstring)
        self.connect()

    def reset_my_socket(self):
        if (self.socket != None):
            self.socket.close()
        self.socket = self.context.socket(zmq.REQ)
        self.socket.setsockopt( zmq.RCVTIMEO, 900 ) # milliseconds
        self.socket.connect(self.tcpstring)

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
        #print ("send ", cmd, self.tcpstring)
        #return "ok"
        self.socket.send(cmd)
        try:
            # answer is a binary string
            answer = self.socket.recv()
            result = answer.decode('ascii')
            return result
        except zmq.Again as e:
            self.reset_my_socket()
            return "NOT CONNECTED"        