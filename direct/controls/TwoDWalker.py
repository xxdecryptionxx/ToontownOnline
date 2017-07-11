# File: d (Python 2.4)

from GravityWalker import *

class TwoDWalker(GravityWalker):
    notify = directNotify.newCategory('TwoDWalker')
    wantDebugIndicator = base.config.GetBool('want-avatar-physics-indicator', 0)
    wantFloorSphere = base.config.GetBool('want-floor-sphere', 0)
    earlyEventSphere = base.config.GetBool('early-event-sphere', 0)
    
    def __init__(self, gravity = -32.173999999999999, standableGround = 0.70699999999999996, hardLandingForce = 16.0):
        self.notify.debug('Constructing TwoDWalker')
        GravityWalker.__init__(self)

    
    def handleAvatarControls(self, task):
        jump = inputState.isSet('forward')
        if self.lifter.isOnGround():
            if self.isAirborne:
                self.isAirborne = 0
                impact = self.lifter.getImpactVelocity()
                messenger.send('jumpLand')
            
            self.priorParent = Vec3.zero()
        elif self.isAirborne == 0:
            pass
        
        self.isAirborne = 1
        return Task.cont

    
    def jumpPressed(self):
        if self.lifter.isOnGround():
            if self.isAirborne == 0:
                if self.mayJump:
                    self.lifter.addVelocity(self.avatarControlJumpForce)
                    messenger.send('jumpStart')
                    self.isAirborne = 1
                
            
        


