import wx
from wx import glcanvas
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy
import math
import keyboard
from pyquaternion import Quaternion

def mfunc_altcol(col):
    if (col < 20):
        return 100
    return int(col / 2.0)
 
def mfunc_atan(y, x):
   if (x == 0.0 and y == 0.0):
       return 0.0;
   else:
       return math.atan2(y, x);

def mfunc_polar(azel, v):
    azel[0] = mfunc_atan(v[1], v[0]);
    azel[1] = mfunc_atan(v[2], math.hypot(v[0], v[1]));


def DrawLine(from_, to, rgb):
        glColor3ub(rgb[0], rgb[1], rgb[2])
        glBegin(GL_LINES);
        glVertex3f(from_[0], from_[1], from_[2]);
        glVertex3f(to[0], to[1], to[2]);
        glEnd();

def Draw3dcircle(origin, edge, r, rgb):
        # Set color
        glColor3ub(rgb[0], rgb[1], rgb[2])

        # Transform
        glPushMatrix();
        direction = [0.0,0,0]
        direction[0] = edge[0] - origin[0];
        direction[1] = edge[1] - origin[1];
        direction[2] = edge[2] - origin[2];
        azel = [0.0,0]
        mfunc_polar(azel, direction);
        azel[0] = azel[0] * 180 / math.pi
        azel[1] = azel[1] * 180 / math.pi

        # Translate and rotate
        glTranslated(edge[0], edge[1], edge[2]);
        glRotated(azel[0], 0, 0, 1);
        glRotated(-azel[1], 0, 1, 0);

        # Draw cone
        glBegin(GL_TRIANGLE_FAN);
        glVertex3d(0, 0, 0);
        #for (DOUBLE angle = 0.0f; angle <= 2 * M_PI; angle += M_PI / 10) {
        for angle in numpy.arange(0.0, 2*math.pi+0.3, math.pi/10):
            y = r * math.sin(angle);
            z = r * math.cos(angle);
            glVertex3d(0, y, z);
        glEnd();

        glPopMatrix();

def Draw3dcone(origin, edge, r, rgb):

        # Set color
        glColor3ub(rgb[0], rgb[1], rgb[2])

        glFrontFace(GL_CW);
    
        # Transform
        glPushMatrix();

        direction = [0.0,0,0]
        direction[0] = edge[0] - origin[0];
        direction[1] = edge[1] - origin[1];
        direction[2] = edge[2] - origin[2];
 
        azel = [0.0,0]
        mfunc_polar(azel, direction);
        azel[0] = azel[0] * 180 / math.pi
        azel[1] = azel[1] * 180 / math.pi

        #h = sqrt(pow(direction(0), 2) + pow(direction(1), 2) + pow(direction(2), 2));
        h = math.sqrt(direction[0]**2 + direction[1]**2 + direction[2]**2)

        # Translate and rotate
        glTranslated(edge[0], edge[1], edge[2]);
        glRotated(azel[0], 0, 0, 1);
        glRotated(-azel[1], 0, 1, 0);

        # Draw cone
        glBegin(GL_TRIANGLE_FAN);
        glVertex3d(0, 0, 0);
        #for(DOUBLE angle=0.0f;angle<=2*M_PI;angle+=M_PI/10) 
        for angle in numpy.arange(0.0, 2*math.pi+0.1, math.pi/10):
            y = r * math.sin(angle);
            z = r * math.cos(angle);
            glVertex3d(-h, y, z);
        glEnd();

        glPopMatrix();
 
        # Draw 'bottom'
        rgbalt = [0,0,0] # 'color that differs from rgb'
        rgbalt[0] = mfunc_altcol(rgb[0])
        rgbalt[1] = mfunc_altcol(rgb[1])
        rgbalt[2] = mfunc_altcol(rgb[2])

        Draw3dcircle(edge, origin, r, rgbalt);

class MyCanvasBase(glcanvas.GLCanvas):
    def __init__(self, parent):
        glcanvas.GLCanvas.__init__(self, parent, -1)
        self.init = False
        self.context = glcanvas.GLContext(self)
        
        # initial mouse position
        self.lastx = self.x = 30
        self.lasty = self.y = 30
        self.size = None
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnMouseDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMotion)

    def OnEraseBackground(self, event):
        pass # Do nothing, to avoid flashing on MSW.

    def OnSize(self, event):
        wx.CallAfter(self.DoSetViewport)
        event.Skip()

    def DoSetViewport(self):
        size = self.size = self.GetClientSize()
        self.SetCurrent(self.context)
        glViewport(0, 0, size.width, size.height)
        
    def OnPaint(self, event):
        dc = wx.ClientDC(self)
        self.SetCurrent(self.context)
        if not self.init:
            self.InitGL()
            self.init = True
        self.OnDraw()

    def OnMouseDown(self, evt):
        self.CaptureMouse()
        self.x, self.y = self.lastx, self.lasty = evt.GetPosition()

    def OnMouseUp(self, evt):
        self.ReleaseMouse()

    def OnMouseMotion(self, evt):
        if evt.Dragging() and evt.LeftIsDown():
            self.lastx, self.lasty = self.x, self.y
            self.x, self.y = evt.GetPosition()
            self.Refresh(True)

    def rotateCanvasStart(self, x, y):
            self.x = self.lastx = x
            self.y = self.lasty = y

    def rotateCanvas(self, x, y):
            self.lastx, self.lasty = self.x, self.y
            self.x = x
            self.y = y
            self.Refresh(True)

    def printmatrices(self, tag):
        m = numpy.eye(4)
        p = numpy.eye(4)
        glGetDoublev(GL_MODELVIEW_MATRIX, m);
        glGetDoublev(GL_PROJECTION_MATRIX, p);
        print(type(m))
        print ("m----------"+tag)
        print (m)
        #print ("p ----------"+tag)
        # print(p)
        try:
            q1 = Quaternion(matrix=m)
            print(str(q1))
        except:
            print("Qerror")#print(q1.rotation_matrix)
        #print(q1.transformation_matrix)

class CubeCanvas(MyCanvasBase):
    def __init__(self, parent, controller, mywindow):
        super().__init__(parent)
        self.controller = controller
        self.mywindow = mywindow
        self.currRotation = controller.getRotation()


    def InitGL(self):
        # set viewing projection
        glMatrixMode(GL_PROJECTION)
        glOrtho(-1.5, 1.5, -1.5, 1.5, -1, 3)
        glMatrixMode(GL_MODELVIEW)

        glEnable(GL_DEPTH_TEST)
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL);
        glDisable(GL_CULL_FACE);

        glColorMaterial(GL_FRONT,GL_DIFFUSE);
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE,1);  
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.5, 0.5, 0.5, 0);


    def update(self):
        self.currRotation = self.controller.getRotation()
        self.lastx = self.x
        self.lasty = self.y
        wx.QueueEvent(self.GetEventHandler(), wx.PyCommandEvent(wx.EVT_PAINT.typeId, self.GetId()))
        self.SwapBuffers()

    def OnDraw(self):
        # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClearColor(0.5, 0.5, 0.5, 0);

        DrawLine([-1.0, 0.0, 0.0], [1.0, 0.0, 0.0], [255,0,0])
        Draw3dcone([0.85, 0.0, 0], [1, 0.0, 0.0], 0.1, [255,0,0])
        DrawLine([0.0, -1.0, 0.0], [0.0, 1.0, 0.0], [0,255,0])
        Draw3dcone([0,0.85, 0.0], [0, 1, 0], 0.1, [0, 255, 0])
        DrawLine([0.0, 0.0, -1.0], [0.0, 0.0, 1.0], [0,0,255])
        Draw3dcone([0,0,0.85], [0, 0.0, 1.0], 0.1, [0,0,255])

        x = self.x - self.lastx;
        y = self.y - self.lasty;
        if (keyboard.is_pressed("shift")):
            # rotation round the z axis
            movement = Quaternion(axis=[0.0, 0.0, 1.0], degrees=y)
            self.currRotation = self.currRotation * movement
        else:
            xmovement = Quaternion(axis=[1.0, 0.0, 0.0], degrees=-y)
            ymovement = Quaternion(axis=[0.0, 1.0, 0.0], degrees=-x)
            self.currRotation = self.currRotation * xmovement * ymovement;

        glMatrixMode(GL_MODELVIEW);
        glLoadIdentity();
        glLoadMatrixd(self.currRotation.transformation_matrix);
        self.SwapBuffers()

            # update the controller
        if (x!=0 or y!=0):
            self.controller.setRotation(self.currRotation)
            self.mywindow.canvasIsUpdated()
        

    def DrawCube(self):
       # clear color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_QUADS)
        glNormal3f( 0.0, 0.0, 1.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5,-0.5, 0.5)
        glVertex3f( 0.5,-0.5, 0.5)

        glNormal3f( 0.0, 0.0,-1.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glVertex3f( 0.5, 0.5,-0.5)
        glVertex3f( 0.5,-0.5,-0.5)

        glNormal3f( 0.0, 1.0, 0.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f( 0.5, 0.5,-0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glVertex3f(-0.5, 0.5, 0.5)

        glNormal3f( 0.0,-1.0, 0.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f( 0.5,-0.5,-0.5)
        glVertex3f( 0.5,-0.5, 0.5)
        glVertex3f(-0.5,-0.5, 0.5)

        glNormal3f( 1.0, 0.0, 0.0)
        glVertex3f( 0.5, 0.5, 0.5)
        glVertex3f( 0.5,-0.5, 0.5)
        glVertex3f( 0.5,-0.5,-0.5)
        glVertex3f( 0.5, 0.5,-0.5)

        glNormal3f(-1.0, 0.0, 0.0)
        glVertex3f(-0.5,-0.5,-0.5)
        glVertex3f(-0.5,-0.5, 0.5)
        glVertex3f(-0.5, 0.5, 0.5)
        glVertex3f(-0.5, 0.5,-0.5)
        glEnd()

        self.SwapBuffers()


