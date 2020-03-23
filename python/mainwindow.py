import wx
import sys
from cubecanvas import CubeCanvas
class MainWindow(wx.Frame):

    def __init__(self, parent, controller):
        super(MainWindow, self).__init__(parent, title="hej", style=wx.DEFAULT_FRAME_STYLE | wx.STAY_ON_TOP, size=(550,550))
        self.controller = controller
        
        menubar = wx.MenuBar()
        file = wx.Menu()
        file.Append(101, '&Quit', 'Quit')

        menubar.Append(file, '&File')
        self.SetMenuBar(menubar)
        menubar.Bind(wx.EVT_MENU, self.menuhandler) 
        self.SetTitle('OpenVR simulator')
        
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.updateUItimer, self.timer)
        self.timer.Start(100)

        self.InitUI()
        self.Centre()
        self.counter = 1;
        
    def updateUItimer(self, event=None):
        if self.buttonButtonState:
            x,y = wx.GetMousePosition()
            self.cubecanvas.rotateCanvas(x, y)

    def InitUI(self):
        # Main window controls
        panel = wx.Panel(self)
        mainbox = wx.BoxSizer(wx.VERTICAL)
        
        # HMR
        line1a = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Head: ")
        line1a.Add(15,15)
        line1a.Add(x,5)
        mainbox.Add(line1a, flag=wx.Left);

        # HMR pos/rot
        line1b = wx.BoxSizer(wx.HORIZONTAL)
        pos = wx.StaticText(panel, label="Pos (x y z): ")
        rot = wx.StaticText(panel, label="Rot (w x y z): ")
        self.headpos = wx.TextCtrl(panel)
        self.headpos.SetValue(self.controller.HMD.posstring);
        self.headrot = wx.TextCtrl(panel)
        self.headrot.SetValue(self.controller.HMD.rotstring);
        line1b.Add(15,15)
        line1b.Add(pos,0)
        line1b.Add(self.headpos)
        line1b.Add(15,15)
        line1b.Add(rot,0)
        line1b.Add(self.headrot)
        mainbox.Add(line1b, flag=wx.Left);
        mainbox.Add((15, 15))

        # HMR Send button
        line1b.Add(15,15)
        self.hpos = wx.Button(panel, label="Send")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.sendHeadRotPos, self.hpos)
        line1b.Add(self.hpos, 0);

        # Left Tracker
        line2a = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Left: ")
        line2a.Add(15,15)
        line2a.Add(x,5)
        mainbox.Add(line2a, flag=wx.Left);

        # Left Tracker pos/rot
        line2b = wx.BoxSizer(wx.HORIZONTAL)
        pos = wx.StaticText(panel, label="Pos (x y z): ")
        rot = wx.StaticText(panel, label="Rot (w x y z): ")
        self.leftpos = wx.TextCtrl(panel)
        self.leftpos.SetValue(self.controller.lefthandle.posstring);
        self.leftrot = wx.TextCtrl(panel)
        self.leftrot.SetValue(self.controller.lefthandle.rotstring);
        line2b.Add(15,15)
        line2b.Add(pos,0)
        line2b.Add(self.leftpos)
        line2b.Add(15,15)
        line2b.Add(rot,0)
        line2b.Add(self.leftrot)
       
        # Left tracker Send button
        line2b.Add(15,15)
        self.lpos = wx.Button(panel, label="Send")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.sendLeftRotPos, self.lpos)
        line2b.Add(self.lpos, 0);

        mainbox.Add(line2b, flag=wx.Left);        
        mainbox.Add((15, 15))

        # Right Tracker
        line3a = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Right: ")
        line3a.Add(15,15)
        line3a.Add(x,5)
        mainbox.Add(line3a, flag=wx.Left);

        # Right Tracker pos/rot
        line3b = wx.BoxSizer(wx.HORIZONTAL)
        pos = wx.StaticText(panel, label="Pos (x y z): ")
        rot = wx.StaticText(panel, label="Rot (w x y z): ")
        self.rightpos = wx.TextCtrl(panel)
        self.rightpos.SetValue(self.controller.righthandle.posstring);
        self.rightrot = wx.TextCtrl(panel)
        self.rightrot.SetValue(self.controller.righthandle.rotstring);

        line3b.Add(15,15)
        line3b.Add(pos,0)
        line3b.Add(self.rightpos)
        line3b.Add(15,15)
        line3b.Add(rot,0)
        line3b.Add(self.rightrot)
        mainbox.Add(line3b, flag=wx.Left);
        mainbox.Add((15, 15))
        # Right tracker Send button
        line3b.Add(15,15)
        self.rpos = wx.Button(panel, label="Send")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.sendRightRotPos, self.rpos)
        line3b.Add(self.rpos, 0);

        # Tracker Buttons
        TSright = wx.BoxSizer(wx.HORIZONTAL)
        TSright.Add(15,15)
        # System button S/L grip G/H app:F/J trig:D/K
        self.buttonButtonButton = wx.Button(panel, label="Click this button for controller input\ns/l=sys d/k=trackpad f/j=app g/h=grip")#, pos=(200, 325))
        self.Bind(wx.EVT_BUTTON, self.buttonButton, self.buttonButtonButton)
        self.buttonButtonButton.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
        self.buttonButtonButton.Bind(wx.EVT_KEY_UP, self.onKeyUp)
        self.buttonButtonButton.Bind(wx.EVT_KILL_FOCUS, self.killFocus)
        self.changeButtonState(False)
        TSright.Add(self.buttonButtonButton, 5);

        mainbox.Add(TSright, flag=wx.Left)
        mainbox.Add((15, 15))

        rotposbox = wx.BoxSizer(wx.HORIZONTAL) # canvas and sliders
        rotbox = wx.BoxSizer(wx.VERTICAL) # canvas/xy-buttons
        rotbuttonsbox = wx.BoxSizer(wx.HORIZONTAL) # xy-buttons
        rotbuttonsbox.Add(15,15)
        xy = wx.Button(panel, id=0, label="xy",style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.resetxyz, xy)
        rotbuttonsbox.Add(xy,1)
        xz = wx.Button(panel, id=1, label="xz", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.resetxyz, xz)
        rotbuttonsbox.Add(xz)
        yz = wx.Button(panel, id=2, label="yz", style=wx.BU_EXACTFIT)
        self.Bind(wx.EVT_BUTTON, self.resetxyz, yz)
        rotbuttonsbox.Add(yz)
        rotbox.Add(rotbuttonsbox)

        # canvas
        self.cubecanvas = CubeCanvas(panel, self.controller, self)
        self.cubecanvas.SetMinSize((130, 130))
        rotbox.Add(self.cubecanvas, 0, wx.ALIGN_BOTTOM|wx.ALL, 15)
        sliderh = 35
        rotposbox.Add(rotbox)

        sliderbox = wx.BoxSizer(wx.VERTICAL)
        sliderbox.Add(15,30)
        xbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="X: ")
        xbox.Add(x, 5);
        self.sliderX = wx.Slider(panel, 0,50,0,100,wx.DefaultPosition, wx.Size(300,sliderh));
        self.sliderX.Bind(wx.EVT_SLIDER, self.onSlider)
        xbox.Add(self.sliderX, flag=wx.Right);
        sliderbox.Add(xbox);

        ybox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Y: ")
        ybox.Add(x, 5);
        self.sliderY = wx.Slider(panel, 1,50,0,100,wx.DefaultPosition, wx.Size(300,sliderh));
        self.sliderY.Bind(wx.EVT_SLIDER, self.onSlider)
        ybox.Add(self.sliderY, flag=wx.Right);
        sliderbox.Add(ybox);

        zbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="Z: ")
        zbox.Add(x, 5);
        self.sliderZ = wx.Slider(panel, 2,50,0,100,wx.DefaultPosition, wx.Size(300,sliderh));
        self.sliderZ.Bind(wx.EVT_SLIDER, self.onSlider)
        zbox.Add(self.sliderZ, flag=wx.Right);
        sliderbox.Add(zbox);

        pbox = wx.BoxSizer(wx.HORIZONTAL)
        x = wx.StaticText(panel, label="P: ")
        pbox.Add(x, 5);
        self.sliderP = wx.Slider(panel,3,50,0,100,wx.DefaultPosition, wx.Size(300,sliderh));
        self.sliderP.Bind(wx.EVT_SLIDER, self.onSlider)
        pbox.Add(self.sliderP, flag=wx.Right);
        sliderbox.Add(pbox);

       
        rotposbox.Add(sliderbox, flag = wx.Right)
        rotposbox.Add(15,15)
        mainbox.Add(rotposbox, flag=wx.Left)

        radiobox = wx.BoxSizer(wx.HORIZONTAL)
        self.selector = wx.RadioBox(panel, wx.ID_ANY, style = wx.RA_SPECIFY_COLS, choices = ["Head", "Left", "Right"])
        self.selector.Bind(wx.EVT_RADIOBOX,self.onRadioBox)
        radiobox.Add(120,10);
        radiobox.Add(self.selector, flag=wx.Right);
        mainbox.Add(radiobox, flag=wx.Right);

        panel.SetSizer(mainbox)

        self.controller.selectedDevice = 0;
        
    def onKeyDown(self, evt):
        self.controller.KeyEvent(True, evt.GetKeyCode())
#        evt.Skip()
    
    def onKeyUp(self, evt):
        self.controller.KeyEvent(False, evt.GetKeyCode())
#        evt.Skip()
    
    def setStringsFrom_UI(self):
        self.controller.HMD.setposstring(self.headpos.GetLineText(0))
        self.controller.HMD.setrotstring(self.headrot.GetLineText(0))
        self.controller.lefthandle.setposstring(self.leftpos.GetLineText(0))
        self.controller.lefthandle.setrotstring(self.leftrot.GetLineText(0))
        self.controller.righthandle.setposstring(self.rightpos.GetLineText(0))
        self.controller.righthandle.setrotstring(self.rightrot.GetLineText(0))

    def setUI_FromStrings(self):
        self.headpos.SetValue(self.controller.HMD.posstring)
        self.headrot.SetValue(self.controller.HMD.rotstring)
        self.leftpos.SetValue(self.controller.lefthandle.posstring)
        self.leftrot.SetValue(self.controller.lefthandle.rotstring)
        self.rightpos.SetValue(self.controller.righthandle.posstring)
        self.rightrot.SetValue(self.controller.righthandle.rotstring)
    
    def canvasIsUpdated(self):  
        self.setUI_FromStrings()

    def updateUI(self):
        self.cubecanvas.update()
        self.cubecanvas.update() # for some unknown reason, two updates are necessary
        self.setUI_FromStrings()


    def onRadioBox(self, event):
        rb = event.GetEventObject() 
        self.controller.setSelectedDevice(rb.GetSelection())
        self.updateUI()

    def menuhandler(self, event):
        id = event.GetId();
        if (id == 101):
            sys.exit();
        self.updateUI()

    def sendHeadRotPos(self, event):
        self.setStringsFrom_UI()
        self.controller.sendRotPos(0)
        self.updateUI()

    def sendLeftRotPos(self, event):
        self.setStringsFrom_UI()
        self.controller.sendRotPos(1)
        self.updateUI()

    def sendRightRotPos(self, event):
        self.setStringsFrom_UI()
        self.controller.sendRotPos(2)
        self.updateUI()

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
        
    def resetxyz(self, event):
        id = event.GetId();
        self.controller.resetxyz(id)
        self.updateUI()
        return

    def buttonButton(self, event):
        self.changeButtonState(not self.buttonButtonState)
        if (self.buttonButtonState):
            x, y = wx.GetMousePosition()
            self.cubecanvas.rotateCanvasStart(x, y)

    
    def killFocus(self, event):
        self.changeButtonState(False)

    def changeButtonState(self, onoff):
        if (onoff):
            self.buttonButtonState = True
            self.buttonButtonButton.SetBackgroundColour(wx.Colour(0, 250, 0))
        else:
            self.buttonButtonState = False
            self.buttonButtonButton.SetBackgroundColour(wx.Colour(160, 160, 160))
