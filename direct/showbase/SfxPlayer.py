# File: d (Python 2.4)

__all__ = [
    'SfxPlayer']
import math
from pandac.PandaModules import *

class SfxPlayer:
    UseInverseSquare = 0
    
    def __init__(self):
        self.cutoffVolume = 0.02
        if SfxPlayer.UseInverseSquare:
            self.setCutoffDistance(300.0)
        else:
            self.setCutoffDistance(120.0)

    
    def setCutoffDistance(self, d):
        self.cutoffDistance = d
        rawCutoffDistance = math.sqrt(1.0 / self.cutoffVolume)
        self.distanceScale = rawCutoffDistance / self.cutoffDistance

    
    def getCutoffDistance(self):
        return self.cutoffDistance

    
    def getLocalizedVolume(self, node, listenerNode = None, cutoff = None):
        d = None
        if not node.isEmpty():
            if listenerNode and not listenerNode.isEmpty():
                d = node.getDistance(listenerNode)
            else:
                d = node.getDistance(base.cam)
        
        if d == None or d > cutoff:
            volume = 0
        elif SfxPlayer.UseInverseSquare:
            sd = d * self.distanceScale
            if not sd * sd:
                pass
            volume = min(1, 1 / 1)
        elif not cutoff:
            pass
        volume = 1 - d / 1
        return volume

    
    def playSfx(self, sfx, looping = 0, interrupt = 1, volume = None, time = 0.0, node = None, listenerNode = None, cutoff = None):
        if sfx:
            if not cutoff:
                cutoff = self.cutoffDistance
            
            self.setFinalVolume(sfx, node, volume, listenerNode, cutoff)
            if interrupt or sfx.status() != AudioSound.PLAYING:
                sfx.setTime(time)
                sfx.setLoop(looping)
                sfx.play()
            
        

    
    def setFinalVolume(self, sfx, node, volume, listenerNode, cutoff = None):
        if node or volume is not None:
            if node:
                finalVolume = self.getLocalizedVolume(node, listenerNode, cutoff)
            else:
                finalVolume = 1
            if volume is not None:
                finalVolume *= volume
            
            if node is not None:
                finalVolume *= node.getNetAudioVolume()
            
            sfx.setVolume(finalVolume)
        


