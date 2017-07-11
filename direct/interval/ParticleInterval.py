# File: d (Python 2.4)

__all__ = [
    'ParticleInterval']
from pandac.PandaModules import *
from direct.directnotify.DirectNotifyGlobal import directNotify
from Interval import Interval
from direct.particles import ParticleEffect

class ParticleInterval(Interval):
    particleNum = 1
    notify = directNotify.newCategory('ParticleInterval')
    
    def __init__(self, particleEffect, parent, worldRelative = 1, renderParent = None, duration = 0.0, softStopT = 0.0, cleanup = False, name = None):
        id = 'Particle-%d' % ParticleInterval.particleNum
        ParticleInterval.particleNum += 1
        if name == None:
            name = id
        
        self.particleEffect = particleEffect
        self.cleanup = cleanup
        if parent != None:
            self.particleEffect.reparentTo(parent)
        
        if worldRelative:
            renderParent = render
        
        if renderParent:
            for particles in self.particleEffect.getParticlesList():
                particles.setRenderParent(renderParent.node())
            
        
        self._ParticleInterval__softStopped = False
        if softStopT == 0.0:
            self.softStopT = duration
        elif softStopT < 0.0:
            self.softStopT = duration + softStopT
        else:
            self.softStopT = softStopT
        Interval.__init__(self, name, duration)

    
    def _ParticleInterval__step(self, dt):
        if self.particleEffect:
            self.particleEffect.accelerate(dt, 1, 0.050000000000000003)
        

    
    def _ParticleInterval__softStart(self):
        if self.particleEffect:
            self.particleEffect.softStart()
        
        self._ParticleInterval__softStopped = False

    
    def _ParticleInterval__softStop(self):
        if self.particleEffect:
            self.particleEffect.softStop()
        
        self._ParticleInterval__softStopped = True

    
    def privInitialize(self, t):
        if self.state != CInterval.SPaused:
            self._ParticleInterval__softStart()
            if self.particleEffect:
                self.particleEffect.clearToInitial()
            
            self.currT = 0
        
        if self.particleEffect:
            for forceGroup in self.particleEffect.getForceGroupList():
                forceGroup.enable()
            
        
        Interval.privInitialize(self, t)

    
    def privInstant(self):
        self.privInitialize(self.getDuration())
        self.privFinalize()

    
    def privStep(self, t):
        if self.state == CInterval.SPaused or t < self.currT:
            self.privInitialize(t)
        elif not (self._ParticleInterval__softStopped) and t > self.softStopT:
            self._ParticleInterval__step(self.softStopT - self.currT)
            self._ParticleInterval__softStop()
            self._ParticleInterval__step(t - self.softStopT)
        else:
            self._ParticleInterval__step(t - self.currT)
        Interval.privStep(self, t)

    
    def privFinalize(self):
        Interval.privFinalize(self)
        if self.cleanup and self.particleEffect:
            self.particleEffect.cleanup()
            self.particleEffect = None
        


