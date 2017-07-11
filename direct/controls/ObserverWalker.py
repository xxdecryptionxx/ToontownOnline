# File: d (Python 2.4)

from direct.showbase.ShowBaseGlobal import *
from pandac.PandaModules import *
from direct.directnotify import DirectNotifyGlobal
import NonPhysicsWalker

class ObserverWalker(NonPhysicsWalker.NonPhysicsWalker):
    notify = DirectNotifyGlobal.directNotify.newCategory('ObserverWalker')
    slideName = 'jump'
    
    def initializeCollisions(self, collisionTraverser, avatarNodePath, avatarRadius = 1.3999999999999999, floorOffset = 1.0, reach = 1.0):
        self.cTrav = collisionTraverser
        self.avatarNodePath = avatarNodePath
        self.cSphere = CollisionSphere(0.0, 0.0, 0.0, avatarRadius)
        cSphereNode = CollisionNode('Observer.cSphereNode')
        cSphereNode.addSolid(self.cSphere)
        self.cSphereNodePath = avatarNodePath.attachNewNode(cSphereNode)
        cSphereNode.setFromCollideMask(self.cSphereBitMask)
        cSphereNode.setIntoCollideMask(BitMask32.allOff())
        self.pusher = CollisionHandlerPusher()
        self.pusher.setInPattern('enter%in')
        self.pusher.setOutPattern('exit%in')
        self.pusher.addCollider(self.cSphereNodePath, avatarNodePath)
        self.setCollisionsActive(1)
        
        class Foo:
            
            def hasContact(self):
                return 1


        self.lifter = Foo()

    
    def deleteCollisions(self):
        del self.cTrav
        del self.cSphere
        self.cSphereNodePath.removeNode()
        del self.cSphereNodePath
        del self.pusher

    
    def setCollisionsActive(self, active = 1):
        if self.collisionsActive != active:
            self.collisionsActive = active
            if active:
                self.cTrav.addCollider(self.cSphereNodePath, self.pusher)
            else:
                self.cTrav.removeCollider(self.cSphereNodePath)
                self.oneTimeCollide()
        

    
    def oneTimeCollide(self):
        tempCTrav = CollisionTraverser('oneTimeCollide')
        tempCTrav.addCollider(self.cSphereNodePath, self.pusher)
        tempCTrav.traverse(render)

    
    def enableAvatarControls(self):
        pass

    
    def disableAvatarControls(self):
        pass


