import wx
class EyeCanvas(wx.Panel):
    def __init__(self, parent, controller, mywindow):
        super(EyeCanvas, self).__init__(parent)
        self.controller = controller
        self.mywindow = mywindow
        self.SetBackgroundStyle(wx.BG_STYLE_CUSTOM)
        self.Bind(wx.EVT_SIZE, self.on_size)
        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)
        # deviation from 'looking straight'; -1 to +1
        self.xpos = 0.0
        self.ypos = 0.0
    def on_size(self, event):
        event.Skip()
        self.Refresh()

    def setpos(self, axis, pos):
        if (axis == 0):
            self.xpos = pos
        else:
            self.ypos = pos
        self.setEyeDir(self.xpos, self.ypos)

    def setEyeDir(self, x, y):
        self.xpos = x
        self.ypos = y
        self.controller.setEyeDir(self.xpos, self.ypos)
        # redraw canval
        wx.QueueEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))
        # update sliders
        self.mywindow.eyeCanvasIsUpdated(self.xpos, -self.ypos)

    def on_paint(self, event):
        w, h = self.GetClientSize()
        dc = wx.ClientDC(self)
        dc.Clear()
        dc.SetPen(wx.Pen(wx.Colour(128,128,128), 5, wx.SOLID))
        dc.SetBrush(wx.Brush(wx.Colour(128,128,128), wx.SOLID))
        dc.DrawRectangle(0,0,w,h)
        dc.SetPen(wx.Pen(wx.BLACK, 5))
        xpospix = w/2 + self.xpos * w/2;
        ypospix = h/2 + self.ypos * h/2
        dc.DrawCircle(xpospix, ypospix, 2)
        
    def OnMouseDown(self, evt):
        self.CaptureMouse()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            w, h = self.GetClientSize()
            xpospix, ypospix = evt.GetPosition()
            xpos = 2 * (xpospix-w/2)/w;
            ypos = 2 * (ypospix-h/2)/(h)
            print ("dir: ", xpos, ypos, xpospix, ypospix)
            self.setEyeDir(xpos, ypos)
 