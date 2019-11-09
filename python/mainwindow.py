import wx
import sys
import zmqsocket
class MainWindow(wx.Frame):

    def __init__(self, parent):
        super(MainWindow, self).__init__(parent, title="hej", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP, size=(650,650))

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
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)

        self.ls = wx.Button(panel, label="Left System")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.LeftSystem, self.ls)
        hbox.Add(self.ls, 0);

        self.rs = wx.Button(panel, label="Right System")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.RightSystem, self.rs)
        hbox.Add(self.rs, 5);

        vbox.Add((15, 15))
        vbox.Add(hbox, flag=wx.ALIGN_CENTER)

        panel.SetSizer(vbox)
        
    def menuhandler(self, event):
        id = event.GetId();
        if (id == 101):
            sys.exit();
        self.updateUI()

    # Methods bound to the buttons:
    def SelectJobFolder(self, event):
        dlg = wx.DirDialog (None, "Choose input directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dlg.SetPath(self.monitor.jobfolder)
        if dlg.ShowModal() == wx.ID_OK:    
            self.monitor.SetJobFolder(dlg.GetPath())
            self.jobfolder_txt.SetValue(self.monitor.jobfolder);

    def SelectBrainFolder(self, event):
        dlg = wx.DirDialog (None, "Choose input directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        dlg.SetPath(self.monitor.braintopfolder)
        if dlg.ShowModal() == wx.ID_OK:    
            self.monitor.SetBrainsFolder(dlg.GetPath())
            self.brainsfolder_txt.SetValue(self.monitor.braintopfolder);

    def LeftSystem(self, event):
        cmd = "1 s"
        print cmd
        print self.ZMQ.sendcommand(cmd);

    def RightSystem(self, event):
        cmd = "2 s"
        print cmd
        print self.ZMQ.sendcommand(cmd);
        




