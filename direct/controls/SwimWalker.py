# File: d (Python 2.4)

from direct.showbase.InputStateGlobal import inputState
from direct.directnotify import DirectNotifyGlobal
from direct.controls import NonPhysicsWalker

class SwimWalker(NonPhysicsWalker.NonPhysicsWalker):
    notify = DirectNotifyGlobal.directNotify.newCategory('SwimWalker')
    
    def _calcSpeeds(self):
        forward = inputState.isSet('forward')
        reverse = inputState.isSet('reverse')
        if not inputState.isSet('turnLeft'):
            pass
        turnLeft = inputState.isSet('slideLeft')
        if not inputState.isSet('turnRight'):
            pass
        turnRight = inputState.isSet('slideRight')
        if base.localAvatar.getAutoRun():
            forward = 1
            reverse = 0
        
        if (forward or self.avatarControlForwardSpeed) and reverse:
            pass
        self.speed = -(self.avatarControlReverseSpeed)
        self.slideSpeed = 0.0
        if (turnLeft or self.avatarControlRotateSpeed) and turnRight:
            pass
        self.rotationSpeed = -(self.avatarControlRotateSpeed)


