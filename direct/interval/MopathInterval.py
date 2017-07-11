# File: d (Python 2.4)

__all__ = [
    'MopathInterval']
import LerpInterval
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import *

class MopathInterval(LerpInterval.LerpFunctionInterval):
    mopathNum = 1
    notify = directNotify.newCategory('MopathInterval')
    
    def __init__(self, mopath, node, fromT = 0, toT = None, duration = None, blendType = 'noBlend', name = None):
        if toT == None:
            toT = mopath.getMaxT()
        
        if duration == None:
            duration = abs(toT - fromT)
        
        if name == None:
            name = 'Mopath-%d' % MopathInterval.mopathNum
            MopathInterval.mopathNum += 1
        
        LerpInterval.LerpFunctionInterval.__init__(self, self._MopathInterval__doMopath, fromData = fromT, toData = toT, duration = duration, blendType = blendType, name = name)
        self.mopath = mopath
        self.node = node

    
    def destroy(self):
        self.function = None

    
    def _MopathInterval__doMopath(self, t):
        self.mopath.goTo(self.node, t)


