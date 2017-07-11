# File: d (Python 2.4)

import wx
from direct.task.Task import Task

def wxLoop(self):
    while base.wxApp.Pending():
        base.wxApp.Dispatch()
    return Task.cont


def spawnWxLoop():
    if not getattr(base, 'wxApp', None):
        base.wxApp = wx.App(False)
    
    taskMgr.add(wxLoop, 'wxLoop')

