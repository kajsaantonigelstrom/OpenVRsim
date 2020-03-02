import sys
import os
import wx
from mainwindow import MainWindow
from controller import Controller
    
def main():
    controller = Controller()
    app = wx.App(False)
    frame = MainWindow(None, controller)
    frame.Show()
    app.MainLoop()    


if __name__ == '__main__':
    main()
