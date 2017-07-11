# File: d (Python 2.4)

__all__ = [
    'DirectSlider']
from pandac.PandaModules import *
import DirectGuiGlobals as DGG
from DirectFrame import *
from DirectButton import *

class DirectSlider(DirectFrame):
    
    def __init__(self, parent = None, **kw):
        optiondefs = (('pgFunc', PGSliderBar, None), ('state', DGG.NORMAL, None), ('frameColor', (0.59999999999999998, 0.59999999999999998, 0.59999999999999998, 1), None), ('range', (0, 1), self.setRange), ('value', 0, self._DirectSlider__setValue), ('scrollSize', 0.01, self.setScrollSize), ('pageSize', 0.10000000000000001, self.setPageSize), ('orientation', DGG.HORIZONTAL, self.setOrientation), ('command', None, None), ('extraArgs', [], None))
        if kw.get('orientation') == DGG.VERTICAL:
            optiondefs += (('frameSize', (-0.080000000000000002, 0.080000000000000002, -1, 1), None), ('frameVisibleScale', (0.25, 1), None))
        else:
            optiondefs += (('frameSize', (-1, 1, -0.080000000000000002, 0.080000000000000002), None), ('frameVisibleScale', (1, 0.25), None))
        self.defineoptions(kw, optiondefs)
        DirectFrame.__init__(self, parent)
        self.thumb = self.createcomponent('thumb', (), None, DirectButton, (self,), borderWidth = self['borderWidth'])
        if self.thumb['frameSize'] == None and self.thumb.bounds == [
            0.0,
            0.0,
            0.0,
            0.0]:
            f = self['frameSize']
            if self['orientation'] == DGG.HORIZONTAL:
                self.thumb['frameSize'] = (f[0] * 0.050000000000000003, f[1] * 0.050000000000000003, f[2], f[3])
            else:
                self.thumb['frameSize'] = (f[0], f[1], f[2] * 0.050000000000000003, f[3] * 0.050000000000000003)
        
        self.guiItem.setThumbButton(self.thumb.guiItem)
        self.bind(DGG.ADJUST, self.commandFunc)
        self.initialiseoptions(DirectSlider)

    
    def setRange(self):
        v = self['value']
        r = self['range']
        self.guiItem.setRange(r[0], r[1])
        self['value'] = v

    
    def _DirectSlider__setValue(self):
        self.guiItem.setValue(self['value'])

    
    def setValue(self, value):
        self['value'] = value

    
    def getValue(self):
        return self.guiItem.getValue()

    
    def getRatio(self):
        return self.guiItem.getRatio()

    
    def setScrollSize(self):
        self.guiItem.setScrollSize(self['scrollSize'])

    
    def setPageSize(self):
        self.guiItem.setPageSize(self['pageSize'])

    
    def setOrientation(self):
        if self['orientation'] == DGG.HORIZONTAL:
            self.guiItem.setAxis(Vec3(1, 0, 0))
        elif self['orientation'] == DGG.VERTICAL:
            self.guiItem.setAxis(Vec3(0, 0, 1))
        else:
            raise ValueError, 'Invalid value for orientation: %s' % self['orientation']

    
    def destroy(self):
        if hasattr(self, 'thumb'):
            self.thumb.destroy()
            del self.thumb
        
        DirectFrame.destroy(self)

    
    def commandFunc(self):
        self._optionInfo['value'][DGG._OPT_VALUE] = self.guiItem.getValue()
        if self['command']:
            apply(self['command'], self['extraArgs'])
        


