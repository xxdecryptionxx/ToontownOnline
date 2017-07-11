# File: d (Python 2.4)

from direct.gui.DirectGui import *
from pandac.PandaModules import *

class DirectCheckBox(DirectButton):
    
    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGButton, None), ('numStates', 4, None), ('state', DGG.NORMAL, None), ('relief', DGG.RAISED, None), ('invertedFrames', (1,), None), ('command', None, None), ('extraArgs', [], None), ('commandButtons', (DGG.LMB,), self.setCommandButtons), ('rolloverSound', DGG.getDefaultRolloverSound(), self.setRolloverSound), ('clickSound', DGG.getDefaultClickSound(), self.setClickSound), ('pressEffect', 1, DGG.INITOPT), ('uncheckedImage', None, None), ('checkedImage', None, None), ('isChecked', False, None))
        self.defineoptions(kw, optiondefs)
        DirectButton.__init__(self, parent)
        self.initialiseoptions(DirectCheckBox)

    
    def commandFunc(self, event):
        self['isChecked'] = not self['isChecked']
        if self['isChecked']:
            self['image'] = self['checkedImage']
        else:
            self['image'] = self['uncheckedImage']
        self.setImage()
        if self['command']:
            apply(self['command'], [
                self['isChecked']] + self['extraArgs'])
        


