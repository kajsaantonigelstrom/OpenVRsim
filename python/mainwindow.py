import wx
import sys
import zmqsocket
class MainWindow(wx.Frame):

    def __init__(self, parent):
        super(MainWindow, self).__init__(parent, title="hej", size=(650,650))

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

        # Buttons for queue/finished
        vbox.Add((-1, 5))
        jobsizer = wx.BoxSizer(wx.HORIZONTAL)
        self.queue_clear = wx.Button(panel, label="Clear")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.ClearQueue, self.queue_clear)
        jobsizer.Add(self.queue_clear, 0);

        vbox.Add(jobsizer, flag=wx.LEFT|wx.RIGHT|wx.EXPAND, border=10)

    def menuhandler(self, event):
        id = event.GetId();
        if (id == 101):
            sys.exit();
        elif id == 102:
            #self.SelectTestDataFolder(event)
            HandleRecipesDialog(self, "Handle Recipes", self.monitor).ShowModal();
        elif id == 103:
            GenerateJobsDialog(self, "Generate Jobs", self.monitor).ShowModal();
        elif id == 104:
            GenerateTestdataDialog(self, "Generate Test Brains", self.monitor).ShowModal();
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

    def ClearQueue(self, event):
        cmd = "hej" + str(self.counter);
        self.counter = self.counter + 1;
        print self.ZMQ.sendcommand(cmd);
        




