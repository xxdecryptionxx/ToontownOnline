# File: d (Python 2.4)

__all__ = [
    'taskMgr']
from Tkinter import *
from direct.task.TaskManagerGlobal import *
from direct.task.Task import Task
import Pmw
import sys
if '_Pmw' in sys.modules:
    sys.modules['_Pmw'].__name__ = '_Pmw'

__builtins__['tkroot'] = Pmw.initialise()

def tkLoop(self):
    while tkinter.dooneevent(tkinter.ALL_EVENTS | tkinter.DONT_WAIT):
        pass
    return Task.cont


def spawnTkLoop():
    taskMgr.add(tkLoop, 'tkLoop')

taskMgr.remove('tkLoop')
spawnTkLoop()
