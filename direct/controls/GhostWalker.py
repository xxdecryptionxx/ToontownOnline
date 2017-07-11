# File: d (Python 2.4)

from direct.showbase.ShowBaseGlobal import *
from direct.directnotify import DirectNotifyGlobal
import NonPhysicsWalker

class GhostWalker(NonPhysicsWalker.NonPhysicsWalker):
    notify = DirectNotifyGlobal.directNotify.newCategory('GhostWalker')
    slideName = 'jump'

