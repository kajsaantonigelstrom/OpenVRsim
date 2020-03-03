import wx
import sys
from cubecanvas import CubeCanvas
class MainWindow(wx.Frame):

    def __init__(self, parent, controller):
        super(MainWindow, self).__init__(parent, title="hej", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP, size=(550,520))
        self.controller = controller
        
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
        self.headpos = wx.TextCtrl(panel)
        self.headpos.SetValue(self.controller.HMD.posstring);
        self.headrot = wx.TextCtrl(panel)
        self.headrot.SetValue(self.controller.HMD.rotstring);
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
        self.Bind(wx.EVT_BUTTON, self.sendHeadRotPos, self.hpos)
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
        self.leftpos = wx.TextCtrl(panel)
        self.leftpos.SetValue(self.controller.lefthandle.posstring);
        self.leftrot = wx.TextCtrl(panel)
        self.leftrot.SetValue(self.controller.lefthandle.rotstring);
        hbox.Add(15,15)
        hbox.Add(pos,0)
        hbox.Add(self.leftpos)
        hbox.Add(15,15)
        hbox.Add(rot,0)
        hbox.Add(self.leftrot)
       
        # Left tracker Send button
        hbox.Add(15,15)
        self.lpos = wx.Button(panel, label="Send")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.sendLeftRotPos, self.lpos)
        hbox.Add(self.lpos, 0);

        vbox.Add(hbox, flag=wx.Left);        
        vbox.Add((15, 15))

        # Left Tracker Buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(15,15)
        self.lt = wx.Button(panel, label="Trigger")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.sendLeftTrigger, self.lt)
        hbox.Add(self.lt, 0);

        self.ls = wx.Button(panel, label="System")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.sendLeftSystem, self.ls)
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
        self.rightpos = wx.TextCtrl(panel)
        self.rightpos.SetValue(self.controller.righthandle.posstring);
        self.rightrot = wx.TextCtrl(panel)
        self.rightrot.SetValue(self.controller.righthandle.rotstring);

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
        self.Bind(wx.EVT_BUTTON, self.sendRightRotPos, self.rpos)
        hbox.Add(self.rpos, 0);

        # Right Tracker Buttons
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(15,15)
        self.rt = wx.Button(panel, label="Trigger")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.sendRightTrigger, self.rt)
        hbox.Add(self.rt, 0);

        self.rs = wx.Button(panel, label="System")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.sendRightSystem, self.rs)
        hbox.Add(self.rs, 5);

        vbox.Add(hbox, flag=wx.Left)
        vbox.Add((15, 15))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(15,15)

        # 3D control
        c = CubeCanvas(panel, self.controller)
        c.SetMinSize((130, 130))
        hbox.Add(c, 0, wx.ALIGN_BOTTOM|wx.ALL, 15)
        sliderh = 35
        sliderbox = wx.BoxSizer(wx.VERTICAL)
        sliderbox.Add((15, 15))

        xbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="X: ")
        xbox.Add(x, 5);
        self.sliderX = wx.Slider(panel, 0,50,0,100,wx.DefaultPosition, wx.Size(300,sliderh));
        self.sliderX.Bind(wx.EVT_SLIDER, self.onSlider)
        xbox.Add(self.sliderX, flag=wx.Right);
        sliderbox.Add(xbox);

        xbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Y: ")
        xbox.Add(x, 5);
        self.sliderY = wx.Slider(panel, 1,50,0,100,wx.DefaultPosition, wx.Size(300,sliderh));
        self.sliderY.Bind(wx.EVT_SLIDER, self.onSlider)
        xbox.Add(self.sliderY, flag=wx.Right);
        sliderbox.Add(xbox);

        xbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Z: ")
        xbox.Add(x, 5);
        self.sliderZ = wx.Slider(panel, 2,50,0,100,wx.DefaultPosition, wx.Size(300,sliderh));
        self.sliderZ.Bind(wx.EVT_SLIDER, self.onSlider)
        xbox.Add(self.sliderZ, flag=wx.Right);
        sliderbox.Add(xbox);

        xbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="P: ")
        xbox.Add(x, 5);
        self.sliderP = wx.Slider(panel,3,50,0,100,wx.DefaultPosition, wx.Size(300,sliderh));
        self.sliderP.Bind(wx.EVT_SLIDER, self.onSlider)
        xbox.Add(self.sliderP, flag=wx.Right);
        sliderbox.Add(xbox);

        xbox = wx.BoxSizer(wx.HORIZONTAL)
        self.selector = wx.RadioBox(panel, wx.ID_ANY, style = wx.RA_SPECIFY_COLS, choices = ["Head", "Left", "Right"])
        self.selector.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        xbox.Add(self.selector, flag=wx.Right);
        xbox.Add(20,10);
        self.controller.selectedDevice = 0;
        sliderbox.Add(xbox);  
        
        hbox.Add(sliderbox, flag = wx.Right)
        hbox.Add(15,15)
        vbox.Add(hbox, flag=wx.Left)
        panel.SetSizer(vbox)
    
    def setStringsFrom_UI(self):
        self.controller.HMD.posstring = self.headpos.GetLineText(0)
        self.controller.HMD.rotstring = self.headrot.GetLineText(0)
        self.controller.lefthandle.posstring = self.leftpos.GetLineText(0)
        self.controller.lefthandle.rotstring = self.leftrot.GetLineText(0)
        self.controller.righthandle.posstring = self.rightpos.GetLineText(0)
        self.controller.righthandle.rotstring = self.rightrot.GetLineText(0)

    def setUI_FromStrings(self):
        self.headpos.SetValue(self.controller.HMD.posstring)
        self.headrot.SetValue(self.controller.HMD.rotstring)
        self.leftpos.SetValue(self.controller.lefthandle.posstring)
        self.leftrot.SetValue(self.controller.lefthandle.rotstring)
        self.rightpos.SetValue(self.controller.righthandle.posstring)
        self.rightrot.SetValue(self.controller.righthandle.rotstring)
        
    def onRadioBox(self, event):
        rb = event.GetEventObject() 
        self.controller.setSelectedDevice(rb.GetSelection())

    def menuhandler(self, event):
        id = event.GetId();
        if (id == 101):
            sys.exit();
        self.updateUI()

    def sendLeftSystem(self, event):
        self.controller.sendSystem(1);

    def sendRightSystem(self, event):
        self.controller.sendSystem(2);
  
    def sendLeftTrigger(self, event):
        self.controller.sendTrigger(1)

    def sendRightTrigger(self, event):
        self.controller.sendTrigger(2)

    def sendHeadRotPos(self, event):
        self.setStringsFrom_UI()
        self.controller.sendRotPos(0)

    def sendLeftRotPos(self, event):
        self.setStringsFrom_UI()
        self.controller.sendRotPos(1)

    def sendRightRotPos(self, event):
        self.setStringsFrom_UI()
        self.controller.sendRotPos(2)

    def onSlider(self, event):
        obj = event.GetEventObject()
        value = obj.GetValue()
        id = obj.GetId()
        self.controller.setSlider(id, value)
        if value == 0 or value == 100:
            obj.SetValue(50)
            self.controller.resetSlider(id, 50)
        # Update UI with the new position
        self.setUI_FromStrings()
        

