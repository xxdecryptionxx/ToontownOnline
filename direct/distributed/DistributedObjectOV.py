# File: d (Python 2.4)

from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectBase import DistributedObjectBase
ESNew = 1
ESDeleted = 2
ESDisabling = 3
ESDisabled = 4
ESGenerating = 5
ESGenerated = 6

class DistributedObjectOV(DistributedObjectBase):
    notify = directNotify.newCategory('DistributedObjectOV')
    
    def __init__(self, cr):
        
        try:
            pass
        except:
            self.DistributedObjectOV_initialized = 1
            DistributedObjectBase.__init__(self, cr)
            self.activeState = ESNew


    
    def getDelayDeleteCount(self):
        return 0

    
    def deleteOrDelay(self):
        self.disableAnnounceAndDelete()

    
    def disableAnnounceAndDelete(self):
        self.disableAndAnnounce()
        self.delete()

    
    def disableAndAnnounce(self):
        if self.activeState != ESDisabled:
            self.activeState = ESDisabling
            messenger.send(self.uniqueName('disable'))
            self.disable()
        

    
    def announceGenerate(self):
        pass

    
    def disable(self):
        if self.activeState != ESDisabled:
            self.activeState = ESDisabled
        

    
    def isDisabled(self):
        return self.activeState < ESGenerating

    
    def isGenerated(self):
        return self.activeState == ESGenerated

    
    def delete(self):
        
        try:
            pass
        except:
            self.DistributedObjectOV_deleted = 1
            self.cr = None
            self.dclass = None


    
    def generate(self):
        self.activeState = ESGenerating

    
    def generateInit(self):
        self.activeState = ESGenerating

    
    def getDoId(self):
        return self.doId

    
    def postGenerateMessage(self):
        if self.activeState != ESGenerated:
            self.activeState = ESGenerated
            messenger.send(self.uniqueName('generate'), [
                self])
        

    
    def updateRequiredFields(self, dclass, di):
        dclass.receiveUpdateBroadcastRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()

    
    def updateAllRequiredFields(self, dclass, di):
        dclass.receiveUpdateAllRequired(self, di)
        self.announceGenerate()
        self.postGenerateMessage()

    
    def updateRequiredOtherFields(self, dclass, di):
        dclass.receiveUpdateBroadcastRequiredOwner(self, di)
        self.announceGenerate()
        self.postGenerateMessage()
        dclass.receiveUpdateOther(self, di)

    
    def getCacheable(self):
        return False

    
    def sendUpdate(self, fieldName, args = [], sendToId = None):
        if self.cr:
            if not sendToId:
                pass
            dg = self.dclass.clientFormatUpdate(fieldName, self.doId, args)
            self.cr.send(dg)
        else:
            self.notify.warning('sendUpdate failed, because self.cr is not set')

    
    def taskName(self, taskString):
        return '%s-%s-OV' % (taskString, self.getDoId())

    
    def uniqueName(self, idString):
        return '%s-%s-OV' % (idString, self.getDoId())


