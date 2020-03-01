import wx
import sys
import zmqsocket
class MainWindow(wx.Frame):

    def __init__(self, parent):
        super(MainWindow, self).__init__(parent, title="hej", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP, size=(550,350))

        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(101, '&Quit', 'Quit')

        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        menubar.Bind(wx.EVT_MENU, self.menuhandler) 
        self.SetTitle('OpenVR simulator')
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateUI, self.timer)
        self.timer.Start(2000)

        self.InitUI()
        self.Centre()
        self.counter = 1;
        self.ZMQ = zmqsocket.ZMQsocket()

    def updateUI(self, event=None):
        return

    def InitUI(self):
        # Main window controls
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # HMR
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Head: ")
        hbox.Add(15,15)
        hbox.Add(x,5)
        vbox.Add(hbox, flag=wx.Left);

        # HMR pos/rot
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        pos = wx.StaticText(panel, label="Pos (x y z): ")
        rot = wx.StaticText(panel, label="Rot (w x y z): ")
        self.headpos_str = "0 0 0"
        self.headpos = wx.TextCtrl(panel)
        self.headpos.SetValue(self.headpos_str);
        self.headrot = wx.TextCtrl(panel)
        self.headrot_str = "0 0 0 0"
        self.headrot.SetValue(self.headrot_str);
        hbox.Add(15,15)
        hbox.Add(pos,0)
        hbox.Add(self.headpos)
        hbox.Add(15,15)
        hbox.Add(rot,0)
        hbox.Add(self.headrot)
        vbox.Add(hbox, flag=wx.Left);
        vbox.Add((15, 15))

        # HMR Send button
        hbox.Add(15,15)
        self.hpos = wx.Button(panel, label="Send")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.Headpos, self.hpos)
        hbox.Add(self.hpos, 0);

        # Left Tracker
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Left: ")
        hbox.Add(15,15)
        hbox.Add(x,5)
        vbox.Add(hbox, flag=wx.Left);

        # Left Tracker pos/rot
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        pos = wx.StaticText(panel, label="Pos (x y z): ")
        rot = wx.StaticText(panel, label="Rot (w x y z): ")
        self.leftpos_str = "0 0 0"
        self.leftpos = wx.TextCtrl(panel)
        self.leftpos.SetValue(self.leftpos_str);
        self.leftrot = wx.TextCtrl(panel)
        self.leftrot_str = "0 0 0 0"
        self.leftrot.SetValue(self.leftrot_str);
        hbox.Add(15,15)
        hbox.Add(pos,0)
        hbox.Add(self.leftpos)
        hbox.Add(15,15)
        hbox.Add(rot,0)
        hbox.Add(self.leftrot)
       
        # Left tracker Send button
        hbox.Add(15,15)
        self.lpos = wx.Button(panel, label="Send")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.Leftpos, self.lpos)
        hbox.Add(self.lpos, 0);

        vbox.Add(hbox, flag=wx.Left);        
        vbox.Add((15, 15))

        # Left Tracker Buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(15,15)
        self.lt = wx.Button(panel, label="Trigger")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.LeftTrigger, self.lt)
        hbox.Add(self.lt, 0);

        self.ls = wx.Button(panel, label="System")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.LeftSystem, self.ls)
        hbox.Add(self.ls, 5);

        vbox.Add(hbox, flag=wx.Left)
        vbox.Add((15, 15))

        # Right Tracker
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Right: ")
        hbox.Add(15,15)
        hbox.Add(x,5)
        vbox.Add(hbox, flag=wx.Left);

        # Right Tracker pos/rot
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        pos = wx.StaticText(panel, label="Pos (x y z): ")
        rot = wx.StaticText(panel, label="Rot (w x y z): ")
        self.rightpos_str = "0 0 0"
        self.rightpos = wx.TextCtrl(panel)
        self.rightpos.SetValue(self.rightpos_str);
        self.rightrot = wx.TextCtrl(panel)
        self.rightrot_str = "0 0 0 0"
        self.rightrot.SetValue(self.rightrot_str);

        hbox.Add(15,15)
        hbox.Add(pos,0)
        hbox.Add(self.rightpos)
        hbox.Add(15,15)
        hbox.Add(rot,0)
        hbox.Add(self.rightrot)
        vbox.Add(hbox, flag=wx.Left);
        vbox.Add((15, 15))
        # Right tracker Send button
        hbox.Add(15,15)
        self.rpos = wx.Button(panel, label="Send")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.Rightpos, self.rpos)
        hbox.Add(self.rpos, 0);

        # Right Tracker Buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(15,15)
        self.rt = wx.Button(panel, label="Trig")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.RightTrigger, self.rt)
        hbox.Add(self.rt, 0);

        self.rs = wx.Button(panel, label="System")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.RightSystem, self.rs)
        hbox.Add(self.rs, 5);

        vbox.Add(hbox, flag=wx.Left)
        vbox.Add((15, 15))


        panel.SetSizer(vbox)
    
    def checkstring(self, str):
        print 1, type(str)
        if (type(str) is unicode):
            print 123
            return str.encode("ascii")
        return str

    def update_str(self):
        self.headpos_str = self.checkstring(self.headpos.GetLineText(0))
        self.headrot_str = self.checkstring(self.headrot.GetLineText(0))
        self.leftpos_str = self.checkstring(self.leftpos.GetLineText(0))
        self.leftrot_str = self.checkstring(self.leftrot.GetLineText(0))
        self.rightpos_str = self.checkstring(self.rightpos.GetLineText(0))
        self.rightrot_str = self.checkstring(self.rightrot.GetLineText(0))
        print self.headpos_str

    def menuhandler(self, event):
        id = event.GetId();
        if (id == 101):
            sys.exit();
        self.updateUI()

    def LeftSystem(self, event):
        cmd = "Ls"
        print cmd
        print self.ZMQ.sendcommand(cmd);

    def RightSystem(self, event):
        cmd = "Rs"
        print cmd
        print self.ZMQ.sendcommand(cmd);
  
    def LeftTrigger(self, event):
        cmd = "Lt"
        print cmd
        print self.ZMQ.sendcommand(cmd);

    def RightTrigger(self, event):
        cmd = "Rt"
        print cmd
        print self.ZMQ.sendcommand(cmd);

    def Headpos(self, event):
        self.update_str()
        cmd = "H " + self.headpos_str
        print cmd
        print self.ZMQ.sendcommand(cmd);
        
        cmd = "H " + self.headrot_str
        print cmd
        print self.ZMQ.sendcommand(cmd);

    def Leftpos(self, event):
        self.update_str()
        cmd = "L " + self.leftpos_str
        print cmd
        print self.ZMQ.sendcommand(cmd);
        
        cmd = "L " + self.leftrot_str
        print cmd
        print self.ZMQ.sendcommand(cmd);

    def Rightpos(self, event):
        self.update_str()
        cmd = "R " + self.rightpos_str
        print cmd
        print self.ZMQ.sendcommand(cmd);
        
        cmd = "R " + self.rightrot_str
        print cmd
        print self.ZMQ.sendcommand(cmd);



