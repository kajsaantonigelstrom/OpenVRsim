import zmq
class ZMQsocket():

    def __init__(self):
        self.connect()

    def connect(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        res = self.socket.connect("tcp://localhost:5577")
        print ("res ", res)
        res = 0;
        if (res == 0):
            print ("connected");
            self.connected = True;
        else:
            print ("Connect failed");
            self.connected = False;

    def sendcommand(self, cmd):
        if (not self.connected):
            self.connect()
        if (not self.connected):
            return "NOT CONNECTED"
        self.socket.send(cmd)
        answer = self.socket.recv()
        print ("received", answer)
        return answer
        