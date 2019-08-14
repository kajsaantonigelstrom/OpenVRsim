import sys
import os
import wx
from mainwindow import MainWindow

def main():
    app = wx.App(False)
    frame = MainWindow(None)
    frame.Show()
    app.MainLoop()    


if __name__ == '__main__':
    main()
