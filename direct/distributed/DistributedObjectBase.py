# File: d (Python 2.4)

from direct.showbase.DirectObject import DirectObject

class DistributedObjectBase(DirectObject):
    notify = directNotify.newCategory('DistributedObjectBase')
    
    def __init__(self, cr):
        self.cr = cr
        self.children = { }
        self.parentId = None
        self.zoneId = None

    
    def getLocation(self):
        
        try:
            if self.parentId == 0 and self.zoneId == 0:
                return None
            
            if self.parentId == 0xFFFFFFFFL and self.zoneId == 0xFFFFFFFFL:
                return None
            
            return (self.parentId, self.zoneId)
        except AttributeError:
            return None


    
    def handleChildArrive(self, childObj, zoneId):
        pass

    
    def handleChildArriveZone(self, childObj, zoneId):
        pass

    
    def handleChildLeave(self, childObj, zoneId):
        pass

    
    def handleChildLeaveZone(self, childObj, zoneId):
        pass

    
    def handleQueryObjectChildrenLocalDone(self, context):
        pass

    
    def getParentObj(self):
        if self.parentId is None:
            return None
        
        return self.cr.doId2do.get(self.parentId)

    
    def hasParentingRules(self):
        return self.dclass.getFieldByName('setParentingRules') != None


