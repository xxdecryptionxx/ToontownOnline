# File: d (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObject import DistributedObject

class DistributedObjectGlobal(DistributedObject):
    notify = directNotify.newCategory('DistributedObjectGlobal')
    neverDisable = 1
    
    def __init__(self, cr):
        DistributedObject.__init__(self, cr)
        self.parentId = 0
        self.zoneId = 0


