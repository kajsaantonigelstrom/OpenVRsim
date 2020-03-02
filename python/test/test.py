try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wx.glcanvas not present")

try:
    from OpenGL.GL import *
except ImportError:
    raise ImportError("Required dependency OpenGL not present")
 