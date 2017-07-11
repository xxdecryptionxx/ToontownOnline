# File: d (Python 2.4)

__all__ = [
    'ShadowPlacer']
from direct.controls.ControlManager import CollisionHandlerRayStart
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
import DirectObject

class ShadowPlacer(DirectObject.DirectObject):
    notify = DirectNotifyGlobal.directNotify.newCategory('ShadowPlacer')
    
    def __init__(self, cTrav, shadowNodePath, wallCollideMask, floorCollideMask):
        self.isActive = 0
        DirectObject.DirectObject.__init__(self)
        self.setup(cTrav, shadowNodePath, wallCollideMask, floorCollideMask)

    
    def setup(self, cTrav, shadowNodePath, wallCollideMask, floorCollideMask):
        if not cTrav:
            base.initShadowTrav()
            cTrav = base.shadowTrav
        
        self.cTrav = cTrav
        self.shadowNodePath = shadowNodePath
        floorOffset = 0.025000000000000001
        self.cRay = CollisionRay(0.0, 0.0, CollisionHandlerRayStart, 0.0, 0.0, -1.0)
        cRayNode = CollisionNode('shadowPlacer')
        cRayNode.addSolid(self.cRay)
        self.cRayNodePath = NodePath(cRayNode)
        self.cRayBitMask = floorCollideMask
        cRayNode.setFromCollideMask(self.cRayBitMask)
        cRayNode.setIntoCollideMask(BitMask32.allOff())
        self.lifter = CollisionHandlerFloor()
        self.lifter.setOffset(floorOffset)
        self.lifter.setReach(4.0)
        self.lifter.addCollider(self.cRayNodePath, shadowNodePath)

    
    def delete(self):
        self.off()
        del self.cTrav
        del self.shadowNodePath
        del self.cRay
        self.cRayNodePath.removeNode()
        del self.cRayNodePath
        del self.lifter

    
    def on(self):
        if self.isActive:
            return None
        
        self.cRayNodePath.reparentTo(self.shadowNodePath.getParent())
        self.cTrav.addCollider(self.cRayNodePath, self.lifter)
        self.isActive = 1

    
    def off(self):
        if not self.isActive:
            return None
        
        didIt = self.cTrav.removeCollider(self.cRayNodePath)
        self.oneTimeCollide()
        self.cRayNodePath.detachNode()
        self.isActive = 0

    
    def oneTimeCollide(self):
        tempCTrav = CollisionTraverser('oneTimeCollide')
        tempCTrav.addCollider(self.cRayNodePath, self.lifter)
        tempCTrav.traverse(render)

    
    def resetToOrigin(self):
        if self.shadowNodePath:
            self.shadowNodePath.setPos(0, 0, 0)
        


