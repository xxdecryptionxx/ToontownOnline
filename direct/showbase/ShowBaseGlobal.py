# File: d (Python 2.4)

__all__ = []
from ShowBase import *
directNotify.setDconfigLevels()

def inspect(anObject):
    Inspector = Inspector
    import direct.tkpanels
    return Inspector.inspect(anObject)

import __builtin__
__builtin__.inspect = inspect
if not __debug__ and __dev__:
    notify = directNotify.newCategory('ShowBaseGlobal')
    notify.error("You must set 'want-dev' to false in non-debug mode.")

